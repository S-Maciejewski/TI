import random
import re
import operator
import numpy as np
from collections import OrderedDict
from string import digits

letters = ' abcdefghijklmnopqrstuvwxyz'


def getAvgLen(text):
    words = text.split(' ')
    return round(np.sum([len(word) for word in words]) / len(words), 2)


def getNextLetter(probs={}):
    return np.random.choice(list(probs.keys()), p=list(probs.values())) if bool(probs) else random.choice(letters)


def getLettersCount(text):
    return {letter: text.count(letter) for letter in letters}


def getProbabilities(text):
    lettersNum = len(text)
    count = getLettersCount(text)
    return {letter: count[letter] / lettersNum for letter in letters}


def getMostCommonLetters(number):
    lettersDict = getLettersCount(text)
    commonLetters = sorted(lettersDict.items(),
                           key=operator.itemgetter(1))[-number:]
    return [letter[0] for letter in reversed(commonLetters)]


def printProbs(probs):
    for key, value in sorted(probs.items(), key=operator.itemgetter(1), reverse=True):
        print(key, value)


def hasNumbers(ngram):
    return any(char.isdigit() for char in ngram)


def normalizeProbability(probs):
    sum1 = sum(list(probs.values()))
    for key in probs.keys():
        probs[key] /= sum1


def getProbs(text, n):
    probs = {}
    count = 0
    for i in range(len(text) - n + 1):
        ngram = text[i:i+n]
        if not hasNumbers(ngram):
            count += 1
            if tuple(ngram) in probs:
                probs[tuple(ngram)] += 1
            else:
                probs[tuple(ngram)] = 1
    for key in probs.keys():
        probs[key] /= count
    return probs


def getConditionalProbability(text, n):
    conditionalProbs = {}
    nGramPlusOneProbs = getProbs(text, n+1)
    nGramProbs = getProbs(text, n)
    for k in nGramProbs.keys():
        conditionalProbs[k] = {}
        for letter in letters:
            newKey = k + tuple(letter)
            if newKey in nGramPlusOneProbs.keys():
                conditionalProbs[k][letter] = nGramPlusOneProbs[newKey] / \
                    nGramProbs[k]
        normalizeProbability(conditionalProbs[k])
    return conditionalProbs


def generateTextOnMarkovChain(startingSequence, sourceText, n, length):
    probs = getConditionalProbability(sourceText, n)
    generatedText = startingSequence
    nextNgram = generatedText[-n:]
    for i in range(length):
        generatedText += getNextLetter(probs[tuple(nextNgram)])
        nextNgram = generatedText[-n:]
    return generatedText


# file = open('norm_wiki_sample.txt', 'r')
# file = open('norm_romeo_and_juliet.txt', 'r')
file = open('norm_hamlet.txt', 'r')
text = file.read()[:1000000]
text = text.translate(str.maketrans('', '', digits))  # usunięcie liczb
text = re.sub(' +', ' ', text)  # usunięcie wielokrotnych spacji


# 1.
print("\n1. Przybliżenie zerowego rzędu\n")
generatedText = ''.join([getNextLetter() for i in range(100000)])
print("Średnia długość słowa : ", getAvgLen(generatedText))

# 2.
print("\n\n2. Częstość liter\n")
printProbs(getProbabilities(text))
print("\nLitery najczęściej występujące w języku angielskim mają w alfabecie Morse'a najkrótsze sekwencje, w celu przyspieszenia nadawania wiadomości.")

# 3.
print("\n\n3. Przyblżenie pierwszego rzędu\n")
probs = getProbabilities(text)
generatedText = ''.join([getNextLetter(probs) for i in range(10000)])
print('Średnia długość słowa w losowym tekście z rzeczywistym prawdopodobieństwem : ',
      getAvgLen(generatedText))
print('\nŚrednia długość słowa w oryginalnym tekście : ', getAvgLen(text))
print('\nW przypadku generowania kolejnych liter tekstu z rzeczywistym prawdopodoboeństwem, średnia długość słowa jest bardzo podobna do średniej długości słowa w tekście oryginalnym.')

# 4.
print("\n\n4. Prawdopodobieństwo warunkowe liter\n")
commonLetters = getMostCommonLetters(2)
print('Dwia najczęściej występujące w tekście znaki to \'' +
      commonLetters[0] + '\' i \'' + commonLetters[1] + '\'')
condProbs = getConditionalProbability(text, 1)
for letter in commonLetters:
    print("\nPrawdopodopieństwo wystąpienia znaków po \'" + letter + "\' :\n")
    printProbs(condProbs[tuple(letter)])

# 5.
print("\n\n5. Przybliżenia na podstawie źródła Markova")

for i in [1, 3, 5]:
    print("\nPrzybliżenie " + str(i) + " rzędu: \n")
    generatedText = generateTextOnMarkovChain('probability', text, i, 2000)
    print(generatedText)
    print("\nŚrednia długość wyrazu: ", getAvgLen(generatedText))
