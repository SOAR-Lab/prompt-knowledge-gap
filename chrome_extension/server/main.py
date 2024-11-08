from flask import Flask, request, jsonify
from flask_cors import CORS
from model import evaluate

import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize, sent_tokenize, RegexpTokenizer
from collections import Counter
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import itertools
import spacy
import contractions as ec
from spellchecker import SpellChecker
from textstat import textstat

import numpy as np

# nltk.download('punkt')
# nltk.download('punkt_tab')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('averaged_perceptron_tagger_eng')

model_name = "roberta-large-mnli"
model = AutoModelForSequenceClassification.from_pretrained(model_name)
auto_tokenizer = AutoTokenizer.from_pretrained(model_name)

app = Flask(__name__)

cors = CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    # Get the JSON data from the request
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Invalid JSON"}), 400

    # Extract the fields from the received data
    issue = data.get('issue')
    expected_outcome = data.get('expectedOutcome')
    programming_language = data.get('programmingLanguage')
    language_version = data.get('languageVersion')
    code_snippets = data.get('codeSnippets')
    error_log = data.get('errorLog')
    libraries = data.get('libraries')
    resources = data.get('resources')

    if len(issue) == 0 or len(expected_outcome) == 0:
        results = {
        'Specificity': 0,
        'Contextual Richness': 0,
        'Clarity': 0
        }
        return results, 200

    constraints_count, repeated_ngrams_count, entailment, uniq_info, misspelled, incomplete_count, Flesch_reading_ease, number_of_code, mean_code_size, code_desc_sent, num_urls, num_err, num_unresovled_ref = preprocess(issue, expected_outcome, code_snippets, resources, error_log)

    prompt = f'''You're an expert in software issue resolution. I'm going to describe the issue in a template, however, some of the fields might be empty.
    ## Issue Decription
    {issue}

    ## Expected Outcome
    {expected_outcome}

    ## Programming Language
    {programming_language}

    ## Programming Language Version
    {language_version}

    ## Code Snippets
    {code_snippets}

    ## Error Log
    {error_log}

    ## Libraries/Frameworks
    {libraries}

    ## Resources
    {resources}
    '''
    full_text = issue + ' ' + expected_outcome
    word_count = len(full_text.split())

    input = {
    '#Constraints': constraints_count,
    '#Repeated 3-grams': repeated_ngrams_count,
    '#Unique Info': uniq_info,
    'First Prompt Length': word_count,
    '#Code Snippets': number_of_code,
    'Mean Size Code Snippets': mean_code_size,
    '#Code Descriptions': code_desc_sent,
    '#URLs': num_urls,
    '#Error Messages': num_err,
    '#Misspellings': misspelled,
    '#Incomplete Sentences': incomplete_count,
    'Flesch Reading Ease': Flesch_reading_ease,
    'Entailment': entailment,
    '#Unresolved References': num_unresovled_ref
    }
    print(input)

    score = evaluate(input_data=input)
    print(score)

    if len(programming_language) != 0:
        programming_language = 1
    else:
        programming_language = 0
    if len(language_version) != 0:
        language_version = 1
    else:
        language_version = 0
    results = (calculate_heuristics(input, programming_language, language_version, len(libraries), prompt))
    # Return a response

    return results, 200

def calculate_heuristics(input_data, programming_language, language_version, libraries, prompt):
    # Set up the maximum desirable values (these can be fine-tuned)
    thresholds = {
        'specificity': {'#Constraints': 1, '#Repeated 3-grams': 2, 'programming_language':1, 'language_version': 1, 'libraries': 1},
        'contextual_richness': {
            '#Unique Info': 16, 'First Prompt Length': 103, '#Code Snippets': 2, 
            'Mean Size Code Snippets': 135, '#Code Descriptions': 3, 
            '#URLs': 1, '#Error Messages': 1
        },
        'clarity': {
            '#Misspellings': 2, '#Incomplete Sentences': 1, 
            'Flesch Reading Ease': 78, 'Entailment': 0.25, 
            '#Unresolved References': 0
        }
    }

    # Helper function to calculate percentages for each feature
    def calculate_feature_percentage(value, max_value):
        return min((value / max_value) * 100, 100) if max_value else 0

    # Calculate specificity score
    specificity_scores = [
        calculate_feature_percentage(input_data['#Constraints'], thresholds['specificity']['#Constraints']),
        calculate_feature_percentage(input_data['#Repeated 3-grams'], thresholds['specificity']['#Repeated 3-grams']),
        calculate_feature_percentage(programming_language, thresholds['specificity']['programming_language']),
        calculate_feature_percentage(language_version, thresholds['specificity']['language_version']),
        calculate_feature_percentage(libraries, thresholds['specificity']['libraries']),
    ]
    specificity = np.mean(specificity_scores)

    # Calculate contextual richness score
    contextual_richness_scores = [
        calculate_feature_percentage(input_data['#Unique Info'], thresholds['contextual_richness']['#Unique Info']),
        calculate_feature_percentage(input_data['First Prompt Length'], thresholds['contextual_richness']['First Prompt Length']),
        calculate_feature_percentage(input_data['#Code Snippets'], thresholds['contextual_richness']['#Code Snippets']),
        100 - calculate_feature_percentage(input_data['Mean Size Code Snippets'], thresholds['contextual_richness']['Mean Size Code Snippets']),
        calculate_feature_percentage(input_data['#Code Descriptions'], thresholds['contextual_richness']['#Code Descriptions']),
        calculate_feature_percentage(input_data['#URLs'], thresholds['contextual_richness']['#URLs']),
        calculate_feature_percentage(input_data['#Error Messages'], thresholds['contextual_richness']['#Error Messages']),
    ]
    print(contextual_richness_scores)
    contextual_richness = np.mean(contextual_richness_scores)

    # Calculate clarity score
    clarity_scores = [
        100 - calculate_feature_percentage(input_data['#Misspellings'], thresholds['clarity']['#Misspellings']),
        calculate_feature_percentage(input_data['#Incomplete Sentences'], thresholds['clarity']['#Incomplete Sentences']),
        calculate_feature_percentage(input_data['Flesch Reading Ease'], thresholds['clarity']['Flesch Reading Ease']),
        calculate_feature_percentage(input_data['Entailment'], thresholds['clarity']['Entailment']),
        100 - calculate_feature_percentage(input_data['#Unresolved References'], thresholds['clarity']['#Unresolved References'])
    ]
    clarity = np.mean(clarity_scores)

    if specificity < 0:
        specificity = 0
    if contextual_richness < 0:
        contextual_richness = 0
    if clarity < 0:
        clarity = 0
    # Aggregate results
    results = {
        'Specificity': specificity,
        'Contextual Richness': contextual_richness,
        'Clarity': clarity,
        'prompt': prompt
    }

    return(results)

def preprocess(issue, expected_outcome, code_snippets, resources, error_log):
    text = issue + ' ' + expected_outcome

    sentences = sent_tokenize(text)
    constraints_count = 0

    for sentence in sentences:
        # Tokenize each sentence into words
        words = word_tokenize(sentence)
        # Get the part-of-speech tags for the words
        pos_tags = pos_tag(words)

        # Count constraints (e.g., 'if', 'unless', 'provided that', 'in case of')
        constraints_keywords = {'if', 'unless', 'provided', 'in case', 'only'}
        constraints_count += sum(1 for word, tag in pos_tags if word.lower() in constraints_keywords)
    
    all_ngrams = []

    # Extract n-grams from each prompt and add them to the list
    all_ngrams.extend(extract_ngrams(text, 3))
    
    # Count the occurrences of each n-gram
    ngram_counts = Counter(all_ngrams)
    
    # Count the number of n-grams that occur more than once
    repeated_ngrams_count = sum(1 for count in ngram_counts.values() if count > 1)

    # Load model and tokenizer
    inputs = auto_tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    # Get probabilities
    probs = torch.softmax(logits, dim=-1)
    entailment = probs[0][0].item()

    tokenizer = RegexpTokenizer(r'\w+')
    nlp = spacy.load('en_core_web_sm')

    total_word = []
    total_word_count = []
    for sent in sentences:
        # Calculate number of words
        words = tokenizer.tokenize(sent)
        words = [word.lower() for word in words if word.isalpha()]
        word_no = len(words)
        total_word_count.append(word_no)
        total_word.append(words)

    # Calculate Amount of unique information- no of distinct words/total no of words
    distinct_words = list(set(list(itertools.chain(*total_word))))  # flatten and create unique list
    try:
        uniq_info = len(distinct_words) / len(total_word)
    except:
        uniq_info = 0

    incomplete_count = 0
    incomplete = []
    misspelled = []

    spell = SpellChecker()
    spell.word_frequency.load_text_file('synonymAbbreviation_manualCheck.txt')
    spell.word_frequency.load_text_file('./Software_terms.txt')
    spell.word_frequency.load_words(['cannot', 'doesn', 'isn', 'wouldn'])

    # Calculate number of incomplete sentences
    for sent in sentences:
        # Expand contractions - Don't -> do not, etc
        sent = ec.expand_contractions(sent)

        sent_dep = nlp(sent)
        nsubj = [tok for tok in sent_dep if (tok.dep_ == "nsubj")]
        dobj = [tok for tok in sent_dep if (tok.dep_ == "dobj")]
        if not (nsubj or dobj):
            incomplete.append(sent)
            incomplete_count += 1

        words = tokenizer.tokenize(sent)
        # Remove proper names (e.g. Usernames) and make sure all characters in the word are alphabets
        words = [word for word in words if (word.isalpha() and word[0].isupper() == False)]
        misspelled.append(spell.unknown(words))

    # Stem words and create unique list
    misspelled = list(set(list(itertools.chain(*misspelled))))

    # Calculate readability scores
    Flesch_reading_ease = textstat.flesch_reading_ease(text)

    code_identifiers = []
    code_snippet_size = 0
    number_of_code = len(code_snippets)
    for snippet in code_snippets:
        code = snippet.get('content')
        code_identifier = tokenizer.tokenize(code)
        code_identifiers.append([c for c in code_identifier])
        code_snippet_size += (len(code) - code.count(' '))
    
    try:
        mean_code_size = code_snippet_size / number_of_code
    except:
        mean_code_size = 0

    code_desc_sent = 0
    for sent in sentences:
        for identifier in code_identifiers:
            if (len(identifier) > 2) and (identifier in word_tokenize(sent)):
                code_desc_sent += 1
    
    num_urls = len(resources)

    num_err = 0
    if len(error_log) != 0:
        num_err = 1

    num_unresovled_ref = 0
    return(constraints_count, repeated_ngrams_count, entailment, uniq_info, len(misspelled), incomplete_count, Flesch_reading_ease, number_of_code, mean_code_size, code_desc_sent, num_urls, num_err, num_unresovled_ref)

    
def extract_ngrams(text, n):
    """
    Extract n-grams from the text.

    Args:
    text (str): The input text (a prompt).
    n (int): The length of n-grams to extract.

    Returns:
    list: A list of n-grams from the input text.
    """
    words = text.split()
    ngrams = [tuple(words[i:i+n]) for i in range(len(words)-n+1)]
    return ngrams


if __name__ == '__main__':
    app.run(debug=True)
