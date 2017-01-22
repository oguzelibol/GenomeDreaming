from util import util
import pprint, json, os
util = util('prokaryotes/')
pp = pprint.PrettyPrinter(indent=4)
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("low", help="display a square of a given number", type=int)
args = parser.parse_args()

with open('y.json') as labels_file:
	labels = json.load(labels_file)

i = args.low
l = labels.keys()
for key in l[args.low: len(l)]:
	i += 1
	if ('clean_' + labels[key]['raw_file_name']) not in os.listdir('prokaryotes/') and labels[key]['raw_file_name'] in os.listdir('prokaryotes/'):
		print 'cleaning', i, labels[key]['raw_file_name']
		sequence = util.get_single_org_genome(labels[key]['raw_file_name'])
		with open('prokaryotes/clean_' + labels[key]['raw_file_name'], 'w') as file:
			file.write(sequence)
	else:
		print 'clean_' + labels[key]['raw_file_name'] + ' already exists!'
# pp.pprint(util.get_single_gene_based_genome('cds_eco.fna'))
# with open('demo_gene_list_of_json_for_cds_eco.json', 'w') as outfile:
# json.dump(util.get_single_gene_based_genome('cds_eco.fna'), outfile)
