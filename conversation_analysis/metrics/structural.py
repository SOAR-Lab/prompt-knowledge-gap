import re
import spacy
from utils import urlmatch
from nltk.tokenize import sent_tokenize, word_tokenize, RegexpTokenizer
import os.path
from utils.api_call import ApiCallStyle
import itertools

# spacy.cli.download("en_core_web_lg")
nlp = spacy.load('en_core_web_lg')


class KnowledgeSeekingSharing:

    def __init__(self):
        self.acc_indicators = ["thanks", "thx", "appreciate", "works", "helpful", "useful"]

    def analyze(self, text):
        is_prim_ques = 0
        is_prim_ks_ques = 0
        is_acc_ans = 0

        # Remove code segments and replace with a blank
        try:
            text = re.sub('`([^`]*)`', '[CODE]', text)
        except:
            print("Error in removing code snippets from text")
        sentence = sent_tokenize(text)

        # Check if there is a primary question in the 1st utterance
        ques_word = ['what', 'where', 'when', 'why', 'who', 'how']
        ks_word = ['how', 'where', 'what']

        for sent in sentence:
            if ('?' in sent) or (sent.split(' ')[0].lower() in ques_word):
                is_prim_ques += 1
                # check if primary question is knowledge seeking
                for word in ks_word:
                    if word in sent:
                        is_prim_ks_ques += 1

        # Check if there is an accepted answer (primary questioner replies with any of the indicators above)
        # Checking similarity of indicators using word embeddings of sentences.
        # for sent in sentence:
        #     for ind in self.acc_indicators:
        #         if nlp(ind).similarity(nlp(sent)) > 0.7:
        #             is_acc_ans += 1
        #
        # print("\nKnowledge Seeking/Sharing")
        # print("##########################")
        # print("# of Primary question: ", is_prim_ques)
        # print("# of Primary question knowledge-seeking: ", is_prim_ks_ques)
        # print("# of acceptance of answer: ", is_acc_ans)

        return is_prim_ques, is_prim_ks_ques, is_acc_ans


class Contextual:
    def __init__(self):
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.code_reg = r'`([^`]*)`|```([^`]+)```'
        self.error_regex = r'error(.*?):'  # "Error followed by a colon is a general pattern for errors and stack trace"

    def analyze(self, message, errors_list, codes_list, code_blocks_list):
        urls = []
        code_snippets_count = 0
        contain_code = 0
        code_snippet_size = 0
        code_snippets = []
        code_identifiers = []
        api_calls_code = []
        api_calls_text = []
        code_desc_sent = 0
        contain_code_desc = 0
        SE_words = []
        SE_Wordlist = self.SEWords()
        err_msg = 0
        contain_err_msg = 0

        # codes_list.extend(code_blocks_list)

        # Remove code segments and replace with a blank
        text = re.sub(self.code_reg, '[CODE]', message)

        findurls = text.count('[URL]')

        # Calculate number of API mentions in text
        for style in ApiCallStyle:
            api_call_pattern = style.value
            for match in re.finditer(api_call_pattern, text):
                api_calls_text.append(match.group())
            if len(api_calls_text) != 0:
                break
        # print(api_calls_text)

        # Contains code
        for code in codes_list:
            if len(code) == 0 or len(code) == 1:
                continue
            code_snippets.append(code)
            code_snippet_size += (len(code) - code.count(' '))
            contain_code = 1
        code_snippets_count += len(code_snippets)

        # Check if there is error message
        for error in errors_list:
            if len(error) == 0 or len(error) == 1:
                continue
            err_msg += 1
            contain_err_msg = 1

        # Contains code description
        # Create code identifiers
        for code in code_snippets:
            code_identifier = self.tokenizer.tokenize(code)
            code_identifiers.append([code for code in code_identifier])
        code_identifiers = list(set(list(itertools.chain(*code_identifiers))))  # flatten and create unique list

        for sent in sent_tokenize(text):
            for identifier in code_identifiers:
                if (len(identifier) > 2) and (identifier in word_tokenize(sent)):
                    code_desc_sent += 1
                    contain_code_desc = 1

        # # Add to code snippet count if there is a link to code snippet in the message
        # for url in urls:
        #     if url.startswith('https://gist'):
        #         code_snippets_count += 1
        #         contain_code = 1
        #     if url.startswith('https://pastebin'):
        #         code_snippets_count += 1
        #         contain_code = 1

        try:
            mean_code_size = code_snippet_size / code_snippets_count
        except:
            mean_code_size = 0

        # Calculate number of API mentions in code
        for style in ApiCallStyle:
            api_call_pattern = style.value
            for code_snippet in code_snippets:
                for match in re.finditer(api_call_pattern, code_snippet):
                    api_calls_code.append(match.group())
            if len(api_calls_code) != 0:
                break

        # Calculate number of software specific words
        for word in list(set(word_tokenize(text))):
            if word in SE_Wordlist:
                SE_words.append(word)

        print("\nContextual")
        print("#############")
        print("Number of urls: ", findurls)
        print("Number of code snippets: ", code_snippets_count)
        print("Mean size of code snippets: ", mean_code_size)
        print("Number of unique API calls in code: ", len(set(api_calls_code)))
        print("Number of unique API calls in text: ", len(set(api_calls_text)))
        print("Number of sentences describing code: ", code_desc_sent)
        print("Number of SE words: ", len(SE_words))
        print("Number of error messages: ", err_msg)

        return (findurls, code_snippets_count, mean_code_size, len(set(api_calls_code)), len(set(api_calls_text)),
                code_desc_sent, len(SE_words), err_msg)

    def SEWords(self):
        my_path = os.path.abspath(os.path.dirname(__file__))
        with open(os.path.join(my_path, 'synonymAbbreviation_manualCheck.txt'), 'r') as abbrev_f, \
                open(os.path.join(my_path, 'Software_terms.txt'), 'r') as terms_f:
            SEWords1 = [word for line in abbrev_f for word in (line.strip('\n')).split(',')]
            SEWords2 = [line.strip(' ').strip('\n').strip('\t') for line in terms_f]
        return SEWords1 + SEWords2
