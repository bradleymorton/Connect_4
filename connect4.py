#Created 2/8/19 by Bradley Morton for CS405 assignment
#Much of the code has been taken from Dr. Metzgar with permission.
import random
from copy import deepcopy

class Move:
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Environment:
	def __init__(self):
		self.board = [[0 for i in range(10)] for j in range(10)]
		self.width = 10
		self.height = 10
		self.lastMoves =[Move(0,0)]
		self.moves = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]



	def reset(self):
		for j in range(10):
			for i in range(10):
				self.board[j][i] = 0


	def get(self, col, row):
		if row < 0 or row > 9:
			return 0
		if col < 0 or col > 9:
			return 0
		return self.board[row][col]

	def put(self, col, row, piece):
		if row < 0 or row > 9:
			return
		if col < 0 or col > 9:
			return
		self.board[row][col] = piece


	def actuator(self, col, player):
		self.sensor()
		if self.moves[col] != -1:
			self.put(col, self.moves[col], player)
		self.lastMoves.append(Move(self.moves[col], col))


	def sensor(self):
		self.moves = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
		for i in range(10):
			if (i-self.lastMoves[-1].y)>2 or (i-self.lastMoves[-1].y)< -2:
				continue
			for j in range(10):
					if self.get(i, j) == 0:
						self.moves[i]=j



	def undo(self):
		self.board[self.lastMoves[-1].x][self.lastMoves[-1].y]=0
		self.lastMoves.pop()



	def twoInRow(self, player):
		total = 0
		for j in range(self.height):
			for i in range(self.width):
				p = self.get(i, j)
				if p == 0:
					continue

                # check horizontal
				h2 = self.get(i+1, j)
				if player == h2 and h2 == h3:
					total += 1

                # check vertical
				v2 = self.get(i, j+1)
				if player == v2 and v2 == v3:
					total += 1

                # check diagonal
				d2 = self.get(i+1, j+1)
				if player == d2 and d2 == d3:
					total += 1

                # check reverse diagonal
				d2 = self.get(i-1, j+1)
				if player == d2 and d2 == d3:
					total += 1

			return total

	def threeInRow(self, player):
		total = 0
		for j in range(self.height):
			for i in range(self.width):
				p = self.get(i, j)
				if p == 0:
					continue

                # check horizontal
				h2 = self.get(i+1, j)
				h3 = self.get(i+2, j)
				if player == h2 and h2 == h3:
					total += 1

                # check vertical
				v2 = self.get(i, j+1)
				v3 = self.get(i, j+2)
				if player == v2 and v2 == v3:
					total += 1

                # check diagonal
				d2 = self.get(i+1, j+1)
				d3 = self.get(i+2, j+2)
				if player == d2 and d2 == d3:
					total += 1

                # check reverse diagonal
				d2 = self.get(i-1, j+1)
				d3 = self.get(i-2, j+2)
				if player == d2 and d2 == d3:
					total += 1

			return total

	def optimalThreeInRow(self, player):
		total = 0
		for j in range(self.height):
			for i in range(self.width):
				p = self.get(i, j)
				if p == 0:
					continue

                # check horizontal
				h0 = self.get(i-1, j)
				h2 = self.get(i+1, j)
				h3 = self.get(i+2, j)
				h4 = self.get(i+3, j)
				if player == h2 and h2 == h3 and h0 == 0 and h4 == 0 and i > 0 and i <6:
					total += 1

                # check vertical
				v2 = self.get(i, j+1)
				v3 = self.get(i, j+2)
				if player == v2 and v2 == v3:
					total += 1

                # check diagonal
				d0 = self.get(i-1, j-1)
				d2 = self.get(i+1, j+1)
				d3 = self.get(i+2, j+2)
				d4 = self.get(i+3, j+3)
				if player == d2 and d2 == d3 and d0 == 0 and d4 == 0 and i>0 and j <5:
					total += 1

                # check reverse diagonal
				d0 = self.get(i+1, j-1)
				d2 = self.get(i-1, j+1)
				d3 = self.get(i-2, j+2)
				d4 = self.get(i-3, j+3)
				if player == d2 and d2 == d3 and d0 == 0 and d4 == 0:
					total += 1

			return total


	def fourInRow(self, player):
		count = 0
		for j in range(self.height):
			for i in range(self.width):
                # check horizontal
				h2 = self.get(i+1, j)
				h3 = self.get(i+2, j)
				h4 = self.get(i+3, j)
				if player == h2 and h2 == h3 and h3 == h4:
					count += 1

                # check vertical
				v2 = self.get(i, j+1)
				v3 = self.get(i, j+2)
				v4 = self.get(i, j+3)
				if player == v2 and v2 == v3 and v3 == v4:
					count += 1

                # check diagonal
				d2 = self.get(i+1, j+1)
				d3 = self.get(i+2, j+2)
				d4 = self.get(i+3, j+3)
				if player == d2 and d2 == d3 and d3 == d4:
					count += 1

                # check reverse diagonal
				d2 = self.get(i-1, j+1)
				d3 = self.get(i-2, j+2)
				d4 = self.get(i-3, j+3)
				if player == d2 and d2 == d3 and d3 == d4:
					count += 1
		return count


	def getWinner(self):
		'''checks to see if Connect 4 has been won'''

		for j in range(self.height):
			for i in range(self.width):
				p = self.get(i, j)
				if p == 0:
					continue

                # check horizontal
				h2 = self.get(i+1, j)
				h3 = self.get(i+2, j)
				h4 = self.get(i+3, j)
				if p == h2 and h2 == h3 and h3 == h4:
					return p

                # check vertical
				v2 = self.get(i, j+1)
				v3 = self.get(i, j+2)
				v4 = self.get(i, j+3)
				if p == v2 and v2 == v3 and v3 == v4:
					return p

                # check diagonal
				d2 = self.get(i+1, j+1)
				d3 = self.get(i+2, j+2)
				d4 = self.get(i+3, j+3)
				if p == d2 and d2 == d3 and d3 == d4:
					return p

                # check reverse diagonal
				d2 = self.get(i-1, j+1)
				d3 = self.get(i-2, j+2)
				d4 = self.get(i-3, j+3)
				if p == d2 and d2 == d3 and d3 == d4:
					return p




def randomMovesAgent(board, player):
	board.sensor()
	while True:
		i = random.randint(0, 9)
		if board.moves == -1:
			continue
		board.actuator(i, player)
		break






def lowHangingFruitAgent(board, player):
	print("calling lowHangingFruitAgent")
	board.sensor()
	for i in range(10):
		board.actuator(board.moves[i], player)
		if board.getWinner():
			print("finishing lowHangingFruitAgent")
			break
		board.undo()
		other = (player + 1) % 2
	for i in range(10):
		board.actuator(board.moves[i], other)
		if board.getWinner():
			board.undo()
			board.actuator(i, player)
			print("finishing lowHangingFruitAgent")
			break
		board.undo()
	while True:
		i = random.randint(0, 9)
		if board.moves[i] == -1:
			continue
			board.actuator(i, player)
			print("finishing lowHangingFruitAgent")
			break



def rankedMovesAgent(board, player):
	percepts = board.sensor()
	for i in range(10):
		board.actuator(i, player)
		if board.getWinner():
			break
		board.undo()
		other = (player + 1) % 2
		board.actuator(i, other)
		if board.getWinner():
			board.undo()
			board.actuator(i, player)
			break

	currentThree = board.threeInRow(player)
	rank = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	for i in range(6):
		rank[i] = ranker(board, i, player, currentThree)

	current = 0
	for i in range(10):
		if rank[i] > rank[current]:
			current = i
	board.actuator(current, player)




def ranker(board, col, player, currentThree):
	total = 0
	if col == 0 or col == 9:
		total += 0
	if col == 1 or col == 8:
		total += 3
	if col == 2 or col == 7:
		total += 6
	if col == 3 or col == 6:
		total += 9
	if col == 4 or col == 5:
		total += 12

	board.actuator(col, player)
	greaterThrees = board.threeInRow(player) - currentThree
	total += 500* board.optimalThreeInRow(player)
	board.undo()
	total += 3*greaterThrees

	return total


def printBoard(board):
	for i in range(10):
		for j in range(10):
			print(board.get(j, i), end = '')
		print()





def humanPlayerAgent(board, player):
	printBoard(board)
	percepts= board.sensor()
	print("Your valid moves are:")
	for i in range(10):
		if percepts[i] == -1:
			continue
		print("("+str(i)+ ", ", str(percepts[i]), "), ", end = '')

	print("")
	while True:
		move = int(input("What is your move?"))
		if move <0 or move >9:
			continue
		if percepts[move] == -1:
			continue
		break
	board.actuator(move, player)





def lookAHead(board, player):
	move = minimax(board, player, 6)
	print("actuator being called at "+str(move))
	board.actuator(move, player)
	print(str(board.lastMoves[-1].x)+" "+str(board.lastMoves[-1].y))
	


def minimax(board, player, depth):
	#print("calling minimax")
	board.sensor()
	bestMove = board.moves[0]
	bestScore = -5000000
	print(board.moves)
	for i in range(10):
		board.sensor()
		if board.moves[i] == -1:
			continue
		board.actuator(i, player)
		score = maxPlay(board, player, depth)
		board.undo()	
		if score > bestScore:
			bestMove = i
			bestScore = score
	return bestMove



def maxPlay(board, player, depth):
	#print("calling maxPlay at a current depth of "+str(depth))
	if board.getWinner() or depth == 0:
		return scoreBoard(board, player)
	board.sensor()
	bestScore = -5000000
	bestMove = 0
	for i in range(10):
		if board.moves[i] == -1:
			continue
		board.actuator(i, player)
		score = minPlay(board, player, depth -1)
		board.undo()
		if score > bestScore:
			bestMove = i
			bestScore = score
	return bestScore



def minPlay(board, player, depth):
	#print("calling minPlay at a current depth of "+str(depth))
	other = (player+1)%2
	if board.getWinner() or depth == 0:
		return scoreBoard(board, other)
	board.sensor()
	bestScore = -5000000
	bestMove = 0
	other = (player+1)%2
	for i in range(10):
		if board.moves[i] == -1:
			continue
		board.actuator(i, other)
		score = maxPlay(board, player, depth -1)
		board.undo()
		if score > bestScore:
			bestMove = i
			bestScore = score
	return bestScore

def scoreBoard(board, player):
	total = 0
	other = (player+1)%2
	total += (board.threeInRow(player)-board.threeInRow(other))*5
	total += (board.fourInRow(player)-board.fourInRow(other))*500
	return total



def lookAHead2(board, player):
	move = minimax2(board, player, 6)
	print("actuator being called at "+str(move))
	board.actuator(move, player)
	print(str(board.lastMoves[-1].x)+" "+str(board.lastMoves[-1].y))
	


def minimax2(board, player, depth):
	#print("calling minimax")
	board.sensor()
	bestMove = board.moves[0]
	bestScore = -5000000
	print(board.moves)
	for i in range(10):
		board.sensor()
		if board.moves[i] == -1:
			continue
		board.actuator(i, player)
		score = maxPlay2(board, player, depth)
		board.undo()	
		if score > bestScore:
			bestMove = i
			bestScore = score
	return bestMove



def maxPlay2(board, player, depth):
	#print("calling maxPlay at a current depth of "+str(depth))
	if board.getWinner() or depth == 0:
		return scoreBoard(board, player)
	board.sensor()
	bestScore = -5000000
	bestMove = 0
	for i in range(10):
		if board.moves[i] == -1:
			continue
		board.actuator(i, player)
		score = minPlay2(board, player, depth -1)
		board.undo()
		if score > bestScore:
			bestMove = i
			bestScore = score
	return bestScore



def minPlay2(board, player, depth):
	#print("calling minPlay at a current depth of "+str(depth))
	other = (player+1)%2
	if board.getWinner() or depth == 0:
		return scoreBoard(board, other)
	board.sensor()
	bestScore = -5000000
	bestMove = 0
	other = (player+1)%2
	for i in range(10):
		if board.moves[i] == -1:
			continue
		board.actuator(i, other)
		score = maxPlay2(board, player, depth -1)
		board.undo()
		if score > bestScore:
			bestMove = i
			bestScore = score
	return bestScore

def scoreBoard2(board, player):
	total = 0
	other = (player+1)%2
	#total += (board.twoInRow(player)-board.twoInRow(other))*30
	#total += (board.threeInRow(player)-board.threeInRow(other))*10
	total += (board.fourInRow(player)-board.fourInRow(other))*500
	return total








board = Environment()
'''
board.actuator(0,1)
board.actuator(0,1)
board.undo()
board.undo()
printBoard(board)

board.sensor()
print(board.moves)

'''
turn =  1
player_1 = 0
player_2 = 0
tie = 0
for i in range(1):
	while True:
		board.sensor()
		numAvailable = 0
		for j in range(10):
			if board.moves[j] != -1:
				numAvailable +=1
		if numAvailable == 0:
			print("no winner")
			printBoard(board)
			print(board.moves)
			tie += 1
			break


		if turn%2 == 1:
			#This is how you determine which agent plays as player one. 
			lookAHead(board, 1)
			done = board.getWinner()
			if done == 1:
				print("player 1 wins")
				printBoard(board)
				player_1 += 1
				break




		if turn%2 == 0:
			#This is how you pick which agent is player two. 
			lookAHead2(board, 2)
			done = board.getWinner()
			if done == 2:
				print("player 2 wins")
				printBoard(board)
				player_2 += 1
				break

		turn += 1

		printBoard(board)
		print("")

	board.reset()
	turn = 1

print("player 1 wins "+ str(player_1) +" times, \nplayer 2 wins " + str(player_2) + " times, \nwith "+str(tie) +" ties")
