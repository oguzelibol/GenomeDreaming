#Plotter for the training data collectted during training 
#Oguz H. Elibol 
import matplotlib.pyplot as plt
from six.moves import cPickle
import os 
import numpy as np

def plot():
    save_dir  = 'save'
    with open(os.path.join(save_dir, 'lossHistory.pkl')) as f:
        data1, data2  = cPickle.load(f)

    data1x = np.array(range(len(data1)))
    data1x = data1x*50/float(len(data1))
    plt.plot(data1x,data1,label = 'training loss')
    plt.plot(data2,label = 'validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('CE Loss')
    plt.legend()
    plt.ylim([1.1,1.6])
    plt.savefig('TrainingLoss.png')

if __name__ == '__main__':
    plot()
