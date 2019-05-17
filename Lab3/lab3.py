import random
import math
import re
import operator
import numpy as np
from collections import OrderedDict
from string import digits

letters = ' abcdefghijklmnopqrstuvwxyz0123456789'


def getProbs(bag, n):
    probs = {}
    count = len(bag) - n + 1
    for i in range(count):
        ngram = bag[i:i+n]
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


def calculateTheoriticalEntropy():
    entropy = 0
    prob = 1/len(letters)
    for i in range(len(letters)):
        entropy += prob * math.log(prob, 2)
    return -entropy


def calculateEntropy(probs):
    entropy = 0
    for prob in probs.values():
        entropy += prob * math.log(prob, 2)
    return -entropy


def calculateConditionalEntropy(probs, conditionalProbs):
    entropy = 0
    for key, value in conditionalProbs.items():
        for key2, prob in value.items():
            entropy += probs[key + tuple([key2])] * math.log(prob, 2)
    return -entropy
    


def normalizeProbability(probs):
    sum1 = sum(list(probs.values()))
    for key in probs.keys():
        probs[key] /= sum1


def getConditionalProbability(text, n):
    conditionalProbs = {}
    nGramPlusOneProbs = getProbs(text, n+1)
    nGramProbs = getProbs(text, n)

    for key in nGramPlusOneProbs.keys():
        if key[:-1] not in conditionalProbs:
            conditionalProbs[key[:-1]] = {}
        conditionalProbs[key[:-1]][key[-1]] = nGramPlusOneProbs[key] / nGramProbs[key[:-1]]

    for key in conditionalProbs:
        normalizeProbability(conditionalProbs[key])
    
    return nGramPlusOneProbs, conditionalProbs


def showEntropyForFile(file, language):
    file = open(file, 'r')
    text = file.read()[:10000000]
    words = text.split(' ')

    print(language)
    # print('Entropia (znaki): ', calculateEntropy(getProbs(text, 1)))
    # print('Entropia (słowa): ', calculateEntropy(getProbs(words, 1)), '\n')

    # probs, conProbs = getConditionalProbability(text, 1)
    # print('Entropia warunkowa 1 rzędu (znaki): ', calculateConditionalEntropy(probs, conProbs))
    # probs, conProbs = getConditionalProbability(text, 2)
    # print('Entropia warunkowa 2 rzędu (znaki): ', calculateConditionalEntropy(probs, conProbs))
    # probs, conProbs = getConditionalProbability(text, 3)
    # print('Entropia warunkowa 3 rzędu (znaki): ', calculateConditionalEntropy(probs, conProbs), '\n')

    probs, conProbs = getConditionalProbability(words, 1)
    print('Entropia warunkowa 1 rzędu (słowa): ', calculateConditionalEntropy(probs, conProbs))
    probs, conProbs = getConditionalProbability(words, 2)
    print('Entropia warunkowa 2 rzędu (słowa): ', calculateConditionalEntropy(probs, conProbs))
    probs, conProbs = getConditionalProbability(words, 3)
    print('Entropia warunkowa 3 rzędu (słowa): ', calculateConditionalEntropy(probs, conProbs))
    print()


showEntropyForFile('norm_wiki_en.txt', 'JĘZYK ANGIELSKI')
showEntropyForFile('norm_wiki_la.txt', 'JĘZYK ŁACIŃSKI')
showEntropyForFile('norm_wiki_eo.txt', 'JĘZYK ESPERANTO')
showEntropyForFile('norm_wiki_et.txt', 'JĘZYK ESTOŃSKI')
showEntropyForFile('norm_wiki_ht.txt', 'JĘZYK HAITAŃSKI')
showEntropyForFile('norm_wiki_nv.txt', 'JĘZYK NAVAHO')
showEntropyForFile('norm_wiki_so.txt', 'JĘZYK SOMALIJSKI')

showEntropyForFile('sample0.txt', 'SAMPLE 0')
showEntropyForFile('sample1.txt', 'SAMPLE 1')
showEntropyForFile('sample2.txt', 'SAMPLE 2')
showEntropyForFile('sample3.txt', 'SAMPLE 3')
showEntropyForFile('sample4.txt', 'SAMPLE 4')
showEntropyForFile('sample5.txt', 'SAMPLE 5')



# print(getWordsProbability(words))
