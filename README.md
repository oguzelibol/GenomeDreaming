# GenomeDreaming Project for Stanford CS229

## Authors: Oguz H. Elibol, Akshay Maheshwari, Bohan Wu

### HOW TO USE THE TSNE class:

SEE demo.py. Example:

from tSNE import tSNE

tsne = tSNE()

tsne.plot(X[:1000], Y[:1000])

X = 

[[ 0.  0.  0. ...,  0.  0.  0.]
 [ 0.  0.  0. ...,  0.  0.  0.]
 [ 0.  0.  0. ...,  0.  0.  0.]
 ..., 
 [ 0.  0.  0. ...,  0.  0.  0.]
 [ 0.  0.  0. ...,  0.  0.  0.]
 [ 0.  0.  0. ...,  0.  0.  0.]]

Y = [5 0 4 1 9 2 1 3 1 4 3 5 ... 4 4 2 4 4 3 1 7 7 6 0 3 6]

NOTE: X needs to be a 2D array with dimension m * n, where m is number of training examples and n is number of features. Y needs to be a 1D array with dimension m * 1, where m is number of training examples.

Avoid letting m > 10000 and/or n > 1000, otherwise it will be as slow as 2 minutes.

### General guideline for pushing to remote master branch:
	1) git commit -m '[commit message]': commit new changes to your local *_dev branch (create one if first time, in my case my dev branch is 'bohanwu_dev')
	2) git fetch && git merge origin/master OR git pull origin master: pulling the newest commits from the remote master branch to your local *_dev so your dev branch is synced
  	3) git push origin *_dev: pushing new commits from your local dev branch to your remote dev branch
	4) submit a pull request so that each of us can look at/review the code before merging these new commits into remote master on github

### code explanation:
	bohanwu_dev:
	1) check_corruption.py: check if any .gz zip files are corrupted and if so, delete them.
	2) data_retrival.py: download every file in genome_urls.htm without repeating donwloading of any files
	3) genome_urls: an html file that contains the urls for complete genome files of all prokaryotes (the discrepency in total number yet to be resolved) 
