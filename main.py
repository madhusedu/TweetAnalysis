# CMPS 245 - Homework 2
# Author: Santrupti Nerli
# Date: Jan 2017
#
# main.py performs calls the preprocessor and performs topic modeling

from preprocess import readAndProcessText
from topicmodel import performLdaTopicModeling, biTermTopicModeling

print "Performing read and preprocessing"
readAndProcessText('../Homework2_data.csv', './data/0.txt')

noWords = 3
noTopics = 3

print "Performing LDA topic modeling"
performLdaTopicModeling(noTopics, noWords, './data/0.txt')

print "Performing Biterm topic modeling"
biTermTopicModeling()
