from bitarray import bitarray
from math import log2, ceil
import operator

letters = ' abcdefghijklmnopqrstuvwxyz0123456789'


def getLettersCount(text):
    lettersDict = {letter: text.count(letter) for letter in letters if letter in text}
    return dict(sorted(lettersDict.items(), key=operator.itemgetter(1), reverse=True))


def create(lettersFreq):
    decodeDict = {}
    encodeDict = {}
    codeLen = ceil(log2(len(lettersFreq)))
    for i, letter in enumerate(lettersFreq):
        decodeDict[('{:0' + str(codeLen) + 'b}').format(i)] = letter
        encodeDict[letter] = ('{:0' + str(codeLen) + 'b}').format(i)
    return encodeDict, decodeDict
    

def readText(filename, signsNo=0):
    file = open(filename, 'r')
    text = file.read()[:signsNo] if signsNo != 0 else file.read()
    file.close()
    return text
    

def encode(text, encodeDict):
    encodedText = bitarray()
    for letter in text:
        encodedText += bitarray(encodeDict[letter])

    # FIX ###########
    filling = (len(encodedText) + 3) % 8
    offsetLen = 8 - filling if filling != 0 else 0
    codeOffset = bitarray(bin(offsetLen)[2:].zfill(3))
    encodedText = codeOffset + encodedText
    #################

    return encodedText
    

def decode(encodedText, decodeDict):
    resultText = ''
    codeLen = len(list(decodeDict.keys())[0])

    # FIX ###########
    offsetLen = int(encodedText[:3].to01(), 2)
    for i in range(3, len(encodedText) - offsetLen, codeLen):
        resultText += decodeDict[encodedText[i:i+codeLen].to01()] 
    return resultText
    

def save(encodedText, encodeDict, encodedTextFilename = 'endcodedText.txt', codeFilename = 'code.txt'):
    encodedFile = open(encodedTextFilename, 'w+b')
    encodedFile.write(encodedText.tobytes())
    encodedFile.close()

    codeFile = open(codeFilename, 'w+')
    codeFile.write(''.join(encodeDict.keys()))
    codeFile.close()


def load(encodedTextFilename, codeFilename):
    encodedFile = open(encodedTextFilename, 'rb')
    encodedText = bitarray()
    encodedText.frombytes(encodedFile.read())
    encodedFile.close()

    codeFile = open(codeFilename, 'r')
    encodeDict, decodeDict = create(list(codeFile.read()))
    codeFile.close()

    return encodedText, encodeDict, decodeDict


def encodingIsCorrect():
    text = 'text to verify correctness of encoding and decoding algorithm'
    encodeDict, decodeDict = create(getLettersCount(text))
    encodedText = encode(text, encodeDict)
    originalText = decode(encodedText, decodeDict)
    return text == originalText




if (encodingIsCorrect()):
    print('Encoding and decoding algorithm is correct\n')
else:
    print('Encoding and decoding algorithm is NOT correct\n')  



text = readText('norm_wiki_sample.txt', signsNo = 0)
# print(text)

encodeDict, decodeDict = create(getLettersCount(text))
encodedText = encode(text, encodeDict)
save(encodedText, encodeDict, 'encodedText.txt', 'code.txt')

encodedText, encodeDict, decodeDict = load('encodedText.txt', 'code.txt')
originalText = decode(encodedText, decodeDict)
# print(originalText)



