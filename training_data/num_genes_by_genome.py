import json as JSON
import matplotlib.pyplot as plt
import numpy as np
import plotly.plotly as py

with open('y.json', 'r') as f:
	json = JSON.load(f)

num_genes_by_genome = {}

i = 0
for genome in json:
	i += 1
	try:
		with open('prokaryotes/cds_' + genome + '.fna', 'r') as f:
			string = ''.join(f.readlines())
			count = string.count('>lcl')
			if count:
				num_genes_by_genome[genome] = count
	except:
		print i, 'unable'

data = num_genes_by_genome.values()
binwidth = 100
numpy_hist = plt.figure()
plt.hist(data, bins=range(min(data), max(data) + binwidth, binwidth))
plt.title("Number of Genes per Genome")
plt.xlabel("# Genes")
plt.ylabel("Frequency")
fig = plt.gcf()
print 'mean = ', np.mean(data)
print 'median = ',  np.median(data)
plt.show()
# plot_url = py.plot_mpl(numpy_hist, filename='numpy-bins')