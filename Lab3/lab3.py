import random
import math
import re
import operator
import numpy as np
from collections import OrderedDict
from string import digits

letters = ' abcdefghijklmnopqrstuvwxyz0123456789'


def getProbs(text, n):
    probs = {}
    count = 0
    for i in range(len(text) - n + 1):
        ngram = text[i:i+n]
        count += 1
        if tuple(ngram) in probs:
            probs[tuple(ngram)] += 1
        else:
            probs[tuple(ngram)] = 1
    for key in probs.keys():
        probs[key] /= count
    return probs


def printProbs(probs):
    for key, value in sorted(probs.items(), key=operator.itemgetter(1), reverse=True):
        print(key, value)


def calculateEntropy(probs):
    entropy = 0
    for prob in probs.values():
        entropy += prob * math.log(prob, 2)
    return -entropy


def calculateConditionalEntropy(probs, conditionalProbs):
    entropy = 0
    # print(probs)
    for key, value in conditionalProbs.items():
        # print(key)
        for key2, prob in value.items():
            if key + tuple(key2) in probs.keys():
                entropy += probs[key + tuple(key2)] * math.log(prob, 2)
    return -entropy
    

def calculateTheoriticalEntropy():
    entropy = 0
    prob = 1/len(letters)
    for i in range(len(letters)):
        entropy += prob * math.log(prob, 2)
    return -entropy


def normalizeProbability(probs):
    sum1 = sum(list(probs.values()))
    for key in probs.keys():
        probs[key] /= sum1


def getConditionalProbability(text, n):
    conditionalProbs = {}
    nGramPlusOneProbs = getProbs(text, n+1)
    nGramProbs = getProbs(text, n)
    for k in nGramProbs.keys():
        conditionalProbs[k] = {}
        for letter in letters:
            newKey = k + tuple(letter)
            if newKey in nGramPlusOneProbs.keys():
                conditionalProbs[k][letter] = nGramPlusOneProbs[newKey] / nGramProbs[k]
        normalizeProbability(conditionalProbs[k])
    return nGramPlusOneProbs, conditionalProbs


def getWordsProbs(words, n):
    probs = {}
    count = len(words) - n + 1
    for i in range(count):
        ngram = words[i:i+n]
        if tuple(ngram) in probs:
            probs[tuple(ngram)] += 1 
        else:
            probs[tuple(ngram)] = 1
    for key in probs.keys():
        probs[key] /= count
    return probs


file = open('norm_wiki_en.txt', 'r')
text = file.read()[:10000000]
# text = file.read()
words = text.split(' ')
# text = text.translate(str.maketrans('', '', digits))
# text = re.sub(' +', ' ', text)

# print('Entropia teorytyczna dla równego prawdopodobieństwa wszystkich znaków: ', calculateTheoriticalEntropy(), '\n')
# print('Entropia zerowego rzędu dla rzeczywistego tekstu: ', calculateEntropy(getProbs(text, 1)))
# print('Entropia pierwszego rzędu dla rzeczywistego tekstu: ', calculateEntropy(getProbs(text, 2)))
# print('Entropia drugiego rzędu dla rzeczywistego tekstu: ', calculateEntropy(getProbs(text, 3)), '\n')

# probs, conProbs = getConditionalProbability(text, 2)
# print('Entropia warunkowa pierwszego rzędu dla rzeczywistego tekstu: ', calculateConditionalEntropy(probs, conProbs))

print('Entropia zerowego rzędu dla rzeczywistego tekstu: ', calculateEntropy(getWordsProbs(words, 1)))

# print('Entropia pierwszego rzędu dla rzeczywistego tekstu: ', calculateEntropy(getProbs(text)))
# print('Entropia drugiego rzędu dla rzeczywistego tekstu: ', calculateEntropy(getProbs(text, 3)), '\n')




# print(getWordsProbability(words))
