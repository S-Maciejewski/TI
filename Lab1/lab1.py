import random
import operator

letters = ' abcdefghijklmnopqrstuvwxyz'


def getRandLetter():
    return random.choice(letters)


def getAvgLen(text):
    splitText = text.split(' ')
    lenSum = 0
    for word in splitText:
        lenSum += len(word)
    return round(lenSum / len(splitText), 2)


def getWeightedRandomLetter(probs):
    randVal = random.random()
    total = 0
    for k, v in probs.items():
        total += v
        if randVal <= total:
            return k


def getLettersDict(text):
    lettersDict = {}
    for letter in letters:
        lettersDict[letter] = text.count(letter)
    return lettersDict


def getProbabilities(text):
    probs = {}
    lettersNumber = len(text)
    lettersDict = getLettersDict(text)
    for letter in letters:
        probs[letter] = lettersDict[letter] / lettersNumber
    return probs


def getPairsProbability(text):
    pairsProbability = {}
    pairsNumber = len(text) - 1
    for letter1 in letters:
        for letter2 in letters:
            pairsProbability[(letter1, letter2)] = text.count(letter1+letter2) / pairsNumber
    return pairsProbability


def getConditionalProbabilityOfLetters(text):
    conditionalProbs = {}
    pairsProbs = getPairsProbability(text)
    lettersProbs = getProbabilities(text)
    for l1 in letters:
        for l2 in letters:
            conditionalProbs[(l1, l2)] = pairsProbs[(l2, l1)] / lettersProbs[l2]
    return conditionalProbs

def getConditionalProbability(text):
    conditionalProbs = getConditionalProbabilityOfLetters(text)
    lettersDict = getLettersDict(text)
    commonLetters = sorted(lettersDict.items(), key=operator.itemgetter(1))[-3:-1]
    print(sortedLettersDict)
    


# # 1.
# textLength = 10000
# text = ''
# for i in range(textLength):
#     text += getRandLetter()

# print(text)
# print(getAvgLen(text))


# 2.
file = open('norm_hamlet.txt', 'r')
text = file.read()
# print(text)
print('Wartosci prawdopodobienstwa dla wszystkich liter:\n', getProbabilities(text))
print('Srednia dlugosc slowa w Hamlecie: ', getAvgLen(text))

getConditionalProbability(text)


# 3.
probs = getProbabilities(text)
textLength = 10000
generatedText = ''
for i in range(textLength):
    generatedText += getWeightedRandomLetter(probs)
# print('Tekst z losowymi literami z rzeczywistym prawdopodobienstwem: ', generatedText)
print('Srednia dlugosc slowa w losowym teksice z rzeczywistym prawdopodobienstwem', getAvgLen(generatedText))
