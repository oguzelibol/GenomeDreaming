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

###### LOAD DATA ########
dataPath = '/Users/Akshay/Dropbox/code/GenomeDreaming/data/'

##Iterates through every FASTA file, parsing genome id (key) and sequence (value).
genomes = []
for fastaFile in os.listdir(dataPath):
    if "fna" in fastaFile: #ensures only fasta files being read
        handle = open(dataPath + fastaFile, "r")
        genomes.append(list(SeqIO.parse(handle, "fasta")))
        handle.close()
len(genomes[1][0].seq)



###### TRAIN N-gram Model ######
train = genomes[1][0].seq
test = "GGAAA"

n = 5; #define the n for this n-gram

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
fdist += nltk.FreqDist(bgs_train)
print(fdist.values())
#Convert n-gram frequencies to probabilities. |V| = 4^n is implicitly added to the denominator to account for laplacian smoothing,
#since fdist.values already have 1 added to each |V|.
totalVal = sum(fdist.values())
for key in fdist.keys():
    fdist[key] = fdist[key]/float(totalVal)
#fdist.values()
#print(fdist.values())
#Perplexity calculation. Remembe I need to add +V to bottom probability.
#Used log probabilities, so log perplexity calculation since risk of underflow with lots of probabilities
#Need to make sure I'm calculating the perplexity correctly for ngrams;
#specifically, the idea of using the previous n words to predict the next
#right now i'm just treating each consecutive n-gram in the test set
#as independent from the last and multiplying all their probabilities
#(sum here, because log)
def perplexity(testset, model):
    perplexity = 1
    #iterate through all possible n-grams; won't work for n=1
    for char in range(n, len(test)+1):
        ngram = tuple(test[char-n:char])
        perplexity = perplexity * (1/model.get(ngram))
    perplexity = pow(perplexity, 1/float())
    return perplexity

test = genomes[1][0].seq
perplexity = 0
##### CALCULATE TEST SEQUENCE PERPLEXITY #####
for char in range(n, len(test)+1):
    ngram = tuple(test[char-n:char])
    perplexity += log(1/fdist.get(ngram))
    #print(ngram)
    #print(fdist.get(ngram))
    ##print(perplexity)
perplexity = exp(perplexity/(len(test)+1-n))
print(perplexity)
