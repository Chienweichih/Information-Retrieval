from collections import defaultdict
import math
import sys
import codecs
from functools import reduce
import os

open('ResultsTrainSet.txt','w')

temp_list = []
for dirPath, dirNames, fileNames in os.walk('./TrainDocSet/SPLIT_DOC_WDID_NEW/'):
    for f in fileNames:
        temp_list.append(os.path.join(dirPath, f))
document_filenames = {i:f for i,f in enumerate(temp_list)}

temp_list2 = []
for dirPath, dirNames, fileNames in os.walk('./QueryTrainSet/QUERY_WDID_NEW/'):
    for f in fileNames:
        temp_list2.append(os.path.join(dirPath, f))
Query_filenames = {i:f for i,f in enumerate(temp_list2)}



N = len(document_filenames)
dictionary = set()
dictionary2 = set()
postings = defaultdict(dict)
Weight = defaultdict(dict)
document_frequency = defaultdict(int)
length = defaultdict(float)
Score = [[["" , 0.0] for i in range(0,N)] for i in range(0,16)]



def main():
    global Score
    index = 0
    initialize_terms_and_postings()
    initialize_weight()
    initialize_lengths()
    for id in Query_filenames:
        Q = Query_filenames[id]
        index = index + 1
        index2 = 0

        print("index1: " + str(index))
        for id in document_filenames:
            index2 = index2 + 1
            #print(str(Weight))
            S = similarity(Q,document_filenames[id])
            Score[index-1][index2-1] = [document_filenames[id].strip("./TrainDocSet/SPLIT_DOC_WDID_NEW/") , S]
            if S > 1:
                print("F")
            print("index1: " + str(index) + "; index2: " + str(index2) + " S: " + str(S))

#            if index2 == 5:
#                break
   
        document_RANK = sorted(Score[index-1],key = lambda x : x[1],reverse=True)
        with open("ResultsTrainSet.txt",'a') as output:
            output.write("Query " + str(index) + "      " + Q.strip("./QueryTrainSet/QUERY_WDID_NEW/") + " " +str(N) + "\n")
            for i in range(0 , N):
                output.write(document_RANK[i][0] + "\n")
        
    print("complete")


    
def initialize_terms_and_postings():
    global dictionary,dictionary2,postings
    for id in document_filenames:
        f = codecs.open(document_filenames[id],'r', encoding = 'UTF-8')
        for a in range(0,3):
            f.readline()
        document = f.read()
        f.close()
        terms = tokenize(document)
        unique_terms = set(terms)
        unique_terms.remove("-1")
        dictionary = dictionary.union(unique_terms)
        dictionary2 = dictionary.union(unique_terms)
        for term in unique_terms:
            postings[term][document_filenames[id]] = terms.count(term)
            document_frequency[term] += 1

            
    for id in Query_filenames:      
        f = codecs.open(Query_filenames[id],'r', encoding = 'UTF-8')
        Query = f.read()
        f.close()
        terms = tokenize(Query)
        unique_terms2 = set(terms)
        unique_terms2.remove("-1")
        dictionary = dictionary.union(unique_terms2)
        for term in unique_terms2:
            postings[term][Query_filenames[id]] = terms.count(term)



        


def tokenize(document):
    terms = document.split()
    return [term for term in terms]



def initialize_weight():
    for term in dictionary:
        for id in document_filenames:
            if document_filenames[id] in postings[term]:
                Weight[term][document_filenames[id]] = (math.log(postings[term][document_filenames[id]],2)+1)*inverse_document_frequency(term)
        for id in Query_filenames:
            if Query_filenames[id] in postings[term]:
                Weight[term][Query_filenames[id]] = (math.log(postings[term][Query_filenames[id]],2)+1)*inverse_document_frequency(term)


def inverse_document_frequency(term):
    if term in dictionary2:
        return math.log(N/document_frequency[term],2)
    else:
        return 0.0



def initialize_lengths():
    global length
    for id in document_filenames:
        l = 0
        for term in dictionary:
            if document_filenames[id] in Weight[term]:
                l += (Weight[term][document_filenames[id]])**2
        length[id] = math.sqrt(l)

    
    for id in Query_filenames:
        l = 0
        for term in dictionary:
            if Query_filenames[id] in Weight[term]:
                l += (Weight[term][Query_filenames[id]])**2
        length[id] = math.sqrt(l)
 


    

def similarity(Q,document):
    similarity = 0.0
    a = 0.0
    b = 0.0
    c = 0.0
    d = 0.0
    for id in Query_filenames:
        if Q == Query_filenames[id]:
            c = length[id]
    for id in document_filenames:
        if document == document_filenames[id]:
            d = length[id]

    for term in dictionary:
        if Q in Weight[term]:
            a = Weight[term][Q]
        else:
            a = 0.0
        if document in Weight[term]:
            b = Weight[term][document]
        else:
            b = 0.0
        similarity += (a * b)
    similarity = similarity / (c * d)
    return similarity

if __name__ == "__main__":
    main()
