# CMPS 245 - Homework 2
# Author: Santrupti Nerli
# Date: Jan 2017
#
# preprocess.py performs preprocessing of tweets

import csv
import re
from normalizr import Normalizr
from nltk.tokenize import TweetTokenizer

# method to perform processing of text
# it internally calls methods to perform cleaning and normalization of text for us
def processText(text):
    global wordCtr
    text = removeURLs(text)
    text = removeAtSymbol(text)
    words = tokenize(text)
    words = removeTrailingHashTags(words)
    text = " ".join(words)
    text = normalize(text)
    wordCtr += len(words)
    return text

# method to remove URLs using a regex
# remove everything that starts with http and goes on until a space is encountered
def removeURLs(text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"www\.\S+", "", text)
    return text

# method to remove @ symbol from twitter user names
def removeAtSymbol(text):
    text = re.sub(r"@", "", text)
    return text

# method to perform tokenization of text
# we use tweet tokenizer to perform tokenization
def tokenize(text):
    tknzr = TweetTokenizer()
    words = tknzr.tokenize(text)
    return words

# method to remove hash tags
# tokenize the text
# lookfor hash tags from the end of the tokenized words until you hit a
# non-hashtagged word
def removeTrailingHashTags(words):
    index = len(words)-1
    for w in reversed(words):
        if w.startswith('#'):
            words[index] = ''
        else:
            break
        index -= 1
    return words

# method to load the normalization dictionary
def loadNormalizationDictionary(dictionaryFile):
    dictionary = {}
    with open(dictionaryFile) as dictFile:
        reader = csv.reader(dictFile)
        for row in reader:
            dictionary[row[0]] = row[1]
    dictFile.close()
    return dictionary

# method to perform normalization
# here, we remove stop words, accet marks, emojis, puntuation and extra white spaces
# we also replace OOV words by using a dictionary
def normalize(text):
    normalizr = Normalizr(language='en')
    normalizations = [
        'remove_stop_words',
        'remove_accent_marks',
        ('replace_emojis', {'replacement': ' '}),
        ('replace_punctuation', {'replacement': ' '}),
        'remove_extra_whitespaces'
    ]
    text = normalizr.normalize(text, normalizations)
    words = tokenize(text)
    for word in words:
        if word in dictionary:
            text = text.replace(word, dictionary[word])
        elif len(word) == 1:
            text = text.replace(word, "")
    return text


# open the csv file for read and write
# for each row, perform the preprocessing on the text
# write only the prcessed text to the output file
def readAndProcessText(inputFileName, outputFileName):
    with open(inputFileName) as inputFile:
        reader = csv.reader(inputFile)
        header = reader.next()
        with open(outputFileName, 'w') as outputFile:
            fieldnames = ['Tweet_text', 'ID']
            for row in reader:
                textToProcess = row[header.index('Tweet_text')]
                processedRow = processText(textToProcess)
                outputFile.write(processedRow.encode('ascii', 'ignore'))
                outputFile.write("\n")
        outputFile.close()
    inputFile.close()
    return wordCtr

wordCtr = 0
dictionary = {}
dictionary = loadNormalizationDictionary('Dictionary.csv')

# end
