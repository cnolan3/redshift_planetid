"""Short and sweet LSTM implementation in Tensorflow.

Motivation:
When Tensorflow was released, adding RNNs was a bit of a hack - it required
building separate graphs for every number of timesteps and was a bit obscure
to use. Since then TF devs added things like `dynamic_rnn`, `scan` and `map_fn`.
Currently the APIs are decent, but all the tutorials that I am aware of are not
making the best use of the new APIs.

Advantages of this implementation:
- No need to specify number of timesteps ahead of time. Number of timesteps is
  infered from shape of input tensor. Can use the same graph for multiple
  different numbers of timesteps.
- No need to specify batch size ahead of time. Batch size is infered from shape
  of input tensor. Can use the same graph for multiple different batch sizes.
- Easy to swap out different recurrent gadgets (RNN, LSTM, GRU, your new
  creative idea)
"""


import numpy as np
import random
import tensorflow as tf
import tensorflow.contrib.layers as layers
import csv

map_fn = tf.map_fn

################################################################################
##                           DATASET GENERATION                               ##
##                                                                            ##
##  The problem we are trying to solve is adding two binary numbers. The      ##
##  numbers are reversed, so that the state of RNN can add the numbers        ##
##  perfectly provided it can learn to store carry in the state. Timestep t   ##
##  corresponds to bit len(number) - t.                                       ##
################################################################################

#def as_bytes(num, final_size):
#    res = []
#    for _ in range(final_size):
#        res.append(num % 2)
#        num //= 2
#    return res
#
#def generate_example(num_bits):
#    a = random.randint(0, 2**(num_bits - 1) - 1)
#    b = random.randint(0, 2**(num_bits - 1) - 1)
#    res = a + b
#    return (as_bytes(a,  num_bits),
#            as_bytes(b,  num_bits),
#            as_bytes(res,num_bits))
#
#def generate_batch(num_bits, batch_size):
#    """Generates instance of a problem.
#
#    Returns
#    -------
#    x: np.array
#        two numbers to be added represented by bits.
#        shape: b, i, n
#        where:
#            b is bit index from the end
#            i is example idx in batch
#            n is one of [0,1] depending for first and
#                second summand respectively
#    y: np.array
#        the result of the addition
#        shape: b, i, n
#        where:
#            b is bit index from the end
#            i is example idx in batch
#            n is always 0
#    """
#    x = np.empty((num_bits, batch_size, 2))
#    y = np.empty((num_bits, batch_size, 1))
#
#    for i in range(batch_size):
#        a, b, r = generate_example(num_bits)
#        x[:, i, 0] = a
#        x[:, i, 1] = b
#        y[:, i, 0] = r
#    return x, y

# get test training data from files
def load_test_data(data_name, label_name):
    datafile = open(data_name, "r")
    labelfile = open(label_name, "r")
    datareader = csv.reader(datafile, delimiter=',', quotechar='|')
    labelreader = csv.reader(labelfile, delimiter=',', quotechar='|')
    datalist = list(datareader)
    labellist = list(labelreader)
    data = [[float(j) for j in i] for i in datalist]
    labels = [[float(j) for j in i] for i in labellist]

    return data, labels

# produce training data batches
def train_batch_producer(data, labels, batch_size, num_steps):
    
    # create staggered batches from raw data
    x = []
    y = []
    for i in range(batch_size):
        x.append(data[i:i + num_steps])
        y.append(labels[i:i + num_steps])

    return x, y

# produce data batches
def batch_producer(data, batch_size, num_steps):
    
    # create staggered batches from raw data
    x = []
    for i in range(batch_size):
        x.append(data[i:i + num_steps])

    return x

################################################################################
##                           GRAPH DEFINITION                                 ##
################################################################################

class Model(object):
    def __init__(self, hidden_size, learning_rate=0.01):
        INPUT_SIZE    = 2       
        OUTPUT_SIZE   = 1       
        TINY          = 1e-6    # to avoid NaNs in logs

        self.inputs  = tf.placeholder(tf.float32, (None, None, INPUT_SIZE))  # (time, batch, in)
        self.outputs = tf.placeholder(tf.float32, (None, None, OUTPUT_SIZE)) # (time, batch, out)

        cell = tf.contrib.rnn.BasicLSTMCell(hidden_size, state_is_tuple=True)

        # Create initial state. Here it is just a constant tensor filled with zeros,
        # but in principle it could be a learnable parameter. This is a bit tricky
        # to do for LSTM's tuple state, but can be achieved by creating two vector
        # Variables, which are then tiled along batch dimension and grouped into tuple.
        batch_size    = tf.shape(self.inputs)[1]
        initial_state = cell.zero_state(batch_size, tf.float32)

        # Given inputs (time, batch, input_size) outputs a tuple
        #  - outputs: (time, batch, output_size)  [do not mistake with OUTPUT_SIZE]
        #  - states:  (time, batch, hidden_size)
        rnn_outputs, rnn_states = tf.nn.dynamic_rnn(cell, self.inputs, initial_state=initial_state, time_major=True)

        # project output from rnn output size to OUTPUT_SIZE. Sometimes it is worth adding
        # an extra layer here.
        final_projection = lambda x: layers.linear(x, num_outputs=OUTPUT_SIZE, activation_fn=tf.nn.sigmoid)

        # apply projection to every timestep.
        self.predicted_outputs = map_fn(final_projection, rnn_outputs)

        # compute elementwise cross entropy.
        self.error = -(self.outputs * tf.log(self.predicted_outputs + TINY) + (1.0 - self.outputs) * tf.log(1.0 - self.predicted_outputs + TINY))
        self.error = tf.reduce_mean(self.error)

        # optimize
        self.train_fn = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(self.error)

        # assuming that absolute difference between output and correct answer is 0.5
        # or less we can round it to the correct output.
        self.accuracy = tf.reduce_mean(tf.cast(tf.abs(self.outputs - self.predicted_outputs) < 0.5, tf.float32))


################################################################################
##                           TRAINING LOOP                                    ##
################################################################################

def train(model, num_steps, iter_per_epoch, iters, data_filename, labels_filename, saver_filename):

    valid_x, valid_y = load_test_data(data_filename, labels_filename)

    BATCH_SIZE = len(valid_y) - num_steps
    valid_x, valid_y = train_batch_producer(valid_x, valid_y, BATCH_SIZE, num_steps)

    session = tf.Session()
    with tf.Session() as sess:

        sess.run(tf.global_variables_initializer())

        saver = tf.train.Saver()

        #saver.restore(sess, saver_filename)

        for epoch in range(iters):
            epoch_error = 0
            for _ in range(iter_per_epoch):
                # here train_fn is what triggers backprop. error and accuracy on their
                # own do not trigger the backprop.
                epoch_error += sess.run([model.error, model.train_fn], {
                    model.inputs: valid_x,
                    model.outputs: valid_y,
                })[0]
            epoch_error /= iter_per_epoch
            valid_accuracy = sess.run(model.accuracy, {
                model.inputs:  valid_x,
                model.outputs: valid_y,
            })
            print ("Epoch %d, train error: %.2f, valid accuracy: %.1f %%" % (epoch, epoch_error, valid_accuracy * 100.0))

        saver.save(sess, saver_filename)

def run(model, num_steps, raw_data, saver_filename):

    data_len = len(raw_data)

    BATCH_SIZE = data_len - num_steps
    x = batch_producer(raw_data, BATCH_SIZE, num_steps)

    with tf.Session() as sess:
        saver = tf.train.Saver()

        saver.restore(sess, saver_filename)

        prediction = sess.run(model.predicted_outputs, {model.inputs: x})
        print(prediction)
