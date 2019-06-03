from bitarray import bitarray
from math import log2, ceil, log
import operator
from queue import PriorityQueue
from numpy import array, mean, min

letters = ' abcdefghijklmnopqrstuvwxyz0123456789'


def create(text):
    output = []
    encodeDictChars = {letter: i for i, letter in enumerate(
        letters) if letter in text}
    p = text[0]
    dictLen = len(encodeDictChars)
    for letter in text[1:]:
        c = letter
        if (p+c in encodeDictChars):
            p = p + c
        else:
            dictLen += 1
            encodeDictChars[p+c] = dictLen
            output.append(encodeDictChars[p])
            p = c
    output.append(encodeDictChars[p])

    decodeDict = {}
    encodeDict = {}
    codeLen = ceil(log2(len(encodeDictChars)))

    for i, letter in enumerate(encodeDictChars.values()):
        decodeDict[('{:0' + str(codeLen) + 'b}').format(i)] = letter
        encodeDict[letter] = ('{:0' + str(codeLen) + 'b}').format(i)

    dictToSave = {letter: code for letter,
                  code in encodeDictChars.items() if len(letter) == 1}

    return encodeDict, dictToSave, output, codeLen


def readText(filename, signsNo=0):
    file = open(filename, 'r')
    text = file.read()[:signsNo] if signsNo != 0 else file.read()
    file.close()
    return text


def encode(output, encodeDict):
    encodedText = bitarray()
    for number in output:
        encodedText += bitarray(encodeDict[number])

    # FIX ###########
    filling = (len(encodedText) + 3) % 8
    offsetLen = 8 - filling if filling != 0 else 0
    codeOffset = bitarray(bin(offsetLen)[2:].zfill(3))
    encodedText = codeOffset + encodedText
    #################

    return encodedText


def decode(encodedText, codeLen, dictFromSave):

    output = []

    textLen = len(encodedText)
    position = 3
    while (position < textLen):
        code = encodedText[position:position+codeLen]
        output.append(int(code.to01(), 2))
        position += codeLen

    print(output)

    old = output[0]

    for num in output[1:]:
        new = num
        if (new not in dictFromSave):
            s = dictFromSave

#     OLD = first input code


# 3    output translation of OLD
# 4    WHILE not end of input stream
# 5        NEW = next input code
# 6        IF NEW is not in the string table
# 7               S = translation of OLD
# 8               S = S + C
# 9       ELSE
# 10              S = translation of NEW
# 11       output S
# 12       C = first character of S
# 13       OLD + C to the string table
# 14       OLD = NEW
# 15   END WHILE

# encodeDictChars = {letter: i for i, letter in enumerate(letters) if letter in text}
# p = text[0]
# dictLen = len(encodeDictChars)
# for letter in text[1:]:
#     c = letter
#     if (p+c in encodeDictChars):
#         p = p + c
#     else:
#         dictLen += 1
#         encodeDictChars[p+c] = dictLen
#         output.append(encodeDictChars[p])
#         p = c
# output.append(encodeDictChars[p])

# decodeDict = {}
# encodeDict = {}
# codeLen = ceil(log2(len(encodeDictChars)))

# for i, letter in enumerate(encodeDictChars.values()):
#     decodeDict[('{:0' + str(codeLen) + 'b}').format(i)] = letter
#     encodeDict[letter] = ('{:0' + str(codeLen) + 'b}').format(i)

# return encodeDict, decodeDict, output
# pass


def save(encodedText, dictToSave, codeLen, encodedTextFilename='endcodedText.txt', codeFilename='code.txt'):
    encodedFile = open(encodedTextFilename, 'w+b')
    encodedFile.write(encodedText.tobytes())
    encodedFile.close()

    codeFile = open(encodedTextFilename, 'w+')
    codeFile.write(str(ceil(log2(len(dictToSave)))) + '\n')
    for key, value in dictToSave.items():
        codeFile.write(str(value) + ' ' + key + "\n")

    codeFile.close()


def load(encodedTextFilename, codeFilename):
    encodedFile = open(encodedTextFilename, 'rb')
    encodedText = bitarray()
    encodedText.frombytes(encodedFile.read())
    encodedFile.close()

    encodeDict = {}
    codeFile = open(codeFilename, 'r')
    f = codeFile.readlines()
    for line in f:
        s = line.replace('\n', '')
        encodeDict[s[0]] = s[1:]
    decodeDict = {value: key for key, value in encodeDict.items()}
    codeFile.close()

    return encodedText, encodeDict, decodeDict


def encodingIsCorrect():
    # text = 'text to verify correctness of encoding and decoding algorithm'
    # encodeDict, decodeDict = create(getLettersProbs(text))
    # encodedText = encode(text, encodeDict)
    # originalText = decode(encodedText, decodeDict)
    # if text == originalText:
    #     print('Encoding and decoding algorithm is correct\n')
    # else:
    #     print('Encoding and decoding algorithm is NOT correct\n')
    pass


# text = readText('norm_wiki_sample.txt', 10000)
text = readText('sample2.txt', 10000)

encodeDict, dictToSave, output, codeLen = create(text)

encodedText = encode(output, encodeDict)

# decode(encodedText, codeLen)

print(encodedText)

save(encodedText, dictToSave, codeLen)

# print(text)
# print(output)
# print(encodeDict)
print('output length =', len(output), '\ndict length =',
      len(encodeDict), '\ntext length =', len(text))
