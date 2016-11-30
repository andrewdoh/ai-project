#Author: Toluwanimi Salako
from collections import defaultdict
import random
import sys
import time
import signal
sys.path.append(r'\ConnectKSource_python')
import ConnectKSource_python.board_model as boardmodel

team_name = "AndRod" #TODO change me

class TimeoutException(Exception):   # Custom exception class
	pass

def timeout_handler(signum, frame):   # Custom signal handler
    	raise TimeoutException

class StudentAI():
	def __init__(self, player, state):
		self.last_move = state.get_last_move()
		self.model = state
		self.user = player

	def get_available_moves(self, state):
		width = state.get_width()
		height = state.get_height()
		#stores the current state of the boardmodel as a key-value pair where (i, j) is the key
		# and value determines whether a location is taken
		spaces = defaultdict(int)

		for i in range(width):
			for j in range(height):
				#fills spaces with free spots and taken
				spaces[(i,j)] = state.get_space(i, j)

		#returns possible moves left for selection
		moves = [k for k in spaces.keys() if spaces[k] == 0]

		return moves

	#heuristic function needs work
	def heuristic_eval(self, state):
		'''Returns the winning spaces'''

		
	
		player_1_score  = 0
		player_2_score = 0

		height = state.get_height()
		width = state.get_width()

		# alternative heuristic
		goal = 5	# goal = K in ConnectK
		moves = self.get_available_moves(state)
	
	
		for i in range(height):	
			j = 1
			moveOn = False
			player1 = 0
			player2 = 0
			# space(0, i)
			if state.get_space(0, i) == -1:
				player2  += 10
			elif state.get_space(0, i) == 1:
				player1 += 10
			elif state.get_space(0, i) == 0:
				player1 += 1
				player2 += 1

			

			while(j < width and (not moveOn)):
				#hp1Count = 0
				#hp2Count = 0
				if state.get_space(j, i) not in moves:
					j += 1
					moveOn = True

				if state.get_space(j - 1, i) == -1:
					#player1 = 0
					player2 += 100
					#hp2count += 1
					#if(hp2count == 4 and (j + 1) < width):
						#player2 += 500
				
				elif state.get_space(j - 1, i) == 0:
					player1 += 1	
					player2 += 1

				elif state.get_space(j - 1, i) == 1:
					#player2 = 0
					player1 += 100
					#if(player2 >= 400 and (j + 1) < width):
						#player2 += 500

				if  i > 0 and state.get_space(j - 1, i - 1) == -1:
					player2 += 100

				elif i > 0 and state.get_space(j - 1, i - 1) == 1:
					player1 += 100

				if i > 0 and state.get_space(j + 1, i - 1) == -1:
					player2 += 100

				elif i > 0 and state.get_space(j + 1, i - 1) == 1:
					player1 += 100

				player_1_score += player1
				player_2_score += player2
				j += 1	
		
		for j in range (width):
			player1 = 0
			player2 = 0
			i = 0
			moveRight = False
			if state.get_space(j, 0) == -1:
				player2 += 100
			elif state.get_space(j, 0) == 1:
				player1 += 100
			elif state.get_space(j, 0) == 0:
				player1 += 1
				player2 += 1		
			
			while(i < height and (not moveRight)):
				if state.get_space(j, i) not in moves:
					i += 1
					moveRight = True	
			
				if state.get_space(j, i - 1) == -1:
					player2 += 100
					#if player1 >= 400 and (i + 1) < height:
						#player1 += 500
				elif state.get_space(j, i - 1) == 0:
					player1 += 1
					player2 += 2

				elif state.get_space(j, i - 1) == 1:
					player1 += 100
					#if player2 >= 400 and (i + 1) < height:
						#player2 += 500
				i += 1

				player_1_score += player1
				player_2_score += player2
	
		print('player 1 score: ', player_1_score)
		print('player 2 score: ', player_2_score)
		return(player_1_score - player_2_score)	

			

"""
		for i in range(height):
			has_1 = False
			has_2 = False
			#print ('cupcake')
			for j in range(width):

				if state.get_space(j, i) == 1:
					has_1 = True
				elif state.get_space(j, i) == -1:
					has_2 = True

			if has_1 and not has_2:
				player_1_score += 100
			elif not has_1 and has_2:
				player_2_score += 100
			elif not has_1 and not has_2:
				player_1_score += 100
				player_2_score += 100

	
		for k in range(width):

			has_1_up = False
			has_2_up = False
			for l in range(height):

				if state.get_space(k, l) == 1:
					has_1_up = True
				elif state.get_space(k, l) == -1:
					has_2_up = True
			if has_1_up and not has_2_up:
				player_1_score += 100
			elif not has_1_up and has_2_up:
				player_2_score += 100
			elif not has_1_up and not has_2_up:
				player_1_score += 100
				player_2_score += 100

			#print('player 1 score: ')
			#print(player_1_score)
			#print('player 2 score: ')
			#print(player_2_score)
		#print ('player difference')
	
		#print (player_1_score - player_2_score)

		return (player_1_score - player_2_score)
		#return random.randint(-9999, 9999)
	"""

	def min_max(self, state, depth, alpha, beta, maximizing):
		# if depth zero we reached limit or we have no more moves left
		if depth == 0 or not state.has_moves_left():
			#print ('THE END')
			#use heuristic to determine quality of play
			return self.heuristic_eval(state), None

		if maximizing: #maximizing player

			#fill actions list with possible moves
			actions = self.get_available_moves(state)


			#apply every possible action in actions to state
			#print('waffles')
			#print('actions')
			#print (len(actions))
			#print('actions')
			#print(actions)
			best_action = actions[0]
			for action in actions:
				#clone board and apply every action in actions
				clone = state.clone()
				nextState = clone.place_piece(action, 1 if self.user == 1 else -1)
				#print(nextState)
				#recurse
				#print('poptart')
				v = self.min_max(nextState, depth - 1, alpha, beta, False)


				#find highest value
				#print('action')
				#print(action)
				#print('alpha: ')
				#print(alpha)
				#print('beta: ')
				#print(beta)
				#print('v: ')
				#print(v[0])
				#print('action: ')
				#print(v[1])
				if v[0] > alpha:
					best_action = action
					alpha = v[0]
					#print('wolf')
					#print(best_action)
				if alpha >= beta:
					break
			#print('brownie')
			#print('alpha')
			#print(alpha)
			#print('best action: ')
			#print(best_action)
			return alpha,best_action

		else: #minimizing player

			actions = self.get_available_moves(state)


			#apply every possible action in actions to state

			#print('pancakes')
			#print('actions length: ')
			#print (len(actions))
			#print('actions')
			#print(actions)
			best_action = actions[0]
			for action in actions:

				#clone board and apply every action in actions
				clone = state.clone()
				nextState = clone.place_piece(action, -1 if self.user == 1 else 1)
				#print(nextState)
				#recurse
				v = self.min_max(nextState, depth - 1, alpha, beta, True)

				#print('action')
				#print(action)
				#print('alpha: ')
				#print(alpha)
				#print('beta: ')
				#print(beta)
				#print('v: ')
				#print(v[0])

				#find lowest value
				if v[0] < beta:
					best_action = action
					beta = v[0]
				if beta <= alpha:
					break
			#print('yolo')
			#print(beta)
			#print('best action: ')
			#print(best_action)
			return beta,best_action


	def make_move(self, deadline):
		'''Write AI Here. Return a tuple (col, row)'''
		#print ('hello')
		#returns randomly selected location in move
		#moves = self.get_available_moves()
		#return moves[random.randint(0, len(moves) - 1)]

		#return min_max which selects best possible move within depth d
		best_action_dict = []
		signal.signal(signal.SIGALRM, timeout_handler)



		#depth = 1
		t = time.process_time()
		elapsed_time = 0
		signal.alarm(deadline)
		for depth in range(1, 99999):

			try:
				tup = self.min_max(self.model, depth, -99999, 99999, True)
				best_action_dict.append(tup)
				#depth += 1
				elapsed_time = time.process_time() - t
				print('elapsed_time: ', elapsed_time)
				print('brownie')
				print(best_action_dict)
				print('max')
				print(max(best_action_dict))
				print(max(best_action_dict)[1])
				print('cheesecake')

			except TimeoutException:
				print("TIMEOUT")
				break






		print('depth ended at: ')
		print(depth)
		elapsed_time = time.process_time() - t
		print('total elapsed_time: ', elapsed_time)
		print ('TUP')
		print (tup)
		print(tup[1])
		best_move = (max(best_action_dict)[1])
		print(best_move)
		return best_move

'''===================================
DO NOT MODIFY ANYTHING BELOW THIS LINE
==================================='''

is_first_player = False
deadline = 5

def make_ai_shell_from_input():
	'''
	Reads board state from input and returns the move chosen by StudentAI
	DO NOT MODIFY THIS
	'''
	global is_first_player
	ai_shell = None
	begin =  "makeMoveWithState:"
	end = "end"

	go = True
	while (go):
		mass_input = input().split(" ")
		if (mass_input[0] == end):
			sys.exit()
		elif (mass_input[0] == begin):
			#first I want the gravity, then number of cols, then number of rows, then the col of the last move, then the row of the last move then the values for all the spaces.
			# 0 for no gravity, 1 for gravity
			#then rows
			#then cols
			#then lastMove col
			#then lastMove row.
			#then deadline.
			#add the K variable after deadline.
			#then the values for the spaces.
			#cout<<"beginning"<<endl;
			gravity = int(mass_input[1])
			col_count = int(mass_input[2])
			row_count = int(mass_input[3])
			last_move_col = int(mass_input[4])
			last_move_row = int(mass_input[5])

			#add the deadline here:
			deadline = -1
			deadline = int(mass_input[6])
			k = int(mass_input[7])
			#now the values for each space.


			counter = 8
			#allocate 2D array.
			model = boardmodel.BoardModel(col_count, row_count, k, gravity)
			count_own_moves = 0

			for col in range(col_count):
				for row in range(row_count):
					model.pieces[col][row] = int(mass_input[counter])
					if (model.pieces[col][row] == 1):
						count_own_moves += model.pieces[col][row]
					counter+=1

			if (count_own_moves % 2 == 0):
				is_first_player = True

			model.last_move = (last_move_col, last_move_row)
			ai_shell = StudentAI(1 if is_first_player else 2, model)

			return ai_shell
		else:
			print("unrecognized command", mass_input)
		#otherwise loop back to the top and wait for proper _input.
	return ai_shell

def return_move(move):
	'''
	Prints the move made by the AI so the wrapping shell can input it
	DO NOT MODIFY THIS
	'''
	made_move = "ReturningTheMoveMade";
	#outputs made_move then a space then the row then a space then the column then a line break.
	print(made_move, move[0], move[1])

def check_if_first_player():
	global is_first_player
	return is_first_player

if __name__ == '__main__':
	'''
	DO NOT MODIFY THIS
	'''
	print ("Make sure this program is ran by the Java shell. It is incomplete on its own. :")
	go = True
	while (go): #do this forever until the make_ai_shell_from_input function ends the process or it is killed by the java wrapper.
		ai_shell = make_ai_shell_from_input()
		moveMade = ai_shell.make_move(deadline)
		return_move(moveMade)
		del ai_shell
		sys.stdout.flush()
