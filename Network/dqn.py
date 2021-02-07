import tensorflow as tf


class DQN:
    def __init__(self, stateSize, actionSize, learningRate, name):
        self.stateSize = stateSize
        self.actionSize = actionSize
        self.learningRate = learningRate
        self.name = name

        with tf.variable_scope(self.name):
            # the inputs describing the state
            self.inputs_ = tf.placeholder(tf.float32, [None, *self.stateSize], name="inputs")

            # the one hotted action that we took
            # e.g. if we took the 3rd action action_ = [0,0,1,0,0,0,0]
            self.actions_ = tf.placeholder(tf.float32, [None, self.actionSize], name="actions")

            # the target = reward + the discounted maximum possible q value of hte next state
            self.targetQ = tf.placeholder(tf.float32, [None], name="target")

            self.ISWeights_ = tf.placeholder(tf.float32, [None, 1], name='ISWeights')

            self.dense1 = tf.layers.dense(inputs=self.inputs_,
                                          units=16,
                                          activation=tf.nn.elu,
                                          kernel_initializer=tf.contrib.layers.xavier_initializer(),
                                          name="dense1")
            self.dense2 = tf.layers.dense(inputs=self.dense1,
                                          units=16,
                                          activation=tf.nn.elu,
                                          kernel_initializer=tf.contrib.layers.xavier_initializer(),
                                          name="dense2")
            self.output = tf.layers.dense(inputs=self.dense2,
                                          units=self.actionSize,
                                          kernel_initializer=tf.contrib.layers.xavier_initializer(),
                                          activation=None,
                                          name="outputs")

            # by multiplying the output by the one hotted action space we only get the q value we desire
            # all other values are 0, therefore taking the sum of these values gives us our qValue
            self.QValue = tf.reduce_sum(tf.multiply(self.output, self.actions_))

            self.absoluteError = abs(self.QValue - self.targetQ)  # used for prioritising experiences

            # calculate the loss by using mean squared error
            self.loss = tf.reduce_mean(self.ISWeights_ * tf.square(self.targetQ - self.QValue))

            # use adam optimiser (its good shit)
            self.optimizer = tf.train.AdamOptimizer(self.learningRate).minimize(self.loss)