from bitarray import bitarray
from math import log2, ceil
import operator

letters = ' abcdefghijklmnopqrstuvwxyz0123456789'
decodeDict = {}
encodeDict = {}
codeLen = 0
encodedText = ''
text = ''


def getLettersCount():
    lettersDict = {letter: text.count(letter) for letter in letters}
    lettersDict = {key: value for key, value in lettersDict.items() if value != 0}
    return dict(sorted(lettersDict.items(), key=operator.itemgetter(1), reverse=True))


def create():
    letterFreq = getLettersCount()
    global codeLen
    codeLen = ceil(log2(len(letterFreq)))
    for i, key in enumerate(letterFreq.keys()):
        decodeDict[('{:0' + str(codeLen) + 'b}').format(i)] = key
        encodeDict[key] = ('{:0' + str(codeLen) + 'b}').format(i)


def readText(filename, signsNo=0):
    file = open(filename, 'r')
    global text
    text = file.read()[:signsNo] if signsNo != 0 else file.read()
    file.close()
    

def encode():
    enText = bitarray()
    for letter in text:
        enText += bitarray(encodeDict[letter])
        print(bitarray(encodeDict[letter]))
    global encodedText
    encodedText = enText
    


def decode():
    print(decodeDict)
    resultText = ''
    for i in range(0, len(encodedText), codeLen):
        print(encodedText[i:i+codeLen])
        resultText += decodeDict[encodedText[i:i+codeLen]]
    print(resultText)
    

def save():
    codeFile = open('code.txt', 'w+')
    codeFile.write(''.join(encodeDict.keys()))

    encodedFile = open('encoded.txt', 'w+b')
    encodedFile.write(encodedText.tobytes())

    encodedFile.close()
    codeFile.close()


def load():
    codeFile = open('code.txt', 'r')
    encodedFile = open('encoded.txt', 'r')


readText('norm_wiki_sample.txt', signsNo = 10)
print(text)
create()
encode()
decode()
save()