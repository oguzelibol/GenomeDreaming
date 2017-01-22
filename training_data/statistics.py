import json, requests, numpy
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
from numpy import *

url = "http://www.genome.jp/kegg-bin/show_organism?org="

with open('y.json') as data_file: 
    data = json.load(data_file)

num_protein_genes = []
num_RNA_genes = []

count = 0;
for key in data:
	count += 1
	if count > 100:
		break
	try:
		r = requests.get(url + str(key))
		string = r.content
		start_protein = string.find("Number of protein genes:") + len("Number of protein genes:")
		start_RNA = string.find("Number of RNA genes:") + len("Number of RNA genes:")
		if start_protein >= 0 and start_RNA >= 0:
			end_protein = string.find("<br>", start_protein)
			end_RNA = string.find("<br>", start_RNA)
			num_protein_genes.append(int(string[start_protein:end_protein]))
			num_RNA_genes.append(int(string[start_RNA:end_RNA]))
			print len(num_protein_genes), len(num_RNA_genes)
	except:
		print "can't parse: " + key
print "num_protein_genes: average " + str(numpy.mean(num_protein_genes)) + " variance: " + str(numpy.var(num_protein_genes))
print "num_RNA_genes: average " + str(numpy.mean(num_RNA_genes)) + " variance: " + str(numpy.var(num_RNA_genes))
plt.hist(num_protein_genes, bins=100, range=(min(num_RNA_genes), max(num_protein_genes)+1))
plt.show()
