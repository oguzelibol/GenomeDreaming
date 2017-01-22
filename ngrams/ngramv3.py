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
import numpy as np
from sklearn import preprocessing,svm


###### LOAD DATA ########
orgs = json.loads(open('y.json').read())
util = util('/Users/Akshay/Google Drive/prokaryotes/')
        
##Iterates through every FASTA file, parsing genome id (key) and sequence (value).
orgs["eco"]["class"]
list(orgs.keys())[0]
Escherichia = list()
Staphylococcus = list()
for org in orgs.keys():
    if(orgs[org]["class"] == "Escherichia"):
        Escherichia.append(org);
    if(orgs[org]["class"] == "Staphylococcus"):
        Staphylococcus.append(org);
print(Staphylococcus)
classes = list()
classes.append(Staphylococcus)
classes.append(Escherichia);


#Perplexity calculation. Remembe I need to add +V to bottom probability.
#Used log probabilities, so log perplexity calculation since risk of underflow with lots of probabilities
def perplexity(test, model):
    perp = 0
    for char in range(n, len(test)+1):
        ngram = tuple(test[char-n:char])
        try:
            perp = perp + log(1/model.get(ngram))
        except:
            perp
    perp = exp(perp/(len(test)+1-n)) 
    return perp


def singleGram(train,test,n):
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

    #Calculate actual n-gram frequencies in training set and add to 
    #laplacian smoothing
    bgs_train = nltk.ngrams(train,n)
    fdistTemp = nltk.FreqDist(bgs_train)
    for key in fdistTemp.keys(): #This for loop is only here because some genomes contain non-ATCG characters
        if key in fdist.keys():
            fdist[key] += fdistTemp[key];
            
    #Convert n-gram frequencies to probabilities. |V| = 4^n is implicitly added to the denominator to account for laplacian smoothing,
    #since fdist.values already have 1 added to each |V|.
    totalVal = sum(fdist.values())
    for key in fdist.keys():
        fdist[key] = fdist[key]/float(totalVal)
    #fdist.values()
    
    ##### CALCULATE TEST SEQUENCE PERPLEXITY #####
    perp = perplexity(test,fdist)
    print(perp)
    
    return fdist

###### TRAIN N-gram Model ######
n_max = 2; #define the max n (model will be built w/ n-gram from 1 to n_max)
X = list();
X_label = list()
classCount = -1
y = list();
for cl in iter(classes):
    classCount += 1
    for org in iter(cl):
        train = util.get_clean_single_org_genome('clean_'+org + '.fna')
        test = util.get_clean_single_org_genome('clean_' + org+ '.fna')
        print(len(test))
        bgs_smooth = nltk.ngrams("",1)
        fdist_tot = nltk.FreqDist(bgs_smooth)
        for n in range(1,n_max+1):
            fdist_tot += singleGram(train,test,n)
        sortedKeys = sorted(fdist_tot.keys())
        sortedFeatures = sorted(fdist_tot.keys())
        for i in range(0,len(sortedFeatures)):
            sortedFeatures[i] = fdist_tot[sortedKeys[i]]
        X.append(sortedFeatures)
        y.append(classCount)
## TEST ###
print(X)
print(y)



################ SVM Model #####################
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
clf = svm.SVC()
scores = cross_val_score(clf, X, y, cv=3)
print(scores)

clf = svm.SVC(kernel='linear', C=1).fit(X_train, y_train)
print(clf.score(X_test, y_test))




################Setting up Grid-search (check ipython notebook) ##################