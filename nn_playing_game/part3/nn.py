import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.utils.np_utils import to_categorical
import numpy as np
from random import randint

import matplotlib.pyplot as plt

from game import controlled_run

# importing static variables
from game import DO_NOTHING
from game import JUMP

# variables for limiting the number of games we play
total_number_of_games = 100
games_count = 0

# The neural network training data
x_train = np.array([])
y_train = np.array([])

really_huge_number = 1000

# How frequently we train the neural network
train_frequency = 10

# The actual neural network
model = Sequential()
model.add(Dense(1, input_dim=1, activation='sigmoid'))
model.add(Dense(2, activation='softmax'))
model.compile(Adam(lr=0.1), loss='categorical_crossentropy', metrics=['accuracy'])

plt.subplots(ncols=1, nrows=3)

class Wrapper(object):

	def __init__(self):
		# Start the game
		controlled_run(self, 0)

	def control(self, values):
		global x_train
		global y_train

		global games_count

		global model

		# This is the function that is called by the game.
		# The values dict contains important information
		# that we will need to use to train and predict
		print (values)

		# There are no enemies right now, so let's ignore the call
		if values['closest_enemy'] == -1:
			return DO_NOTHING

		if values['old_closest_enemy'] is not -1:
			if values['score_increased'] == 1:
				x_train = np.append(x_train, [values['old_closest_enemy']/really_huge_number])
				y_train = np.append(y_train, [values['action']])

		# Let's ask for input
		# print ("Enter 1 for JUMP and 0 for DO_NOTHING")
		# action = int(input())

		# The prediction from neural network
		prediction2 = model.predict(np.array([values['closest_enemy']/really_huge_number]))
		prediction = model.predict_classes(np.array([[values['closest_enemy']/really_huge_number]]))

		r = randint(0, 100)

		random_rate = 50*(1-games_count/50)

		if r < random_rate:
			if prediction == DO_NOTHING:
				return JUMP
			else:
				return DO_NOTHING
		else:
			if prediction == JUMP:
				return JUMP
			else:
				return DO_NOTHING

	def gameover(self, score):
		global games_count
		global x_train
		global y_train 
		global model

		games_count += 1

		# Printing x_train and y_train
		print(x_train)
		print(y_train)

		if games_count is not 0 and games_count % train_frequency is 0:
			# Before training, let's make the y_train array categorical
			y_train_cat = to_categorical(y_train, num_classes = 2)

			print(x_train)

			# Let's train the network
			model.fit(x_train, y_train_cat, epochs = 50, verbose=1, shuffle=1)

			# Reset x_train and y_train
			x_train = np.array([])
			y_train = np.array([])

		if games_count>=total_number_of_games:
			# Let's exit the program now
			return

		# Let's start another game!
		controlled_run(self, games_count)

if __name__ == '__main__':
	w = Wrapper()
