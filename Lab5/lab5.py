from bitarray import bitarray
from math import log2, ceil, log
import operator
from queue import PriorityQueue
from numpy import array, mean, min

letters = ' abcdefghijklmnopqrstuvwxyz0123456789'

class Tree(object):
    def __init__(self, label = None, prob = None, treeL = None, treeR = None): 
        self.left = treeL
        self.right = treeR
        self.label = label if not treeL and not treeR else treeL.label + treeR.label
        self.prob = prob if not treeL and not treeR else treeL.prob + treeR.prob
        self.isLeaf = not treeL and not treeR

    def __repr__(self):
        if self.isLeaf:
            return "\"" + str(self.label) + "\": " + str(self.prob)
        else:
            return "\"" + str(self.label) + "\" : {" + str(self.left) + "," + str(self.right) + "}"

class TreeList(object):
    def __init__(self, list):
        self.treelist = sorted(list, key = lambda x: x.prob)
        # self.treelist = sorted(list, key = lambda x: (x.prob, 0 if x.isLeaf else 1))

    def append(self, tree):
        self.treelist.append(tree)
        self.treelist.sort(key = lambda x: x.prob)
        # self.treelist.sort(key = lambda x: (x.prob, 0 if x.isLeaf else 1))

    def __len__(self):
        return len(self.treelist)

    def pop(self, l):
        return self.treelist.pop(l)

    def __getitem__(self, index):
         return self.treelist[index]

    def __str__(self):
        return ' '.join([str(tree) for tree in self.treelist])

    def __repr__(self):
        return self.treelist


def getLettersProbs(text):
    textLength = len(text)
    lettersDict = {letter: text.count(letter)/textLength for letter in letters if letter in text}
    return dict(sorted(lettersDict.items(), key=operator.itemgetter(1), reverse=False))


def calculateEntropy(probs):
    entropy = 0
    for prob in probs.values():
        entropy += prob * log(prob, 2)
    return -entropy


def createKeyDictRecursively(tree, keyDict, key):
    if tree.isLeaf:
        keyDict[tree.label] = key
        return
    else:
        key += '0'
        createKeyDictRecursively(tree.left, keyDict, key)
        key = key[:-1] + '1'
        createKeyDictRecursively(tree.right, keyDict, key)
        key = key[:-1]


def prepareTree(lettersProbs):
    treeList = TreeList([Tree(key, value) for key, value in lettersProbs.items()])
    while(len(treeList) != 1):
        treeList.append(Tree(treeL = treeList.pop(0), treeR = treeList.pop(0)))
    return treeList


def create(lettersProbs, printJSON=False):
    encodeDict = {}
    tree = prepareTree(lettersProbs)
    treeInJSON = "{" + str(tree) + "}"
    if printJSON: print(treeInJSON)
    createKeyDictRecursively(tree[0], encodeDict, '')
    decodeDict = {value: key for key, value in encodeDict.items()}
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
    encodedText.fill()
    #################

    return encodedText
    

def decode(encodedText, decodeDict):
    resultText = ''
    minCodeLen = min([len(key) for key in decodeDict.keys()])

    # FIX ###########
    offsetLen = int(encodedText[:3].to01(), 2)
    position = 3
    while position < len(encodedText) - offsetLen:
        codeLen = minCodeLen
        while True:
            code = encodedText[position:position+codeLen].to01()
            if code in decodeDict.keys(): break
            codeLen += 1
        resultText += decodeDict[code]
        position += codeLen

    return resultText
    

def save(encodedText, encodeDict, encodedTextFilename = 'endcodedText.txt', codeFilename = 'code.txt'):
    encodedFile = open(encodedTextFilename, 'w+b')
    encodedFile.write(encodedText.tobytes())
    encodedFile.close()

    codeFile = open(codeFilename, 'w+')
    for key, value in encodeDict.items():
        codeFile.write(key + value + "\n")

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
    text = 'text to verify correctness of encoding and decoding algorithm'
    encodeDict, decodeDict = create(getLettersProbs(text))
    encodedText = encode(text, encodeDict)
    originalText = decode(encodedText, decodeDict)
    if text == originalText:
        print('Encoding and decoding algorithm is correct\n')
    else:
        print('Encoding and decoding algorithm is NOT correct\n')  


# encodingIsCorrect()

text = readText('norm_wiki_sample.txt', signsNo = 0)

lettersProbs = getLettersProbs(text)
entropy = calculateEntropy(lettersProbs)
print('Entropia (znaki): ', entropy)
print('\nŚrednia długość słowa kodowego: 6 bitów')
print('Efektywność kodowania z ostatnich zajęć to', str(entropy/6*100))

lettersProbs = getLettersProbs(text)
encodeDict, decodeDict = create(lettersProbs)
# print('\n', encodeDict, '\n\n', decodeDict)

m = sum([len(key) * lettersProbs[v] for v, key in encodeDict.items()])
print("\nŚrednia długość słowa kodowego:", m, 'bitów')
print('Efektywność kodowania to', str(entropy/m * 100))

encodedText = encode(text, encodeDict)
save(encodedText, encodeDict, 'encodedText.txt', 'code.txt')

encodedText, encodeDict, decodeDict = load('encodedText.txt', 'code.txt')
# print('\n', encodeDict, '\n\n', decodeDict)
originalText = decode(encodedText, decodeDict)
# print(originalText)



