#This code tests the data loader file so we can read in sequence information
from utils import TextLoader  

dataFolder = 'prokaryotes/'
batchSize  = 50 
seqLength  = 50

data_loader  = TextLoader(dataFolder,batchSize, seqLength)
print data_loader.vocab
print data_loader.tensor.shape
print data_loader.x_batches[1].shape
print len(data_loader.y_batches)

