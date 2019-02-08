#Created 2/8/19 by Bradley Morton for CS405 assignment

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
		if row < 0 or row > self.height - 1:
			return 0
		if col < 0 or col > self.width - 1:
			return 0
		return self.board[row][col]

	def put(self, col, row, piece):
		if row < 0 or row > 5:
			return
		if col < 0 or col > 6:
			return
		self.lastMove = (col, row, piece)
		self.board[row][col] = piece




	def getWinner(self):
		'''checks to see if Tic Tac Toe has been won'''

		for j in range(self.height):
			for i in range(self.width):
				p = self.get(i, j)
				if p == 0:
					continue

                # check horizontal
				h2 = self.get(i+1, j)
				h3 = self.get(i+2, j)
				if p == h2 and h2 == h3:
					return p

                # check vertical
				v2 = self.get(i, j+1)
				v3 = self.get(i, j+2)
				if p == v2 and v2 == v3:
					return p

                # check diagonal
				d2 = self.get(i+1, j+1)
				d3 = self.get(i+2, j+2)
				if p == d2 and d2 == d3:
					return p

                # check reverse diagonal
				d2 = self.get(i-1, j+1)
				d3 = self.get(i-2, j+2)
				if p == d2 and d2 == d3:
					return p
        

