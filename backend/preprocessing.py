import re
import sys
import os
import nltk
import string

from nltk.tokenize import TweetTokenizer
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')


def tokenize(string_text):
    '''
    Input:
        string
    Output:
        list of tokens
    This function split the input string into individual words and removes all punctuations
    '''
    tweetTokenizer = TweetTokenizer()
    tokens = tweetTokenizer.tokenize(string_text)

    tokens_list = list(filter(None, [s.translate(str.maketrans('','',string.punctuation)) for s in tokens]))
    return tokens_list

def stem(tokens):
    '''
    Input:
        list of tokens
    Output:
        list of tokens after stemming
    Use Porter Stemmer to stem words in the list of tokens
    '''
    ps = PorterStemmer()
    return [ps.stem(token) for token in tokens]


def preprocess(string, stemming=True, stop=False):
    '''
    Input:
        string: text to be preprocessed
        stemming: boolen of whether to stem individual stop_words
        stop: boolen of whether to remove stop words
    Output:
        list of preprocessed tokens
    This function preprocesses the input string, by calling the previous 'tokenize' and 'stem'
    function, and remove the stop words if the related boolen is True
    '''
    tokenized = tokenize(string)
    stop_words = set(stopwords.words('english'))
    filtered = [term.lower() for term in tokenized if term not in stop_words or not stop]
    if (stemming):
        filtered = stem(filtered)
    return list(filter(lambda x: x.isalnum(), filtered))
