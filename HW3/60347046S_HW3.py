from collections import defaultdict
import math
import sys
import codecs
from functools import reduce
import os

temp_list = []
for dirPath, dirNames, fileNames in os.walk('./TrainDocSet/SPLIT_DOC_WDID_NEW/'):
    for f in fileNames:
        temp_list.append(os.path.join(dirPath, f))
document_filenames = {i:f for i,f in enumerate(temp_list)}

N = len(document_filenames)
dictionary = set()
postings = defaultdict(dict)
document_frequency = defaultdict(int)
length = defaultdict(float)

characters = " .,!#$%^&*();:\n\t\\\"?!{}[]<>"

def main():
    initialize_terms_and_postings()
    initialize_document_frequencies()
    initialize_lengths()
    simSum = 0.0
    lineNum = 0
    mAP = 0.0
    queryList = [path[2] for path in os.walk('./QueryTrainSet/QUERY_WDID_NEW/')][0]
    for fileName in queryList:
        with codecs.open("./QueryTrainSet/QUERY_WDID_NEW/" + str(fileName),'r',encoding='utf-8') as f:
            for line in f:
                lineValue = file_sim(line)
                if lineValue == 0.0:
                    continue
                lineNum += 1
                simSum += lineValue
            mAP += simSum/lineNum
    print(mAP/16)
    

def initialize_terms_and_postings():
    global dictionary, postings
    for id in document_filenames:
        f = codecs.open(document_filenames[id],'r',encoding='utf-8')
        document = f.read()
        f.close()
        terms = tokenize(document)
        unique_terms = set(terms)
        dictionary = dictionary.union(unique_terms)
        for term in unique_terms:
            postings[term][id] = terms.count(term)

def tokenize(document):
    terms = document.lower().split()
    return [term.strip(characters) for term in terms]

def initialize_document_frequencies():
    global document_frequency
    for term in dictionary:
        document_frequency[term] = len(postings[term])

def initialize_lengths():
    global length
    for id in document_filenames:
        l = 0
        for term in dictionary:
            l += imp(term,id)**2
        length[id] = math.sqrt(l)

def imp(term,id):
    if id in postings[term]:
        return postings[term][id]*inverse_document_frequency(term)
    else:
        return 0.0

def inverse_document_frequency(term):
    if term in dictionary:
        return math.log(N/document_frequency[term],2)
    else:
        return 0.0

def file_sim(inputStr):
    topNum = 10
    query = tokenize(inputStr)
    if query == []:
        sys.exit()
    relevant_document_ids = intersection(
            [set(postings[term].keys()) for term in query])
    if not relevant_document_ids:
        return 0.0
    else:
        scores = sorted([similarity(query,id)
                         for id in relevant_document_ids],
                         reverse=True)
        sumScore = 0.0
        for score in scores[:topNum]:
            sumScore += score
        return sumScore/topNum

def intersection(sets):
    return reduce(set.intersection, [s for s in sets])

def similarity(query,id):
    similarity = 0.0
    for term in query:
        if term in dictionary:
            similarity += inverse_document_frequency(term)*imp(term,id)
    similarity = similarity / length[id]
    return similarity

if __name__ == "__main__":
    main()