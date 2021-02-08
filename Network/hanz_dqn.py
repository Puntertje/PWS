from termcolor import colored
from . import dqn, memory
import tensorflow as tf
import numpy as np
import random
import os
"""
Welcome to Hanz Verkehrsschlager, he doesn't bite except when he does.
"""


# Modified/Stolen from https://github.com/Code-Bullet/Car-QLearning/blob/master/main.py
# Oh yeah no, I 100% stole it from there ^
# Also huge help from sentdex's video series, https://www.youtube.com/c/sentdex
# TODO: refactor *all* of this, including but not limited to;
#       Integrate AI with game
#       - game.get_state
#       - game.make_action
#       Clean up the code
#       Improve commenting
class Brain:
    def __init__(self, game, load=False, load_from_episode_no=0):
        self.game = game
        self.stateSize = [game.max_cars]
        self.actionSize = 4 * 16       # number of possible actions, each light has 4 states, there are 16 lights
        self.learningRate = 0.00025
        self.possibleActions = np.identity(self.actionSize, dtype=int)
        self.totalTrainingEpisodes = 100000
        self.maxSteps = 300  #3600
        self.batchSize = 64
        self.memorySize = 100000
        self.maxEpsilon = 1
        self.minEpsilon = 0.01
        self.decayRate = 0.00001
        self.decayStep = 0
        self.gamma = 0.9
        self.training = True
        self.pretrainLength = self.batchSize
        self.maxTau = 10000
        self.tau = 0
        self.score_floor = -50000       # At some point we kind of give up I guess? Beats telling management we failed.
        # reset the graph i guess, I don't know why therefore is already a graph happening but who cares
        tf.compat.v1.reset_default_graph()
        self.sess = tf.compat.v1.Session()
        self.DQNetwork = dqn.DQN(self.stateSize, self.actionSize, self.learningRate, name='DQNetwork')
        self.TargetNetwork = dqn.DQN(self.stateSize, self.actionSize, self.learningRate, name='TargetNetwork')
        self.memoryBuffer = memory.PrioritisedMemory(self.memorySize)
        self.pretrain()
        self.state = []
        self.trainingStepNo = 0
        self.newEpisode = False
        self.stepNo = 0
        self.episodeNo = 0
        self.saver = tf.compat.v1.train.Saver()
        # Load from existing model
        if load:
            self.episodeNo = load_from_episode_no
            self.saver.restore(self.sess, "./allModels/dqn/model{}/models/model.ckpt".format(self.episodeNo))
        else:
            self.sess.run(tf.compat.v1.global_variables_initializer())
        # Finalize is called to make a model read only
        # self.sess.graph.finalize()
        self.sess.run(self.update_target_graph())

    # This function helps us to copy one set of variables to another
    # In our case we use it when we want to copy the parameters of DQN to Target_network
    # Thanks of the very good implementation of Arthur Juliani https://github.com/awjuliani
    def update_target_graph(self):
        # Get the parameters of our DQNNetwork
        from_vars = tf.compat.v1.get_collection(tf.compat.v1.GraphKeys.TRAINABLE_VARIABLES, "DQNetwork")
        # Get the parameters of our Target_network
        to_vars = tf.compat.v1.get_collection(tf.compat.v1.GraphKeys.TRAINABLE_VARIABLES, "TargetNetwork")
        op_holder = []
        # Update our target_network parameters with DQNNetwork parameters
        for from_var, to_var in zip(from_vars, to_vars):
            op_holder.append(to_var.assign(from_var))
        return op_holder

    def pretrain(self):
        for i in range(self.pretrainLength):
            if i == 0:
                state = self.game.get_game_data()

            # pick a random movement and do it to populate the memory thing
            # choice = random.randInt(self.actionSize)
            # action = self.possibleActions[choice]
            action = random.choice(self.possibleActions)
            action_no = np.argmax(action)
            # Do something and see how it worked out
            self.game.action(number=action_no)
            reward = self.game.score
            self.game.next_tick()
            next_state = self.game.get_game_data()
            self.newEpisode = False
            if self.game.score < self.score_floor:              # If Hanz hits the game floor we do what my ex did.
                self.memoryBuffer.store((state, action, reward, next_state, True))
                self.game.reset()
                state = self.game.get_game_data()
                self.newEpisode = True
            else:
                self.memoryBuffer.store((state, action, reward, next_state, False))
                state = next_state
        print(colored("pretrainingDone", "blue"))

    def train(self):

        if self.trainingStepNo == 0 or self.newEpisode:
            self.state = self.game.get_game_data()

        if self.stepNo < self.maxSteps:
            self.stepNo += 1
            self.decayStep += 1
            self.trainingStepNo += 1
            self.tau += 1

            # choose best action if not exploring choose random otherwise

            epsilon = self.minEpsilon + (self.maxEpsilon - self.minEpsilon) * np.exp(
                -self.decayRate * self.decayStep)

            if np.random.rand() < epsilon:
                choice = random.randint(1, len(self.possibleActions)) - 1
                action = self.possibleActions[choice]

            else:
                q_values = self.sess.run(self.DQNetwork.output,
                                         feed_dict={self.DQNetwork.inputs_: np.array([self.state])})
                choice = np.argmax(q_values)
                action = self.possibleActions[choice]

            action_no = np.argmax(action)
            # now we need to get next state
            self.game.action(number=action_no)
            self.game.next_tick()
            reward = self.game.score
            next_state = self.game.get_game_data()

            if reward > 2000:
                print("Reward {}".format(reward))
            # if car is dead then finish episode
            finished = False
            if self.game.score < self.score_floor:
                self.stepNo = self.maxSteps
                finished = True
                print(colored("DEAD!", "red"))

            # print("Episode {} Step {} Action {} reward {} epsilon {} experiences stored {}"
            #       .format(self.episodeNo, self.stepNo, action_no, reward, epsilon, self.trainingStepNo))

            # add the experience to the memory buffer
            self.memoryBuffer.store((self.state, action, reward, next_state, finished))

            self.state = next_state

            # learning part
            # first we are gonna need to grab a random batch of experiences from out memory
            tree_indexes, batch, is_weights = self.memoryBuffer.sample(self.batchSize)

            states_from_batch = np.array([exp[0][0] for exp in batch])
            actions_from_batch = np.array([exp[0][1] for exp in batch])
            rewards_from_batch = np.array([exp[0][2] for exp in batch])
            next_states_from_batch = np.array([exp[0][3] for exp in batch])
            car_die_booleans_from_batch = np.array([exp[0][4] for exp in batch])
            target_qs_from_batch = []
            # predict the q values of the next state for each experience in the batch
            q_value_of_next_states = self.sess.run(self.TargetNetwork.output,
                                                   feed_dict={self.TargetNetwork.inputs_: next_states_from_batch})

            for i in range(self.batchSize):
                action = np.argmax(q_value_of_next_states[i])  # double DQN
                terminal_state = car_die_booleans_from_batch[i]
                if terminal_state:
                    target_qs_from_batch.append(rewards_from_batch[i])
                else:
                    # target = rewards_from_batch[i] + self.gamma * np.max(q_value_of_next_states[i])
                    target = rewards_from_batch[i] + self.gamma * q_value_of_next_states[i][action]  # double DQN
                    target_qs_from_batch.append(target)

            targets_for_batch = np.array([t for t in target_qs_from_batch])

            loss, _, absolute_errors = self.sess.run(
                [self.DQNetwork.loss, self.DQNetwork.optimizer, self.DQNetwork.absoluteError],
                feed_dict={self.DQNetwork.inputs_: states_from_batch,
                           self.DQNetwork.actions_: actions_from_batch,
                           self.DQNetwork.targetQ: targets_for_batch,
                           self.DQNetwork.ISWeights_: is_weights})

            # update priorities
            self.memoryBuffer.batchUpdate(tree_indexes, absolute_errors)

        if self.stepNo >= self.maxSteps:
            self.episodeNo += 1
            self.stepNo = 0
            self.newEpisode = True
            self.game.reset()
            if self.episodeNo >= self.totalTrainingEpisodes:
                self.training = False
            if self.episodeNo % 100 == 0:
                directory = "./allModels/dqn/{}/model{}".format(self.game.max_cars, self.episodeNo)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                # TODO: update path
                save_path = self.saver.save(self.sess,
                                            "./allModels/dqn/{}/model{}/models/model.ckpt".format(self.game.max_cars,
                                                                                                  self.episodeNo))
                print(colored("Model Saved", "blue"))
        if self.tau > self.maxTau:
            self.sess.run(self.update_target_graph())
            self.tau = 0
            print("Target Network Updated")

    def test(self):

        self.state = self.game.get_state()

        q_values = self.sess.run(self.DQNetwork.output,
                                 feed_dict={self.DQNetwork.inputs_: np.array([self.state])})
        choice = np.argmax(q_values)
        action = self.possibleActions[choice]

        action_no = np.argmax(action)
        # now we need to get next state
        self.game.action(number=action_no)

        if self.game.score < self.score_floor:
            self.game.reset()
