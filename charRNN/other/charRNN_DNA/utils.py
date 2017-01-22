import codecs
import os
import collections
from six.moves import cPickle
import numpy as np
from dataUtil import util
import random

class TextLoader():
    def __init__(self, data_dir, batch_size, seq_length, savedVocab = None, savedChars = None, encoding='utf-8'):
        a = util(data_dir)
        data_file  = 'tpi.fna'
        self.valratio = 0.1
        #print("generating random sequence")
        #self.data = self.genRandom(4500000)
        self.data = a.get_single_org_genome(data_file)
        print("Data file is ", data_file)
        self.batch_size = batch_size
        self.seq_length = seq_length
        self.encoding = encoding

        vocab_file = os.path.join(data_dir, "vocab.pkl")
        tensor_file = os.path.join(data_dir, "data.npy")

        #if not (os.path.exists(vocab_file) and os.path.exists(tensor_file)):
        if savedVocab != None and savedChars !=None: 
            self.preprocessTensor(savedChars, savedVocab)
        else: 
            print("reading text file")
            self.preprocess(vocab_file, tensor_file)
       # else:
       #     print("loading preprocessed files")
       #     self.load_preprocessed(vocab_file, tensor_file)
        self.create_batches()
        self.reset_batch_pointer()
        self.reset_valbatch_pointer()

   
    def genRandom(self, size):
        bases = ['A','T','C','G']
        result =[]
        for _ in range(size):
            result.append(random.choice(bases))
        return result 

    def preprocessTensor(self, savedChars, savedVocab):
        self.chars = savedChars
        self.vocab_size = len(self.chars)
        self.vocab = savedVocab
        self.tensor = np.array(list(map(self.vocab.get, self.data)))

    def preprocess(self, vocab_file, tensor_file):
       
        counter = collections.Counter(self.data)
        count_pairs = sorted(counter.items(), key=lambda x: -x[1])
        self.chars, _ = zip(*count_pairs)
        self.vocab_size = len(self.chars)
        self.vocab = dict(zip(self.chars, range(len(self.chars))))
        #with open(vocab_file, 'wb') as f:
        #    cPickle.dump(self.chars, f)
        self.tensor = np.array(list(map(self.vocab.get, self.data)))
       # np.save(tensor_file, self.tensor)

    def load_preprocessed(self, vocab_file, tensor_file):
        with open(vocab_file, 'rb') as f:
            self.chars = cPickle.load(f)
        self.vocab_size = len(self.chars)
        self.vocab = dict(zip(self.chars, range(len(self.chars))))
        self.tensor = np.load(tensor_file)
        self.num_batches = int(self.tensor.size / (self.batch_size *
                                                   self.seq_length))

    def create_batches(self):
        self.num_batches = int(self.tensor.size / (self.batch_size *
                                                   self.seq_length))

        # When the data (tensor) is too small, let's give them a better error message
        if self.num_batches==0:
            assert False, "Not enough data. Make seq_length and batch_size small."

        self.tensor = self.tensor[:self.num_batches * self.batch_size * self.seq_length]
        xdata = self.tensor
        ydata = np.copy(self.tensor)
        ydata[:-1] = xdata[1:]
        ydata[-1] = xdata[0]
        self.x_batches = np.split(xdata.reshape(self.batch_size, -1), self.num_batches, 1)
        self.y_batches = np.split(ydata.reshape(self.batch_size, -1), self.num_batches, 1)

        index = int((1-self.valratio)*self.num_batches)
        print index 

        self.x_valbatches = self.x_batches[index:]
        self.y_valbatches = self.y_batches[index:]
        self.x_batches = self.x_batches[:index]
        self.y_batches = self.y_batches[:index]
        self.num_batches = len(self.x_batches)
        self.num_valbatches = len(self.x_valbatches)

    def next_batch(self):
        x, y = self.x_batches[self.pointer], self.y_batches[self.pointer]
        self.pointer += 1
        return x, y

    def next_valbatch(self):
        xval, yval = self.x_valbatches[self.valpointer], self.y_valbatches[self.valpointer]
        self.valpointer += 1
        return xval, yval

    def val_batch(self):
        return self.xValidation, self.yValidation

    def reset_batch_pointer(self):
        self.pointer = 0

    def reset_valbatch_pointer(self):
        self.valpointer = 0
