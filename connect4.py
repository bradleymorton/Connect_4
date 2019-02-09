#Created 2/8/19 by Bradley Morton for CS405 assignment
#Much of the code has been taken from Dr. Metzgar with permission.

class Environment:
	def __init__(self):
		self.board = [[0 for i in range(7)] for j in range(6)]
		self.width = 7
		self.height = 6
		self.lastMove = (0, 0, 0)



	def reset(self):
		for j in range(6):
			for i in range(7):
				self.board[j][i] = 0


	def get(self, col, row):
		if row < 0 or row > 6:
			return 0
		if col < 0 or col > 7:
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
		moves = returnValidMoves
		if moves[col] != -1:
			put(col, moves[col], player)



	def returnValidMoves(self):
		moves = [-1, -1, -1, -1, -1, -1, -1]
		for i in moves:
			for j in range(5):
				if get(i, j) == 0:
					passmoves[i]=j
		return moves



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




def randomMove(Environment):
	return 1