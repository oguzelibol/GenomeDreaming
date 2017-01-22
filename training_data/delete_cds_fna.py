import gzip, os

for file in os.listdir('prokaryotes/'):
	if file.startswith('cds_') and file.endswith('.fna'):
		print('Removed ' + file) 
		os.remove('prokaryotes/' + file)        
		        