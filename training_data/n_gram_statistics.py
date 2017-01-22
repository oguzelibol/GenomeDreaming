def occurrences(string, sub):
    count = start = 0
    while True:
        start = string.find(sub, start) + 1
        if start > 0:
            count+=1
        else:
            return count

import sys, json, random, copy
from pprint import pprint
from util import util
sys.path.insert(0, '../tsne/')
from tSNE import tSNE

util = util('prokaryotes/')

with open('y.json') as y_json_file:
	y_json = json.load(y_json_file)

temp = copy.deepcopy(y_json)
for key in y_json:
	if y_json[key]['class'].find('Bacilli') < 0 and y_json[key]['class'].find('Gammaproteobacteria') < 0:
		del temp[key]
y_json = temp

X, Y_domain, Y_phylum, Y_class, Y_genus, Y_name = [], [], [], [], [], []

one_gram_features = ['A', 'T', 'C', 'G']
two_gram_features = []
three_gram_features = []
four_gram_features = []
five_gram_features = []
for i in one_gram_features:
	for j in one_gram_features:
		two_gram_features.append(i + j)
		for k in one_gram_features:
			three_gram_features.append(i + j + k)
			for l in one_gram_features:
				four_gram_features.append(i + j + k + l)
				for m in one_gram_features:
					five_gram_features.append(i + j + k + l + m)

two_gram_features += one_gram_features
three_gram_features += two_gram_features
four_gram_features += three_gram_features
five_gram_features += four_gram_features

print len(one_gram_features)
print len(two_gram_features)
print len(three_gram_features)
print len(four_gram_features)
print len(five_gram_features)

unique_domain, unique_phylum, unique_class, unique_genus, unique_name = [], [], [], [], []

for key in y_json:
	if y_json[key]['domain'] not in unique_domain:
		unique_domain.append(y_json[key]['domain'])	
	if y_json[key]['phylum'] not in unique_phylum:
		unique_phylum.append(y_json[key]['phylum'])
	if y_json[key]['class'] not in unique_class:
		unique_class.append(y_json[key]['class'])
	if y_json[key]['genus'] not in unique_genus:
		unique_genus.append(y_json[key]['genus'])
	if y_json[key]['name'] not in unique_name:
		unique_name.append(y_json[key]['name'])
	
print len(unique_domain), len(unique_phylum), len(unique_class), len(unique_genus), len(unique_name)

print unique_domain
print unique_phylum
print unique_class
print unique_genus
print unique_name

i = 0

print 'label size = ' + str(len(y_json))
keys = y_json.keys()
random.shuffle(keys)

for key in keys:
	i += 1
	print 'clean_' + y_json[key]['name']
	sequence = util.get_clean_single_org_genome('clean_' + y_json[key]['name'] + '.fna')
	length = len(sequence)
	x = [sequence.count(char) * 1.0000 / (length / len(char)) for char in five_gram_features]
	# x = [occurrences(sequence, char) * 1.0000 / (length - 1) for char in two_gram_features]
	# x = [occurrences(sequence, char) * 1.0000 / (length - 2) for char in three_gram_features]
	# x = [occurrences(sequence, char) * 1.0000 / (length - 3) for char in four_gram_features]
	# x = [occurrences(sequence, char) * 1.0000 / (length - 4) for char in five_gram_features]
	s = sum(x)
	print i, s
	# assert s > 0.75 and s < 1.25
	X.append(x)
	Y_domain.append(unique_domain.index(y_json[key]['domain']) + 1)
	Y_phylum.append(unique_phylum.index(y_json[key]['phylum']) + 1)
	Y_class.append(unique_class.index(y_json[key]['class']) + 1)
	Y_genus.append(unique_genus.index(y_json[key]['genus']) + 1)
	Y_name.append(unique_name.index(y_json[key]['name']) + 1)

assert len(X) == len(Y_domain) == len(Y_phylum) == len(Y_class) == len(Y_genus) == len(Y_name)

tsne = tSNE()
tsne.plot(X, Y_domain, Y_phylum, Y_class, Y_genus, Y_name, unique_domain, unique_phylum, unique_class, unique_genus, unique_name, '5GramAkshay-1b')


