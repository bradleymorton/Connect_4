#Created 2/8/19 by Bradley Morton for CS405 assignment
#Much of the code has been taken from Dr. Metzgar with permission.
import random


class Environment:
	def __init__(self):
		self.board = [[0 for i in range(7)] for j in range(6)]
		self.width = 7
		self.height = 6
		self.lastMoveCol = 0
		self.lastMoveRow = 0



	def reset(self):
		for j in range(6):
			for i in range(7):
				self.board[j][i] = 0


	def get(self, col, row):
		if row < 0 or row > 5:
			return 0
		if col < 0 or col > 6:
			return 0
		return self.board[row][col]

	def put(self, col, row, piece):
		if row < 0 or row > 5:
			return
		if col < 0 or col > 6:
			return
		self.lastMove = (col, row, piece)
		self.board[row][col] = piece


	def makeMove(self, col, player):
		moves = self.returnValidMoves()
		if moves[col] != -1:
			self.put(col, moves[col], player)
		lastMoveCol = col
		lastMoveRow = moves[col]


	def returnValidMoves(self):
		moves = [-1, -1, -1, -1, -1, -1, -1]
		for i in moves:
			for j in range(5):
				if self.get(i, j) == 0:
					moves[i]=j
		return moves



	def undo(self):
		self.board[lastMoveRow][lastMoveCol]=0

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




def randomMove(Environment, player):
	moves = Environment.returnValidMoves()
	while True:
		i = random.randint(0, 6)
		if moves[i] == -1:
			continue
		Environment.makeMove(i, player)
		break





def lowHangingFruit(board, player):
	moves = board.returnValidMoves()
	for i in range(6):
		board.makeMove(board, i, player)
		if board.getWinner():
			break
		board.undo()











board = Environment()
turn =  1
player_1 = 0
player_2 = 0
tie = 0
for i in range(1000):
	while True:
		moves = board.returnValidMoves()
		numAvailable = 0
		for j in range(6):
			if moves[j] != -1:
				numAvailable +=1
		if numAvailable == 0:
			#print("no winner")
			tie += 1
			break


		if turn%2 == 1:
			#print("player 1 going")
			randomMove(board, 1)
			done = board.getWinner()
			if done == 1:
				#print("player 1 wins")
				player_1 += 1
				break




		if turn%2 == 0:
			#print("player 2 going")
			randomMove(board, 2)
			done = board.getWinner()
			if done == 2:
				#print("player 2 wins")
				player_2 += 1
				break

		turn += 1
		
	board.reset()
	turn = 1

print("player 1 wins "+ str(player_1) +" times, \nplayer 2 wins " + str(player_2) + " times, \nwith "+str(tie) +" ties")
