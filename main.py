# CMPS 245 - Homework 2
# Author: Santrupti Nerli
# Date: Jan 2017
#
# main.py performs calls the preprocessor and performs topic modeling

from preprocess import readAndProcessText
from topicmodel import performLdaTopicModeling, biTermTopicModeling

dataSetFile = '../Homework2_data.csv'
preprocessedOutputFile = './data/0.txt'

print "Performing read and preprocessing"
wordCt = readAndProcessText(dataSetFile, preprocessedOutputFile)

noWords = 3
noTopics = 3

print "Performing LDA topic modeling"
performLdaTopicModeling(noTopics, noWords, preprocessedOutputFile)

inputDir = './data/'
outputDir = './output/'
pathToOnlineBTM = 'OnlineBTM'

print "Performing Biterm topic modeling"
biTermTopicModeling(noTopics, wordCt, inputDir, outputDir, pathToOnlineBTM)
