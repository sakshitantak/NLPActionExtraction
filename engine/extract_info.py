"""Python Script to work with NLP Actions"""
import re
import sys
import json
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from actions import Actions
from database_helper import MongoHelper, TestCaseHelper
#import requests
import pandas as pd
import numpy as np
import nltk
import json
import csv
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.model_selection import train_test_split
from sklearn import naive_bayes
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import make_pipeline
#import desk
import pickle

nltk.download('stopwords')
stops = stopwords.words("english")


def main(SENTENCE, option):
    """ 
    Action Threshold which limits the number of
    tokens which needs to match in
    order to be considered as prediction
    """
    #print(type(SENTENCE))
    ACTION_THRESHOLD = 4

    def tree_to_string(inp):
        """ Converts Trees to String """
        return inp[0] if isinstance(inp, tuple) else ''.join([i for i in tree_to_string(inp[0])])

    def check_if_present_in_file(action_tokens):
        """ Checks if any element of array present in file """
        flag = False
        for token in action_tokens:
            flag = flag or check_keyword(token)
        return flag

    def check_keyword(keyword):
        """ Checks if token present in file """
        flag = False
        with open('unique-keywords.txt') as file:
            if keyword in file.read():
                flag = True
        return flag

    WRITE_USER = False
    WRITE_ACTION = False
    WRITE_EXPECTATION = False
    RESULT_ITE = {
        "case_id": "",
        "user": "",
        "action": "",
        "expectation": "",
        "type": False,
        "predictions": []
    }

    """ Using NLP to tokenize the sentences with tags """
    TOKENS = word_tokenize(SENTENCE)
    #TOKENS = [word for word in TOKENS if not word in stopwords.words()]

    """ Storing the tokens as a copy of extracted tokens """
    RESULT_ITE["tokens"] = TOKENS.copy()

    """ Finding first nouns which denote to the user """
    for index, _ in enumerate(TOKENS):
        if "NN" in pos_tag(TOKENS)[index][1]:
            RESULT_ITE["user"] = ""
            WRITE_USER = True
        if WRITE_USER and pos_tag(TOKENS)[index][1] == ",":
            WRITE_USER = False
            del TOKENS[1:index + 1]
            break

        if WRITE_USER:
            RESULT_ITE["user"] += TOKENS[index] + " "

    """ Finding first verbs which denote to the action """
    for index, _ in enumerate(TOKENS):
        if "VB" in pos_tag(TOKENS)[index][1]:
            WRITE_ACTION = True

        if WRITE_ACTION and pos_tag(TOKENS)[index][1] == ",":
            WRITE_ACTION = False
            del TOKENS[1:index + 1]
            break

        if WRITE_ACTION:
            RESULT_ITE["action"] += TOKENS[index] + " "
    
    if "so that " in RESULT_ITE["action"]:
        RESULT_ITE["action"] = RESULT_ITE["action"].split("so that")[0]
        #print(RESULT_ITE["action"])

        

    """ Finding objective which denote to the expectations """
    for index, _ in enumerate(TOKENS):
        if "IN" in pos_tag(TOKENS)[index][1]:
            WRITE_EXPECTATION = True

        if WRITE_EXPECTATION:
            RESULT_ITE["expectation"] += TOKENS[index] + " "
            if "so that " in RESULT_ITE["expectation"]:
                RESULT_ITE["expectation"] = (RESULT_ITE["expectation"].split("so that"))[1]
        
        if WRITE_EXPECTATION and pos_tag(TOKENS)[index][1] == ".":
            WRITE_EXPECTATION = False
            break

    """
    Pre-processing data by implementing techniques in the following sequence:
    1 . Converting all letter in string to lower case.
    2 . Removing numbers from string.
    3 . Removing Punctuations from the string.
    4 . Remove whitespaces from the string.
    5 . Remove stop words from the string.
    6 . Lemmantize the sentences to get filter out common tenses.
    7 . Converting string to chunks.
    """
    ACTION_TOKENS = Actions(RESULT_ITE['action']) \
        .convert_to_lower() \
        .remove_numbers() \
        .remove_punctuation() \
        .remove_whitespace() \
        .remove_stop_words() \
        .lemmantize_sentence() \
        .convert_to_chunks() \
    
   
    text_categories = [0, 1]

    #function to give prediction
    def my_prediction(my_sent, option):
        if option == "whatsapp":
            #print(type(option))
            model = pickle.load(open(r"C:/Users/saksh/Sakshi Tantak/NLPActionExtraction/engine/model_binomialnb.sav", 'rb'))
            my_sent = [' '.join([word for word in my_sent.split() if word not in stops])]
            prediction = "UNIQUE" if model.predict(my_sent).astype(int) == 1 else "GENERIC"
            return prediction
        elif option == "bank":
            model = pickle.load(open(r"C:/Users/saksh/Sakshi Tantak/NLPActionExtraction/engine/model_binomialnb.sav", 'rb'))
            my_sent = [' '.join([word for word in my_sent.split() if word not in stops])]
            prediction = "UNIQUE" if model.predict(my_sent).astype(int) == 1 else "GENERIC"
            return prediction
        elif option == "publisher":
            model = pickle.load(open(r"C:/Users/saksh/Sakshi Tantak/NLPActionExtraction/engine/model_binomialnb.sav", 'rb'))
            my_sent = [' '.join([word for word in my_sent.split() if word not in stops])]
            prediction = "UNIQUE" if model.predict(my_sent).astype(int) == 1 else "GENERIC"
            return prediction
        else:
            model = pickle.load(open(r"C:/Users/saksh/Sakshi Tantak/NLPActionExtraction/engine/model_binomialnb.sav", 'rb'))
            my_sent = [' '.join([word for word in my_sent.split() if word not in stops])]
            prediction = "UNIQUE" if model.predict(my_sent).astype(int) == 1 else "GENERIC"
            return prediction


    ACTION_LIST = [tree_to_string(word) for word in ACTION_TOKENS]
    RESULT_ITE['type'] = my_prediction(SENTENCE, option)

    ACTION_REGEX = re.compile(
        "(?:" + '|'.join(ACTION_LIST) + ")", re.IGNORECASE)
    ACTIONS_FOUND = MongoHelper.get_all_objects({'action': ACTION_REGEX})


    ACTIONS_DICT = {}
    for action in ACTIONS_FOUND:
        if action['expectation'] not in ACTIONS_DICT.keys():
            ACTIONS_DICT[action['expectation']] = [action['action']]
        else:
            ACTIONS_DICT[action['expectation']].append(action['action'])

    COUNT_ACTIONS = {}
    for key, value in ACTIONS_DICT.items():
        if len(value) >= ACTION_THRESHOLD:
            COUNT_ACTIONS[key] = len(value)

    RESULT_ITE['predictions'].extend(
        [item for item in COUNT_ACTIONS.keys() if item != RESULT_ITE['expectation']])

    RESULT_ITE['predictions'] = list(set(RESULT_ITE['predictions']))

    for word in ACTION_TOKENS.leaves():
        MongoHelper.insert_if_not_exist({
            'action': tree_to_string(word),
            'expectation': RESULT_ITE['expectation'],
            'common': RESULT_ITE['type'] #True if RESULT_ITE['type'] == 'UNIQUE' else False
        })

    RESULT_ITE['case_id'] = TestCaseHelper.get_testcase_id(
        'UTC' if RESULT_ITE['type'] == 'UNIQUE' else 'GTC'
    )

    rg = re.compile("((?:[\\w\\d_.-]*)) = ((?:[\\w\\d_.-]*))",
                    re.IGNORECASE | re.DOTALL)
    RESULT_ITE['inputs'] = re.findall(rg, RESULT_ITE['action'])

    return RESULT_ITE


if __name__ == '__main__':
    """ Gets the first argument from the command line input """
    FIN_RES = main(sys.argv[1], sys.argv[2])
    print(json.dumps(FIN_RES))
    sys.stdout.flush()
