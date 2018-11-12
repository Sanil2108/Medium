from game import controlled_run

# importing static variables
from game import DO_NOTHING
from game import JUMP

# variables for limiting the number of games we play
total_number_of_games = 5
games_count = 0

class Wrapper(object):
	# Some static variables that we will use later

	def __init__(self):
		# Start the game
		controlled_run(self, 0)

	def control(self, values):
		# This is the function that is called by the game.
		# The values dict contains important information
		# that we will need to use to train and predict
		print (values)

		# Let's ask for input
		print ("Enter 1 for JUMP and 0 for DO_NOTHING")
		action = int(input())

		return action

	def gameover(self, score):
		global games_count
		games_count += 1

		if games_count>=total_number_of_games:
			# Let's exit the program now
			return

		# Let's start another game!
		controlled_run(self, games_count)

if __name__ == '__main__':
	w = Wrapper()