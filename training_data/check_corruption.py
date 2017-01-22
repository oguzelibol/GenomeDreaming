import gzip, os
for file in os.listdir('prokaryotes/'):
	if file.find('fna.gz') >= 0:
		with gzip.open('prokaryotes/' + file) as g:
		    try:
		        while g.read(1024 * 1024):
		            pass
		    except IOError as e:
		        print("Corrupted!", e)
		        os.remove('prokaryotes/' + file)
		        print('Removed ' + file) 
		        unzipped_file = file[:file.find('.gz')]
		        if unzipped_file in os.listdir('prokaryotes/'): 
		        	print('Removed ' + unzipped_file) 
		        	os.remove('prokaryotes/' + unzipped_file)