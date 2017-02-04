# CMPS 245 - Homework 2
# Author: Santrupti Nerli
# Date: Jan 2017
#
# topicmodel.py performs topic modeling

import csv
import gensim
import subprocess
from gensim import corpora, models
from nltk.tokenize import TweetTokenizer

# method to perform tokenization of text
# we use tweet tokenizer to perform tokenization
def tokenize(text):
    tknzr = TweetTokenizer()
    words = tknzr.tokenize(text)
    return words

# method to read the tweet text from preprocessed output
# and then create a corpus which will be used by LDA to perform topic modeling
def readTextAndCreateCorpus(corpus, inputFileName):
    with open(inputFileName) as inputFile:
        texts = []
        for row in inputFile:
            texts.append(tokenize(row))

        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
    inputFile.close()
    return corpus

# method to perform topic modeling using LDA provided by gensim
def performLdaTopicModeling(topics, words, inputFileName):
    corpus = []
    corpus = readTextAndCreateCorpus(corpus, inputFileName)
    ldaModel = gensim.models.ldamodel.LdaModel(corpus, num_topics=topics)
    print(ldaModel.print_topics(num_topics=topics, num_words=words))

# method to perform topic modeling using Biterm topic modeling
# It executes a script that reads the data, learns, infers topics and finally display them
def biTermTopicModeling():
    subprocess.call(['./runBiterm.sh'])


# End
