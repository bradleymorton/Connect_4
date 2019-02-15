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
		self.board[self.lastMoveRow][self.lastMoveCol]=0


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




def randomMove(board, player):
	moves = board.returnValidMoves()
	while True:
		i = random.randint(0, 6)
		if moves[i] == -1:
			continue
		board.makeMove(i, player)
		break





def lowHangingFruit(board, player):
	moves = board.returnValidMoves()
	for i in range(6):
		board.makeMove(i, player)
		if board.getWinner():
			break
		board.undo()
		other = (player + 1) % 2
		board.makeMove(i, other)
		if board.getWinner():
			board.undo()
			board.makeMove(i, player)
			break
		while True:
			i = random.randint(0, 6)
			if moves[i] == -1:
				continue
			board.makeMove(i, player)
			break



def rankedMoves(board, player):
	moves = board.returnValidMoves()
	for i in range(6):
		board.makeMove(i, player)
		if board.getWinner():
			break
		board.undo()
		other = (player + 1) % 2
		board.makeMove(i, other)
		if board.getWinner():
			board.undo()
			board.makeMove(i, player)
			break

	currentThree = board.threeInRow(player)
	rank = [0, 0, 0, 0, 0, 0, 0]
	for i in range(6):
		rank[i] = ranker(board, i, player, currentThree)

	current = 0
	for i in range(6):
		if rank[i] > rank[current]:
			current = i
	board.makeMove(current, player)




def ranker(board, col, player, currentThree):
	total = 0
	if col == 0 or col == 6:
		total += 0
	if col == 1 or col == 5:
		total += 3
	if col == 2 or col == 4:
		total += 6
	if col == 3:
		total +=9

	board.makeMove(col, player)
	greaterThrees = board.threeInRow(player) - currentThree
	total += 500* board.optimalThreeInRow(player)
	board.undo()
	total += 3*greaterThrees

	return total


def userPlays(board, player)
print("You are player "+str(player))





board = Environment()
turn =  1
player_1 = 0
player_2 = 0
tie = 0
for i in range(1):
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
			#This is how you determine which agent plays as player one. 
			rankedMoves(board, 1)
			done = board.getWinner()
			if done == 1:
				#print("player 1 wins")
				player_1 += 1
				break




		if turn%2 == 0:
			#This is how you pick which agent is player two. 
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
