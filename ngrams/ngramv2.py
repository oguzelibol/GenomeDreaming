import nltk
from nltk import bigrams
from nltk import trigrams
from nltk import FreqDist
from nltk.util import ngrams
from nltk.probability import LidstoneProbDist
from collections import Counter
from itertools import product
from math import log
from math import exp
from Bio.Seq import Seq
from Bio import SeqIO
import os;
import json
from util import util

###Perplexity method definition#
def perplexity(test, model):
    perp = 1
    #iterate through all possible n-grams; won't work for n=1
    for char in range(n, len(test)+1):
        ngram = tuple(test[char-n:char])
        try:
            perp = perp + log(1/model.get(ngram))
        except:
            perp
    perp = exp(perp/(len(test)+1-n)) 
    return perp

###### LOAD DATA ########
orgs = json.loads(open('training_data/y.json').read())
util = util('prokaryotes/')
        
##Iterates through every FASTA file, parsing genome id (key) and sequence (value).
orgs["eco"]["class"]
list(orgs.keys())[0]
Escherichia = list()
Treponema = list()
for org in orgs.keys():
    if(orgs[org]["class"] == "Escherichia"):
        Escherichia.append(org);
    if(orgs[org]["class"] == "Treponema"):
        Treponema.append(org);
print(Escherichia)
print(Treponema)

###### TRAIN N-gram Model ######
n = 2; #define the n for this n-gram

#Laplacian smoothing for all combinations of n-gram; creates initial
#frequency table with freq of var smooth given to every possible combination.
smooth = 0.1
vocabulary = "ATCG"
smoothingVocab = ['A','T','C','G']
#perms = [''.join(p) for p in product(vocabulary,repeat = n)]
bgs_smooth = nltk.ngrams("",1)
fdist = nltk.FreqDist(bgs_smooth)
for p in product(vocabulary,repeat = n):
    bgs_smooth = nltk.ngrams(p,n)
    fdist += nltk.FreqDist(bgs_smooth)
for key,value in fdist.items(): 
    fdist[key] = value*smooth  
fdist2 = fdist;

################Genome 1 - eco####################
#Calculate actual n-gram frequencies in training set and add to 
#laplacian smoothing
#for i in range(1,len(Escherichia)):
 #   print(Escherichia[i])
train = util.get_single_org_genome('eco.fna')
bgs_train = nltk.ngrams(train,n)
fdist += nltk.FreqDist(bgs_train)

#Convert n-gram frequencies to probabilities. |V| = 4^n is implicitly added to the denominator to account for laplacian smoothing,
#since fdist.values already have 1 added to each |V|.
totalVal = sum(fdist.values())
for key in fdist.keys():
    fdist[key] = fdist[key]/float(totalVal)

sortedKeys = sorted(fdist.keys())
sortedFeatures = sorted(fdist.keys())
for i in range(0,len(sortedFeatures)):
    sortedFeatures[i] = fdist[sortedKeys[i]]

ecoFeatures = sortedFeatures

################Genome 2 - sau####################
#Calculate actual n-gram frequencies in training set and add to 
#laplacian smoothing
#for i in range(1,len(Escherichia)):
 #   print(Escherichia[i])
train = util.get_single_org_genome('sau.fna')
bgs_train = nltk.ngrams(train,n)
fdist2 += nltk.FreqDist(bgs_train)

#Convert n-gram frequencies to probabilities. |V| = 4^n is implicitly added to the denominator to account for laplacian smoothing,
#since fdist.values already have 1 added to each |V|.
totalVal = sum(fdist2.values())
for key in fdist.keys():
    fdist2[key] = fdist2[key]/float(totalVal)

sortedKeys = sorted(fdist2.keys())
sortedFeatures = sorted(fdist2.keys())
for i in range(0,len(sortedFeatures)):
    sortedFeatures[i] = fdist2[sortedKeys[i]]
print(sortedFeatures)

sauFeatures = sortedFeatures;


##### CALCULATE TEST SEQUENCE PERPLEXITY #####
test = util.get_single_org_genome(Escherichia[1]+'.fna')
file = open("newfile.txt", "w")
file.write(test)
print(len(Treponema[1]))
perp = perplexity(test,fdist)
print(perp)
