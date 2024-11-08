import re
from nltk.tokenize import sent_tokenize, RegexpTokenizer
import itertools
import spacy
import os.path
from textstat import textstat
from spellchecker import SpellChecker
from utils import contractions as ec
from nltk.stem import PorterStemmer
import pandas as pd
import numpy as np


class Psycholinguistics:
    def __init__(self):
        pass


class Diversity:
    def __init__(self):
        self.tokenizer = RegexpTokenizer(r'\w+')

    def analyze(self, clean_text):
        total_sent = 0
        total_word = []
        total_word_count = []

        message = clean_text
        # Remove code segments and replace with a blank
        message = re.sub(r'`([^`]*)`|```([^`]+)```', ' ', message)
        # Remove urls and replace with "url"
        message = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', 'url',
                         message)

        # Calculate number of sentences
        sentence = sent_tokenize(message)
        sent_no = len(sentence)
        total_sent += sent_no

        for sent in sentence:
            # Calculate number of words
            words = self.tokenizer.tokenize(sent)
            words = [word.lower() for word in words if word.isalpha()]
            word_no = len(words)
            total_word_count.append(word_no)
            total_word.append(words)

        # Calculate Amount of unique information- no of distinct words/total no of words
        distinct_words = list(set(list(itertools.chain(*total_word))))  # flatten and create unique list
        uniq_info = len(distinct_words) / len(total_word)

        print("\nDiversity")
        print("#############")
        print("# Unique words: ", len(distinct_words))
        print("# Unique information: ", uniq_info)

        return len(distinct_words), uniq_info


class Readability:
    def __init__(self):
        my_path = os.path.abspath(os.path.dirname(__file__))
        df = pd.read_excel(os.path.join(my_path, 'TextSpeak.xlsx'))
        text_speak_list = (df['Abbv']).tolist()

        # spacy.cli.download("en_core_web_sm")
        self.nlp = spacy.load('en_core_web_sm')
        self.spell = SpellChecker()
        self.spell.word_frequency.load_text_file(os.path.join(my_path, 'synonymAbbreviation_manualCheck.txt'))
        self.spell.word_frequency.load_text_file(os.path.join(my_path, './Software_terms.txt'))
        self.spell.word_frequency.load_words(['cannot', 'doesn', 'isn', 'wouldn'])
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.stemmer = PorterStemmer()
        self.text_speak = [str(x).lower() for x in text_speak_list]

    def analyze(self, text):
        incomplete_count = 0
        total_sent_count = 0
        incomplete = []
        misspelled = []
        total_text_speak = 0

        message = text
        # Remove code segments and replace with a blank
        message = re.sub('`([^`]*)`', ' ', message)
        # Remove urls and replace with a blank
        message = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ',
                         message)

        sentence = sent_tokenize(message)
        total_sent_count += len(sentence)

        for sent in sentence:
            # Calculate number of words
            words = self.tokenizer.tokenize(sent)
            words = [word.lower() for word in words if word.isalpha()]

            for wd in words:
                # Calculate number of text speaks
                if wd in self.text_speak:
                    total_text_speak += 1

        # Calculate number of incomplete sentences
        for sent in sentence:
            # Expand contractions - Don't -> do not, etc
            sent = ec.expand_contractions(sent)

            sent_dep = self.nlp(sent)
            nsubj = [tok for tok in sent_dep if (tok.dep_ == "nsubj")]
            dobj = [tok for tok in sent_dep if (tok.dep_ == "dobj")]
            if not (nsubj or dobj):
                incomplete.append(sent)
                incomplete_count += 1

            # Calculate number of misspelled words
            # include code identifiers in list of words in dictionary
            # self.spell.word_frequency.load_words(id for id in code_identifiers)
            words = self.tokenizer.tokenize(sent)
            # Remove proper names (e.g. Usernames) and make sure all characters in the word are alphabets
            words = [word for word in words if (word.isalpha() and word[0].isupper() == False)]
            misspelled.append(self.spell.unknown(words))

        # Stem words and create unique list
        misspelled = list(set(list(itertools.chain(*misspelled))))
        complete_count = total_sent_count - incomplete_count

        # Calculate readability scores
        ARI = textstat.automated_readability_index(message)
        Coleman_Liau = textstat.coleman_liau_index(message)
        Flesch_reading_ease = textstat.flesch_reading_ease(message)
        Flesch_Kincaid_grade = textstat.flesch_kincaid_grade(message)
        Gunning_Fog = textstat.gunning_fog(message)
        Smog = textstat.smog_index(message)

        print("\nReadability")
        print("##########################")
        print("Total number of misspelled words: ", len(misspelled))
        print("Total number of incomplete sentences: ", incomplete_count)
        print("Total number of complete sentences: ", complete_count)
        print("Total number of text speaks: ", total_text_speak)
        print("Readability scores: ", ARI, Coleman_Liau, Flesch_reading_ease, Flesch_Kincaid_grade,
              Gunning_Fog, Smog)

        return len(misspelled), incomplete_count, total_text_speak, ARI, Coleman_Liau, Flesch_reading_ease, Flesch_Kincaid_grade, Gunning_Fog, Smog


class Verbosity:
    def __init__(self):
        self.tokenizer = RegexpTokenizer(r'\w+')

    def analyze(self, text):
        total_sent = 0
        total_word_count = []

        message = text

        # Calculate number of sentences
        sentence = sent_tokenize(message)
        sent_no = len(sentence)
        total_sent += sent_no

        for sent in sentence:
            # Calculate number of words
            words = self.tokenizer.tokenize(sent)
            words = [word.lower() for word in words if word.isalpha()]
            word_no = len(words)
            total_word_count.append(word_no)

        print("\nVerbosity")
        print("#############")
        print("Total no. of sentences: ", total_sent)
        print("Total no. of words: ", np.sum(total_word_count))
        return total_sent, np.sum(total_word_count)


class Sentiment:
    def __init__(self):
        pass
