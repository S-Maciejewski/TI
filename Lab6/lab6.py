from bitarray import bitarray
from math import log2, ceil, log
import operator
from queue import PriorityQueue
from numpy import array, mean, min
from operator import itemgetter    

def create(text, maxDictSize=0):
    output = []
    encodeDictChars = {letter: i for i, letter in enumerate(list(set(text))) }
    dictToSave = dict(encodeDictChars)

    dictLen = len(encodeDictChars)
    p = text[0]
    if maxDictSize == 0:    # sprawdzenie tutaj, żeby nie sprawdzać tego warunku miliardy razy w pętli
        for letter in text[1:]:
            c = letter
            p_c = sumTuples(p, c)
            if p_c in encodeDictChars:
                p = p_c
            else:
                encodeDictChars[p_c] = dictLen
                dictLen += 1
                output.append(encodeDictChars[p])
                p = c
    else:
        dictIsFull = False if len(encodeDictChars) < maxDictSize else True
        for letter in text[1:]:
            c = letter
            p_c = sumTuples(p, c)
            if p_c in encodeDictChars:
                p = p_c
            else:
                if not dictIsFull:
                    encodeDictChars[p_c] = dictLen
                    dictLen += 1
                    if dictLen == maxDictSize:
                        dictIsFull = True
                output.append(encodeDictChars[p])
                p = c
    output.append(encodeDictChars[p])

    encodeDict = {}
    codeLen = ceil(log2(len(encodeDictChars)))
    for num in encodeDictChars.values():
        encodeDict[num] = ('{:0' + str(codeLen) + 'b}').format(num)

    return encodeDict, dictToSave, output, codeLen


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


def sumTuples(t1, t2):
    t1 = t1 if isinstance(t1, tuple) else (t1,)
    t2 = t2 if isinstance(t2, tuple) else (t2,)
    return t1 + t2


def decode(encodedText, codeLen, dictFromSave):
    textLen = len(encodedText)
    output = [int(code.to01(), 2) for code in [encodedText[i:i+codeLen] for i in range(3, textLen, codeLen)]]

    count = len(dictFromSave)

    old = output[0]
    s = dictFromSave[old]
    c = s
    result = [s]
    for num in output[1:]:
        new = num
        s = sumTuples(dictFromSave[old], c) if (new not in dictFromSave) else dictFromSave[new]
        result += list(s) if isinstance(s, tuple) else [s]
        c = s[0] if isinstance(s, tuple) else s
        dictFromSave[count] = sumTuples(dictFromSave[old], c)
        count += 1
        old = new

    return bytes(result)


def save(encodedText, dictToSave, codeLen, encodedTextFilename='endcodedText.txt', codeFilename='code.txt'):
    encodedFile = open(encodedTextFilename, 'w+b')
    encodedFile.write(encodedText.tobytes())
    encodedFile.close()

    codeFile = open(codeFilename, 'w+b')
    codeFile.write(bytes([codeLen]))
    for (t, n) in sorted(dictToSave.items(), key = itemgetter(1), reverse = False):
        codeFile.write(bytes([t]))
    codeFile.close()


def load(encodedTextFilename='endcodedText.txt', codeFilename='code.txt'):
    encodedFile = open(encodedTextFilename, 'rb')
    encodedText = bitarray()
    encodedText.frombytes(encodedFile.read())
    
    # remove unnecessary bits at the end
    for i in range(int(encodedText[:3].to01(), 2)):
        encodedText.pop()
    encodedFile.close()

    codeFile = open(codeFilename, 'rb')
    chars = codeFile.read()
    codeLen = chars[0]
    decodeDict = {i: sign for i, sign in enumerate(chars[1:]) }
    codeFile.close()

    return encodedText, decodeDict, codeLen


def readText(filename, signsNo=0):
    file = open(filename, 'rb')
    text = file.read()[:signsNo] if signsNo != 0 else file.read()
    file.close()
    return text


# text = readText('sample.txt')
# text = readText('norm_wiki_sample/norm_wiki_sample.txt')
# encodeDict, dictToSave, output, codeLen = create(text, 4096)
# print(len(encodeDict))
# encodedText = encode(output, encodeDict)
# save(encodedText, dictToSave, codeLen, 'norm_wiki_sample/2^12/encoded.txt', 'norm_wiki_sample/full/code.txt')
# loadedText, decodeDict, loadedCodeLen = load('norm_wiki_sample/2^12/encoded.txt', 'norm_wiki_sample/full/code.txt')
# decodedText = decode(loadedText, loadedCodeLen, decodeDict)


def run(folder, fileExtension):
    text = readText(folder + '/' + folder + '.' + fileExtension)
    print("Size before compression:", len(text), 'bytes\n')

    for size, subfolder in [(0, 'full'), (4096, '2^12'), (262144, '2^18')]:
        fullEncodedFilePath = folder + '/' + subfolder + '/encoded.txt'
        codeFilePath = folder + '/' + subfolder + '/code.txt'

        encodeDict, dictToSave, output, codeLen = create(text, size)
        encodedText = encode(output, encodeDict)
        save(encodedText, dictToSave, codeLen, fullEncodedFilePath, codeFilePath)

        loadedText, decodeDict, loadedCodeLen = load(fullEncodedFilePath, codeFilePath)
        decodedText = decode(loadedText, loadedCodeLen, decodeDict)

        if(text == decodedText):
            print('Dictionary size:', subfolder)
            print('Compression successful!')
            print("Size after compression:", ceil(len(encodedText)/8), 'bytes\n')

# run('norm_wiki_sample', 'txt')
# run('wiki_sample', 'txt')
run('lena', 'bmp')