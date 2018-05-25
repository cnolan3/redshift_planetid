import tensorflow as tf
import csv
import numpy as np

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

# produce data batches
def batch_producer(data, labels, batch_size, num_steps):
    
    # create staggered batches from raw data
    x = []
    y = []
    for i in range(batch_size):
        x.append(data[i:i + num_steps])
        y.append(labels[i + num_steps - 1])

#    data = tf.convert_to_tensor(x, name='data', dtype=tf.float32)
#    labels = tf.convert_to_tensor(y, name='labels', dtype=tf.float32)
#
#    data_len = tf.size(labels)
#    y = np.reshape(y, (batch_size, num_steps))
#    y = labels

    return x, y

# model input object
class Input(object):
    def __init__(self, num_steps, data, labels):
        self.num_steps = num_steps
        self.batch_size = len(labels) - num_steps
        self.epoch_size = ((len(data) // self.batch_size) - 1) // num_steps
        self.input_data, self.targets = batch_producer(data, labels, self.batch_size, num_steps)

# model object
class Model(object):
    def __init__(self, input_obj, is_training, hidden_size, learning_rate=0.001, dropout=0.5, init_scale=0.05):
        self.is_training = is_training
        self.input_obj = input_obj
        self.batch_size = input_obj.batch_size
        self.num_steps = input_obj.num_steps
        self.hidden_size = hidden_size

        out_weights = tf.Variable(tf.random_normal([self.hidden_size, 1]))
        out_bias = tf.Variable(tf.random_normal([1]))

        x = tf.placeholder("float", [None, self.num_steps, 2])
        y = tf.placeholder("float", [None, 1])

        inp = tf.unstack(x, self.num_steps, 1)

        lstm_layer = tf.contrib.rnn.BasicLSTMCell(self.hidden_size, forget_bias=1)

        output, state = tf.contrib.rnn.static_rnn(lstm_layer, inp, dtype="float32")

        prediction = tf.matmul(output[-1], out_weights) + out_bias

        loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y))
        opt = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(loss)

        correct_prediction = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

        init = tf.global_variables_initializer()
        with tf.Session() as sess:
            sess.run(init)

            iter = 1
            while iter < 5:
                batch_x = self.input_obj.input_data
                batch_y = self.input_obj.targets

                sess.run(opt, feed_dict={x: batch_x, y: batch_y})

                if iter % 1 == 0:
                    acc = sess.run(accuracy, feed_dict={x: batch_x, y: batch_y})
                    los = sess.run(loss, feed_dict={x: batch_x, y:batch_y})
                    print("For iter ", iter)
                    print("Accuracy ", acc)
                    print("Loss ", los)
                    print("____________")
                    print("Prediction: ", sess.run(prediction))
                    print("____________")

                iter = iter + 1

            test_data = self.input_obj.input_data
            test_label = self.input_obj.targets

            print("Testing Accuracy:", sess.run(accuracy, feed_dict={x: test_data, y: test_label}))
