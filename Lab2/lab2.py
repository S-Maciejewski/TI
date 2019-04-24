import random
import re
import operator
import numpy as np
from collections import OrderedDict
from string import digits


file = open('norm_wiki_sample.txt', 'r')
# file = open('norm_romeo_and_juliet.txt', 'r')
# file = open('norm_hamlet.txt', 'r')
text = file.read()[:3000000]
text = text.translate(str.maketrans('', '', digits))    #usunięcie liczb
text = re.sub(' +', ' ', text)                          #usunięcie wielokrotnych spacji 

words = text.split(' ')


def getNextWord(probs):
    return np.random.choice(list(probs.keys()), p=list(probs.values()))


def getWordsCount():
    return {word: words.count(word) for word in words}

def getWordsProbability():
    probs = {}
    count = len(words)
    for word in words:
        if word in probs:
            probs[word] += 1 
        else:
            probs[word] = 1
    for key in probs.keys():
        probs[key] /= count
    return probs


def printProbs(probs):
    for key, value in sorted(probs.items(), key=operator.itemgetter(1), reverse=True):
        print(key, value)


def normalizeProbability(probs):
    sum1 = sum(list(probs.values()))
    for key in probs.keys():
        probs[key] /= sum1


def getProbs(n):
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


def getConditionalProbability(n):
    conditionalProbs = {}
    nGramPlusOneProbs = getProbs(n+1)
    nGramProbs = getProbs(n)
    for key in nGramPlusOneProbs.keys():
        main = tuple(key[:n])
        last = key[-1]
        if not main in conditionalProbs:
            conditionalProbs[main] = {}
        conditionalProbs[main][last] = nGramPlusOneProbs[key] / nGramProbs[main]
    for key in conditionalProbs.keys():
        normalizeProbability(conditionalProbs[key])
    return conditionalProbs


def generateTextOnMarkovChain(n, wordsNumber, startWords=[]):
    ngram = startWords if len(startWords) != 0 else [getNextWord(getWordsProbability())]
    while len(ngram) < n:
        probs = getConditionalProbability(len(ngram))
        ngram.append(getNextWord(probs[tuple(ngram)]))

    probs = getConditionalProbability(n)
    generatedText = ' '.join(str(word) for word in ngram)
    
    for i in range(wordsNumber):
        nextWord = getNextWord(probs[tuple(ngram)])
        generatedText += ' ' + nextWord
        ngram = ngram[1:]
        ngram.append(nextWord)

    print(generatedText)




# #1.
wordsProb = getWordsProbability()
normalizeProbability(wordsProb)
wordsSorted = sorted(wordsProb.items(), key=operator.itemgetter(1))
for k, v in wordsSorted: 
    if v > 0.0004:
        print(k, v)
print("\n30 tysięcy najpopularniejszych słów stanowi", round(np.sum(list(OrderedDict(wordsSorted).values())[-30000:])*100, 2), "% wszystkich słów")
print("\n6 tysięcy najpopularniejszych słów stanowi", round(np.sum(list(OrderedDict(wordsSorted).values())[-6000:])*100, 2), "% wszystkich słów")


# #2.
print('\n\nPrzybliżenie pierwszego rzędu\n')
generatedText = ' '.join([getNextWord(wordsProb) for i in range(40)])
print(generatedText)


# 3
print('\n\nPrzybliżenie na podstawie źródła Markowa 1 rzędu\n')
generateTextOnMarkovChain(1, 100)

print('\n\nPrzybliżenie na podstawie źródła Markowa 2 rzędu\n')
generateTextOnMarkovChain(2, 100)

print('\n\nPrzybliżenie na podstawie źródła Markowa 2 rzędu z wyrazem początkowym\n')
generateTextOnMarkovChain(2, 100, ['probability'])


