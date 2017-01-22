from __future__ import print_function
import numpy as np
import tensorflow as tf

import argparse
import time
import os
from six.moves import cPickle

from utils import TextLoader
from model import Model

from six import text_type
from dataUtil import util 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--save_dir', type=str, default='saveEco',
                       help='model directory to store checkpointed models')
    parser.add_argument('-n', type=int, default=100,
                       help='number of characters to sample')
    parser.add_argument('--prime', type=text_type, default='ATG',
                       help='prime text')
    parser.add_argument('--sample', type=int, default=1,
                       help='0 to use max at each timestep, 1 to sample at each timestep, 2 to sample on spaces')
    args = parser.parse_args()
    score(args)

def score(args):
    #Add this cleanly to args after - for now, just loading the data 
    data_dir = 'prokaryotes/'
    data_file = 'tpi.fna'
    a  = util(data_dir) 
    data = a.get_single_org_genome(data_file)
    print('Loading model from ', args.save_dir)
    print('Evaluating file ', data_file)
    with open(os.path.join(args.save_dir, 'config.pkl'), 'rb') as f:
        saved_args = cPickle.load(f)
    with open(os.path.join(args.save_dir, 'chars_vocab.pkl'), 'rb') as f:
        chars, vocab = cPickle.load(f)
    model = Model(saved_args, True)
    with tf.Session() as sess:
        tf.initialize_all_variables().run()
        saver = tf.train.Saver(tf.all_variables())
        ckpt = tf.train.get_checkpoint_state(args.save_dir)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
            print(model.evaluate(sess, chars, vocab, data))

if __name__ == '__main__':
    main()
