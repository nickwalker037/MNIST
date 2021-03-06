# The below code references TensorFlow's Convolutional Neural Network Tutorial and can be found on TensorFlow's website

import tensorflow as tf

# Load the data:
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)


# Placeholders:
x = tf.placeholder(tf.float32, shape=[None,784]) # None for unspecified amount of evidence, imported as 32x32 pixel matrices (784 pixels total)
y_ = tf.placeholder(tf.float32, shape=[None, 10]) # Target output classes

# Variables:
W = tf.Variable(tf.zeros([784, 10])) # shape as this in order to multiply it by x to output produce a 10-dim vector for each class
b = tf.Variable(tf.zeros([10])) # 10 for the output classes. this is the bias

sess.run(tf.global_variables_initializer())


# Weight Initialization:
def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1) # truncated_normal outputs random values from a truncated normal distribution
    return tf.Variable(initial)

# Define the bias variable:
def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return(tf.Variable(initial))
    
# Define Convolution with stride of 1 and zero padding
def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding = 'SAME') # strides --> [batch, height, width, channel] (channel means depth of convolution) (use -1 for batch as a placeholder that adjusts the size as necessary to match the size needed for the full tensor)

# Define Pooling as max pooling over 2x2 blocks:
def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                             strides=[1, 2, 2, 1],
                             padding = 'SAME')
                             
                             
# First Convolution Layer - computing 32 features for each 5x5 patch
    # its weight tensor will have a shape of [5, 5, 1, 32]
        # first two dimensions are patch size, 3rd is num of input channels, 4th isnum of output channels
W_conv1 = weight_variable([5, 5, 1, 32])
b_conv1 = bias_variable([32])

# to apply the layer, reshape x to a 4d tensor 
# with the 2nd and 3rd dimensions corresponding to the image width and height
# and the final dimension corresponding to the number of color channels
x_image = tf.reshape(x, [-1, 28, 28, 1])


#then convolve x_image with weight tensor, add bias, apply ReLU, and max pool
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)


# Second Convolution Layer - having 64 features for each 5x5 patch
W_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])

h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)


# Densely Connected Layer
    # now that image size is 7x7, add a fully-connected layer with 1024 neurons to allow processing the entire image
    
W_fc1 = weight_variable([7 * 7 * 64, 1024])
b_fc1 = bias_variable([1024])

h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)


# Dropout - to reduce overfitting
keep_prob = tf.placeholder(tf.float32) # placeholder for the prob that a neuron's output is kept during dropout
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)


# Readout Layer:
W_fc2 = weight_variable([1024, 10])
b_fc2 = bias_variable([10])

y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2


# Train and Evaluate the Model
cross_entropy = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(labels=y_, logits=y_conv))

train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))

accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(10000):
        batch = mnist.train.next_batch(50)
        if 1 % 100 == 0:
            train_accuracy = accuracy.eval(feed_dict= {
                x:batch[0], y_:batch[1], keep_prob: 1.0})
            print('step %d, training accuracy %g' % (i, train_accuracy))
        train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})
        
    print('Test Accuracy: %g' % accuracy.eval(feed_dict={x: mnist.test.images,
                                                         y_: mnist.test.labels,
                                                         keep_prob: 1.0}))
