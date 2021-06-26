"""Helper class to deal with NLP Actions"""
import re
import string
from nltk.tag import pos_tag
from nltk import RegexpParser
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


class Actions:
    """Actions class definition"""

    def __init__(self, input_str):
        self.input_str = input_str

    def convert_to_lower(self):
        """ Converts to lower case """
        self.input_str = self.input_str.lower()
        return self

    def remove_numbers(self):
        """ Removes number from string """
        self.input_str = re.sub(r'\d+', '', self.input_str)
        return self

    def remove_punctuation(self):
        """ Removes punctuation from string """
        self.input_str = self.input_str.translate(
            str.maketrans('', '', string.punctuation))
        return self

    def remove_whitespace(self):
        """ Removes whitespaces from string """
        self.input_str = self.input_str.strip()
        return self

    def remove_stop_words(self):
        """ Removes stop words from string """
        self.input_str = ' '.join([word for word in word_tokenize(
            self.input_str) if word not in ENGLISH_STOP_WORDS])
        return self

    def lemmantize_sentence(self):
        """ Lemmantizes tokens from string """
        self.input_str = ' '.join([WordNetLemmatizer().lemmatize(
            word) for word in word_tokenize(self.input_str)])
        return self

    def convert_to_chunks(self):
        """ Create Chunks from string """
        tokens = word_tokenize(self.input_str)
        grammar = "NP: {<DT>?<JJ>*<NN>}"
        cp = RegexpParser(grammar)
        return cp.parse(pos_tag(tokens))
