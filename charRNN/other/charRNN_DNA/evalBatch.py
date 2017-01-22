from __future__ import print_function
import numpy as np
import tensorflow as tf

import argparse
import time
import os
from six.moves import cPickle

from utils import TextLoader
from model import Model

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='prokaryotes/',
                       help='data directory containing input.txt')
    parser.add_argument('--save_dir', type=str, default='save',
                       help='directory to store checkpointed models')
    parser.add_argument('--rnn_size', type=int, default=128,
                       help='size of RNN hidden state')
    parser.add_argument('--num_layers', type=int, default=2,
                       help='number of layers in the RNN')
    parser.add_argument('--model', type=str, default='lstm',
                       help='rnn, gru, or lstm')
    parser.add_argument('--batch_size', type=int, default=50,
                       help='minibatch size')
    parser.add_argument('--seq_length', type=int, default=50,
                       help='RNN sequence length')
    parser.add_argument('--num_epochs', type=int, default=50,
                       help='number of epochs')
    parser.add_argument('--save_every', type=int, default=1000,
                       help='save frequency')
    parser.add_argument('--grad_clip', type=float, default=5.,
                       help='clip gradients at this value')
    parser.add_argument('--learning_rate', type=float, default=0.002,
                       help='learning rate')
    parser.add_argument('--decay_rate', type=float, default=0.97,
                       help='decay rate for rmsprop')                       
    parser.add_argument('--init_from', type=str, default='save',
                       help="""continue training from saved model at this path. Path must contain files saved by previous training process: 
                            'config.pkl'        : configuration;
                            'chars_vocab.pkl'   : vocabulary definitions;
                            'checkpoint'        : paths to model file(s) (created by tf).
                                                  Note: this file contains absolute paths, be careful when moving files around;
                            'model.ckpt-*'      : file(s) with model definition (created by tf)
                        """)
    args = parser.parse_args()
    print("Data Directory", args.data_dir)
    print("Initialize From", args.init_from)
    evalBatch(args)

def evalBatch(args):
    #Data loader contains the file to load
    with open(os.path.join(args.init_from, 'chars_vocab.pkl')) as f:
        saved_chars, saved_vocab = cPickle.load(f)

    data_loader = TextLoader(args.data_dir, args.batch_size, args.seq_length, savedChars = saved_chars, savedVocab = saved_vocab)
    args.vocab_size = data_loader.vocab_size
    
    # check compatibility if training is continued from previously saved model
    # check if all necessary files exist 
    assert os.path.isdir(args.init_from)," %s must be a a path" % args.init_from
    assert os.path.isfile(os.path.join(args.init_from,"config.pkl")),"config.pkl file does not exist in path %s"%args.init_from
    assert os.path.isfile(os.path.join(args.init_from,"chars_vocab.pkl")),"chars_vocab.pkl.pkl file does not exist in path %s" % args.init_from
    ckpt = tf.train.get_checkpoint_state(args.init_from)
    assert ckpt,"No checkpoint found"
    assert ckpt.model_checkpoint_path,"No model path found in checkpoint"

    # open old config and check if models are compatible
    with open(os.path.join(args.init_from, 'config.pkl')) as f:
        saved_model_args = cPickle.load(f)
    need_be_same=["model","rnn_size","num_layers","seq_length"]
    for checkme in need_be_same:
        assert vars(saved_model_args)[checkme]==vars(args)[checkme],"Command line argument and saved model disagree on '%s' "%checkme

# open saved vocab/dict and check if vocabs/dicts are compatible
        #print(saved_vocab, data_loader.vocab)
    assert saved_chars==data_loader.chars, "Data and loaded model disagree on character set!"
    assert saved_vocab==data_loader.vocab, "Data and loaded model disagree on dictionary mappings!"
        
        
    model = Model(args)

    with tf.Session() as sess:
        tf.initialize_all_variables().run()
        saver = tf.train.Saver(tf.all_variables())
        # restore model
        saver.restore(sess, ckpt.model_checkpoint_path)
        #for e in range(args.num_epochs):
        #No longer running muliple epochs 
        data_loader.reset_batch_pointer()
        state = sess.run(model.initial_state)
        total_loss = [] 
        for b in range(data_loader.num_batches):
 	    start = time.time()
	    x, y = data_loader.next_batch()
	    feed = {model.input_data: x, model.targets: y}
	    for i, (c, h) in enumerate(model.initial_state):
	        feed[c] = state[i].c
	        feed[h] = state[i].h
	    train_loss, state = sess.run([model.cost, model.final_state], feed)
	    total_loss.append(train_loss)
	    end = time.time()
	    print("{}/{}, train_loss = {:.3f}, time/batch = {:.3f}" \
	        .format(b, data_loader.num_batches, train_loss, end - start))
	print("Perplexity ", np.exp(np.mean(total_loss))) 
if __name__ == '__main__':
    main()
