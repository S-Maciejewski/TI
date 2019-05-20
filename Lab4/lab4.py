from bitarray import bitarray
from math import log2, ceil
import operator

letters = ' abcdefghijklmnopqrstuvwxyz0123456789'
decodeDict = {}
encodeDict = {}
encodedText = ''


def getLettersCount(text):
    lettersDict = {letter: text.count(letter) for letter in letters}
    lettersDict = {key: value for key, value in lettersDict.items() if value != 0}
    return dict(sorted(lettersDict.items(), key=operator.itemgetter(1), reverse=True))


def create(text):
    lettersFreq = getLettersCount(text)
    codeLen = ceil(log2(len(lettersFreq)))
    for i, key in enumerate(lettersFreq.keys()):
        decodeDict[('{:0' + str(codeLen) + 'b}').format(i)] = key
        encodeDict[key] = ('{:0' + str(codeLen) + 'b}').format(i)
    return codeLen, encodeDict, decodeDict


def readText(filename, signsNo=0):
    file = open(filename, 'r')
    text = file.read()[:signsNo] if signsNo != 0 else file.read()
    file.close()
    return text
    

def encode(text, encodeDict):
    encodedText = bitarray()
    for letter in text:
        encodedText += bitarray(encodeDict[letter])
    return encodedText
    

def decode(encodedText, decodeDict):
    resultText = ''
    for i in range(0, len(encodedText), codeLen):
        resultText += decodeDict[encodedText[i:i+codeLen].to01()]
    return resultText
    

def save(encodedText, encodeDict, encodedTextFilename = 'endcodedText.txt', codeFilename = 'code.txt'):
    encodedFile = open(encodedTextFilename, 'w+b')
    codeFile = open(codeFilename, 'w+')

    encodedFile.write(encodedText.tobytes())
    codeFile.write(''.join(encodeDict.keys()))

    encodedFile.close()
    codeFile.close()


def load():
    codeFile = open('code.txt', 'r')
    encodedFile = open('encoded.txt', 'r')


text = readText('norm_wiki_sample.txt', signsNo = 10000)
print(text)

codeLen, encodeDict, decodeDict = create(text)

encodedText = encode(text, encodeDict)

save(encodedText, encodeDict, 'encodedText.txt', 'code.txt')

originalText = decode(encodedText, decodeDict)
print(originalText)
