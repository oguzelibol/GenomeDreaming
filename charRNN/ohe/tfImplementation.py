#Tensorflow implementation of Andrej Karpathys
#Simle RNN model - character level learning
#Oguz H. Elibol 10/27/2016
#Last modified 11/05/2016

import tensorflow as tf


class Config(object):
  """Holds model hyperparams and data information.
  """
  batchSize = 64
  embedSize = 50
  hiddenSize = 100
  numSteps = 25     #Steps to unroll the RNN 
  maxEpochs = 16
  dropout = 0.9
  lr = 1e-1         #Learning Rate 


class Model(object) 

  def loadData(self):
    data = open('input.txt','r').read() 
    chars = list(set(data)) 
    data_size, vocab_size  = len(data), len(chars)
    print 'data has %d characters, %d unique.' % (data_size, vocab_size)
    self.char2idx = { ch:i for i,ch in enumerate(chars)}
    self.idx2char = { i:ch for i,ch in enumerate(chars)}

  def addPlaceholders(self)
    self.inputPlaceholder = tf.placeholder(tf.int32, shape=(None, self.config.numSteps))
    self.labelsPlaceholder = tf.placeholder(tf.int32, shape=(None, self.config.numSteps))
    self.dropoutPlaceholder = tf.placeholder(tf.float32)

  def formEmbeddings(self)
  ''' 
  Forms the input batch for batch training
  '''
    inputs  = [char2idx[ch] for ch in data[
  
  def add_model(self, inputs)
    rnn  = tf.nn.rnn_cell.BasicRNNCell(self.config.numSteps, embedSize)

  def runEpoch(self, session, data, train_op=None, verbose=10):
    config = self.config
    dp = config.dropout

    #Running the code in forward pass 
    if not train_op:
      train_op = tf.no_op()
      dp = 1
    totalSteps = sum(1 for x in inputIterator(data, config.batchSize, config.numSteps))
    totalLoss = []
    state = self.initialState.eval()
    for step, (x, y) in enumerate(ptb_iterator(data, config.batch_size, config.num_steps)):
      # We need to pass in the initial state and retrieve the final state to give
      # the RNN proper history
      feed = {self.inputPlaceholder: x,
              self.labelsPlaceholder: y,
              self.initialState: state,
              self.dropoutPlaceholder: dp}
      loss, state, _ = session.run(
          [self.calculateLoss, self.finalState, train_op], feedDict=feed)
      totalLoss.append(loss)
      if verbose and step % verbose == 0:
          sys.stdout.write('\r{} / {} : pp = {}'.format(
              step, total_steps, np.exp(np.mean(totalLoss))))
          sys.stdout.flush()
    if verbose:
      sys.stdout.write('\r')
    return np.exp(np.mean(total_loss))

  # on the function defined before  
  def __init__(self, config):
    self.config = config
    self.load_data(debug=False)
    self.add_placeholders()
    self.inputs = self.add_embedding()
    self.rnn_outputs = self.add_model(self.inputs)
    self.outputs = self.add_projection(self.rnn_outputs)


#Run the RNN below 
def testRNN()
  config = Config()
  rnn  = Model(config)
  with tf.Session as session: 
    for epoch in range(config.maxEpochs)
    rnn.runEpoch(session, rnn.data)  
