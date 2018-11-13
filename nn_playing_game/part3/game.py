import pygame
import random
import copy

from Enemy import Enemy
import Player as Player
from Collision import check_collision_between_polygons

# Static variables
enemy_prob = 100
enemies = []
min_time_between_enemies = 200
current_time_since_last_enemy = 0

# static variables
JUMP = 1
DO_NOTHING = 0

score = 0

gameEnded = False

controlled = False

increase_counter_divide = 2
increase_counter_max = ((Player.Player.jump_height / Player.Player.jump_speed) * 2 + 2)/increase_counter_divide
increase_counter = 0

# The game should be able to execute an action given by the neural network
# This means that it should wait a while before another action can be accepted
# This is handled by the next set of variables
action_duration = ((Player.Player.jump_height / Player.Player.jump_speed) * 2 + 2)/increase_counter_divide
action_counter = 0

clock_tick = 250

def check_collisions(player, enemies):
	for enemy in enemies:
		collision(player, enemy)

def collision(player, enemy):
	global gameEnded

	polygon1 = [(player.x, player.y), (player.x+player.width, player.y), (player.x+player.width, player.y+player.height), (player.x, player.y+player.height)]
	polygon2 = [(enemy.x, enemy.y), (enemy.x-enemy.base/2, enemy.y+enemy.height), (enemy.x+enemy.base/2, enemy.y+enemy.height)]
	# SAT
	if check_collision_between_polygons(polygon1, polygon2):
		gameEnded = True

def check_if_enemy_passed_player(player, enemies):
	global score

	for enemy in enemies:
		if player.x>enemy.x+Enemy.base:
			if not enemy.scoreUpdated:
				score+=1
				enemy.scoreUpdated=True
		if enemy.x<0:
			enemies.remove(enemy)

def update(display, player):
	global current_time_since_last_enemy
	global score
	global increase_counter
	global increase_counter_max

	# TODO: player.inair is broken

	if player.inair:
		increase_counter = 0

	if not player.inair and len(enemies)>=0:
		if increase_counter<increase_counter_max:
			increase_counter += 1
		else:
			increase_counter = 0
			score += 1


	check_collisions(player, enemies)

	draw_static(display, player)
	player.draw_it(display)
	for e in enemies:
		e.draw_it(display)

	if current_time_since_last_enemy>min_time_between_enemies:
		if random.randint(0, enemy_prob-1) == 0:
			e = Enemy()
			enemies.append(e)
			current_time_since_last_enemy = 0
	else:
		current_time_since_last_enemy += 1

	player.update()
	for e in enemies:
		e.update()

	check_if_enemy_passed_player(player, enemies)

	myfont = pygame.font.SysFont('Comic Sans MS', 30)
	textsurface = myfont.render(str(score), False, (0, 0, 0))
	display.blit(textsurface,(0,0))	


def draw_static(display, player):
	display.fill(white)

	pygame.draw.rect(display, red, (0, 400+player.height, width, height-400))

# Colors etc
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)

width, height = 800, 600	

def run():
	global score
	global gameEnded
	global player
	global enemies

	global clock_tick

	enemies = []

	# boiler plate stuff
	gameEnded = False
	pygame.init()
	pygame.font.init()
	caption = 'Doing something'
	gameDisplay = pygame.display.set_mode((width, height))
	pygame.display.set_caption(caption)
	clock = pygame.time.Clock()
	crashed = False

	player = Player.Player()

	# Initial filling
	gameDisplay.fill(white)
	score=0

	# Main game loop
	while not crashed and not gameEnded:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				crashed = True
			elif event.type == pygame.KEYDOWN:
				if event.key==32:
					player.jump()
				elif event.key == 119:
					clock_tick += 25
				elif event.key == 115:
					clock_tick -= 25

		update(gameDisplay, player)

		pygame.display.update()
		clock.tick(clock_tick)

	pygame.quit()
	quit()


old_response = None

def controlled_run(wrapper, counter):
	global score
	global gameEnded
	global player
	global enemies

	global action_counter
	global action_duration

	global clock_tick

	enemies = []

	# boiler plate stuff
	gameEnded = False
	pygame.init()
	pygame.font.init()
	caption = 'Doing something '+str(counter)
	gameDisplay = pygame.display.set_mode((width, height))
	pygame.display.set_caption(caption)
	clock = pygame.time.Clock()
	crashed = False

	player = Player.Player()

	# Initial filling
	gameDisplay.fill(white)
	score=0

	# When an action is recieved, score is saved here and used when 
	# a new action is needed
	old_score = 0

	old_action = None
	old_closest_enemy = None

	# values = dict()
	# Main game loop
	while not crashed and not gameEnded:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				crashed = True
			elif event.type == pygame.KEYDOWN:
				if event.key == 119:
					clock_tick += 25
				elif event.key == 115:
					clock_tick -= 25

		# 1. Check whether a new action can be taken or not
		if action_counter<action_duration or player.inair:
			# A new action cannot be taken
			# Nothing more should be done
			action_counter += 1

			update(gameDisplay, player)
			pygame.display.update()
			clock.tick(clock_tick)

		else:
			# A new action can be taken
			action_counter = 0

			update(gameDisplay, player)

			new_score = copy.deepcopy(score)
			score_increased = 0

			if new_score>old_score:
				score_increased = 1

			values = dict()

			if old_action is None:
				values['action'] = DO_NOTHING
			else:
				values['action'] = old_action

			if old_closest_enemy is None:
				values['old_closest_enemy'] = -1
			else:
				values['old_closest_enemy'] = old_closest_enemy

			if len(enemies)>0:
				closest_enemy = 1000
				for enemy in enemies:
					if enemy.x>player.x and enemy.x<closest_enemy:
						closest_enemy = enemy.x
				values['closest_enemy'] = closest_enemy
			else:
				values['closest_enemy'] = -1

			values['score_increased'] = score_increased

			response = wrapper.control(values)

			# Only take new action if the player can accept the action
			# i.e. it is not in air
			if not player.inair:
				old_action = response

			if response == JUMP:
				player.jump()
			elif response == DO_NOTHING:
				pass

			old_score = new_score
			old_closest_enemy = values['closest_enemy']

	# pygame.quit()
	# quit()

	wrapper.gameover(score)

if __name__ == '__main__':
	run()