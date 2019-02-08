import random
import tkinter as tk
import tkinter.font as tkfont

class Agent:
    '''Base class for intelligent agents'''

    def __init__(self, team, environment):
        self.percepts = []
        self.team = team
        self.environment = Environment(environment.width, environment.height)
        self.nextMove = (0, 0, 0)
        self.availableMoves = []
        self.lastMove = (0, 0, 0)

    def sense(self, percepts, environment):
        '''process environment percepts'''
        self.percepts.append(percepts)

        # percepts contain the available move choices
        self.availableMoves = environment.getPossibleMoves()
        self.lastMove = environment.lastMove
        if self.lastMove[2] != 0:
            self.environment.put(
                self.lastMove[0], self.lastMove[1], self.lastMove[2])

    def think(self):
        '''think about what action to take'''
        # print("thinking...rattle, rattle, rattle")

    def action(self):
        '''return action agent decided on'''
        return self.nextMove


class PureRandomMoveAgent(Agent):
    '''Executes random moves'''

    def __init__(self, team, environment):
        super().__init__(team, environment)

    def think(self):
        '''Prepares the nextMove'''

        numAvailableMoves = len(self.availableMoves)
        i = random.randint(0, numAvailableMoves - 1)
        move = self.availableMoves[i]
        self.nextMove = (move[0], move[1], self.team)
        self.environment.put(self.nextMove[0], self.nextMove[1], self.team)


class RandomMoveAgent(Agent):
    '''Executes random moves, but doesn't miss an obvious win'''

    def __init__(self, team, environment):
        super().__init__(team, environment)

    def think(self):
        '''Prepares the nextMove'''

        numAvailableMoves = len(self.availableMoves)
        bestMove = (0, 0, 0)
        for move in self.availableMoves:
            self.environment.put(move[0], move[1], self.team)
            isWinner = self.environment.getWinner() == self.team
            self.environment.put(move[0], move[1], 0)

            # Only pick a random move if we can't find an obvious move
            if isWinner:
                bestMove = (move[0], move[1], self.team)
                break

        if bestMove[2] == 0:
            i = random.randint(0, numAvailableMoves - 1)
            move = self.availableMoves[i]
            self.nextMove = (move[0], move[1], self.team)
        else:
            self.nextMove = bestMove

        self.environment.put(self.nextMove[0], self.nextMove[1], self.team)


class DefensiveMoveAgent(Agent):
    '''Executes random moves, but minimizes adversity possible wins'''

    def __init__(self, team, environment):
        super().__init__(team, environment)

    def think(self):
        '''Prepares the nextMove'''

        otherTeam = self.team + 1
        if otherTeam > 2:
            otherTeam = 1

        numAvailableMoves = len(self.availableMoves)
        bestMove = (0, 0, 0)
        alpha = -100
        alphai = 0
        beta = 100
        betai = 0
        i = 0
        for move in self.availableMoves:
            self.environment.put(move[0], move[1], self.team)
            isWinner = self.environment.getWinner() == self.team
            for j in range(numAvailableMoves):
                if j == i:
                    continue;
                theirmove = self.availableMoves[j]
                self.environment.put(theirmove[0], theirmove[1], otherTeam)
                theirPossibleWins = self.environment.countPossibleWins(otherTeam)
                if self.environment.getWinner == otherTeam:
                    bestMove = (theirmove[0], theirmove[1], self.team)
                    isWinner = True;
                    break;
                if beta > theirPossibleWins:
                    beta = theirPossibleWins
                    betai = i
                ourPossibleWins = self.environment.countPossibleWins(self.team)
                if alpha < ourPossibleWins:
                    alpha = ourPossibleWins
                    alphai = i
                self.environment.put(theirmove[0], theirmove[1], 0)
            self.environment.put(move[0], move[1], 0)

            i = i + 1

            # Only pick a random move if we can't find an obvious move
            if isWinner:
                bestMove = (move[0], move[1], self.team)
                break

        if bestMove[2] == 0:
            move = self.availableMoves[betai]
            self.nextMove = (move[0], move[1], self.team)
        else:
            self.nextMove = bestMove

        self.environment.put(self.nextMove[0], self.nextMove[1], self.team)


class BestMoveAgent(Agent):
    '''Executes better than random moves. Checks if opponents will win'''

    def __init__(self, team, environment):
        super().__init__(team, environment)

    def think(self):
        '''Prepares the nextMove'''

        numAvailableMoves = len(self.availableMoves)
        bestMove = (0, 0, 0)
        bestScore = -100
        otherTeam = self.team + 1
        if otherTeam > 2:
            otherTeam = 1

        choices = []
        i = 0
        for move in self.availableMoves:
            self.environment.put(move[0], move[1], self.team)
            score = self.pathScore()
            theirmoves = self.environment.getPossibleMoves()
            for theirmove in theirmoves:
                self.environment.put(theirmove[0], theirmove[1], otherTeam)
                score = self.pathScore()
                self.environment.put(theirmove[0], theirmove[1], 0)
            self.environment.put(move[0], move[1], 0)

            # Only pick a random move if we can't find an obvious move
            if score > bestScore:
                bestMove = (move[0], move[1], self.team)
                bestScore = score
                choices = [i]
            elif score == bestScore:
                choices.append(i)

        if bestMove[2] == 0:
            i = random.randint(0, numAvailableMoves - 1)
            move = self.availableMoves[i]
            self.nextMove = (move[0], move[1], self.team)
        else:
            j = random.randint(0, len(choices) - 1)
            move = self.availableMoves[choices[j]]
            self.nextMove = (move[0], move[1], self.team)
            
        # print(self.team, ' ', bestScore, end='', flush=True)
        self.environment.put(self.nextMove[0], self.nextMove[1], self.team)

    def pathScore(self):
        ourPossibleWins = self.environment.countPossibleWins(self.team)
        theirPossibleWins = self.environment.countPossibleWins(-self.team)
        winner = self.environment.getWinner()
        theirWin = winner > 0 and winner != self.team
        ourWin = winner == self.team
        if ourWin:
            ourPossibleWins = ourPossibleWins + 100
        elif theirWin:
            theirPossibleWins = theirPossibleWins + 100
        return ourPossibleWins - theirPossibleWins


class Environment:
    '''Environment for AI program'''

    def __init__(self, width, height):
        self.board = [[0 for i in range(width)] for j in range(height)]
        self.width = width
        self.height = height
        self.lastMove = (0, 0, 0)
        self.reset()

    def reset(self):
        for j in range(self.height):
            for i in range(self.width):
                self.board[j][i] = 0

    def resetRandom(self):
        turn = 0
        self.reset()
        x = [(i, j) for i in range(self.width)
             for j in range(self.height)]
        random.shuffle(x)
        count = 0
        for i, j in x:
            if turn == 0:
                self.board[j][i] = 1
            else:
                self.board[j][i] = 2
            turn = 1 - turn
            count = count + 1
            # print(self)
            # print("Turn: {}, Team 1: {}, Team 2: {}".format(
            #     count, self.countPossibleWins(1), self.countPossibleWins(2)))
            # print(self.getPossibleMoves())

    def __str__(self):
        '''Creaste string representation of Environment'''
        s = ""
        for j in range(self.height):
            s = s + "[ "
            for i in range(self.width):
                s = s + str(format(self.board[j][i], "01d")) + " "
            s = s + "]"
            if j < self.height-1:
                s = s + "\n"
        return s

    def get(self, col, row):
        if row < 0 or row > self.height - 1:
            return 0
        if col < 0 or col > self.width - 1:
            return 0
        return self.board[row][col]

    def put(self, col, row, piece):
        if row < 0 or row > self.height - 1:
            return
        if col < 0 or col > self.width - 1:
            return
        self.lastMove = (col, row, piece)
        self.board[row][col] = piece

    def isPossibleWin(self, p1, p2, p3):
        if p1 == 0 and p2 == p3:
            return p2
        elif p2 == 0 and p1 == p3:
            return p1
        elif p3 == 0 and p1 == p2:
            return p1
        return 0

    def numAvailableMoves(self):
        count = 0
        for j in range(self.height):
            for i in range(self.width):
                if self.board[j][i] == 0:
                    count = count + 1
        return count

    def countPossibleWins(self, team):
        count = 0

        for j in range(self.height):
            for i in range(self.width):
                p = self.board[j][i]
                h2 = self.get(i+1, j)
                h3 = self.get(i+2, j)
                v2 = self.get(i, j+1)
                v3 = self.get(i, j+2)
                d2 = self.get(i+1, j+1)
                d3 = self.get(i+2, j+2)
                o2 = self.get(i-1, j+1)
                o3 = self.get(i-2, j+2)

                t1 = self.isPossibleWin(p, h2, h3)
                t2 = self.isPossibleWin(p, v2, v3)
                t3 = self.isPossibleWin(p, d2, d3)
                t4 = self.isPossibleWin(p, o2, o3)

                if team > 0:
                    # check if our team
                    if t1 == team:
                        count = count + 1
                    elif t2 == team:
                        count = count + 1
                    elif t3 == team:
                        count = count + 1
                    elif t4 == team:
                        count = count + 1
                else:
                    # check if their team
                    if t1 != 0 and t1 != -team:
                        count = count + 1
                    elif t2 != 0 and t2 != -team:
                        count = count + 1
                    elif t3 != 0 and t3 != -team:
                        count = count + 1
                    elif t4 != 0 and t4 != -team:
                        count = count + 1

        return count

    def getPossibleMoves(self):
        x = []
        for j in range(self.height):
            for i in range(self.width):
                if self.board[j][i] == 0:
                    x.append((i, j))
        return x

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

        numMoves = self.numAvailableMoves()
        if numMoves == 0:
            return -1
        return 0

    def __len__(self):
        '''implements len(self)'''
        return self.width * self.height


class Simulation(tk.Frame):
    '''Simulation environment for AI program'''

    def __init__(self, master=None, width=3, height=3):
        super().__init__(master)
        self.width = width
        self.height = height

        self.master = master
        self.pack()
        self.init()

        self.started = False
        self.wantsQuit = False

    def init(self):
        default_font = tk.font.Font(font='TkDefaultFont')
        size = default_font['size']
        sizetwo = 2*size
        self.h1font = tkfont.Font(family="PragmataPro", size=sizetwo)
        self.h2font = tkfont.Font(family="PragmataPro", size=size)
        self.gamefont = tkfont.Font(family="PragmataPro", size=sizetwo)
        tk.Label(self, text="Tic Tac Toe", font=self.h1font).pack(fill=tk.X)
        tk.Label(self, text="agents by Dr. Jonathan Metzgar", font=self.h2font).pack(fill=tk.X)
        self.controlsFrame = tk.Frame(self)
        self.controlsFrame.pack()
        tk.Frame(self, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx = 5, pady = 5)
        self.scoresFrame = tk.Frame(self)
        self.scoresFrame.pack()
        tk.Frame(self, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx = 5, pady = 5)
        self.gameFrame = tk.Frame(self)
        self.gameFrame.pack()
        self.gameInnerFrame = tk.Frame(self.gameFrame)
        self.gameInnerFrame.pack()
        tk.Frame(self, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx = 5, pady = 5)
        self.optionsFrame = tk.Frame(self)
        self.optionsFrame.pack()
        tk.Frame(self, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx = 5, pady = 5)
        self.statusFrame = tk.Frame(self)
        self.statusFrame.pack()

        self.startStopButton = tk.Button(self.controlsFrame, text="Start", command=self.startStop)
        self.startStopButton.pack(side="left")
        self.quitButton = tk.Button(self.controlsFrame, text="Quit", command=self.quit)
        self.quitButton.pack(side="left")
        self.startStopLabel = tk.Label(self.statusFrame, text="stopped")
        self.startStopLabel.pack(side="left")

        # Options

        self.team1AgentType = tk.StringVar(value="Pure Random")
        self.team2AgentType = tk.StringVar(value="Pure Random")
        tk.Label(self.optionsFrame, text="Team 1 Agent Type").grid(column = 0, row = 0)
        self.team1Type = tk.OptionMenu(self.optionsFrame, self.team1AgentType, "Pure Random", "Random", "Best Move", "Defensive")
        tk.Label(self.optionsFrame, text="Team 2 Agent Type").grid(column = 0, row = 1)
        self.team2Type = tk.OptionMenu(self.optionsFrame, self.team2AgentType, "Pure Random", "Random", "Best Move", "Defensive")
        self.team1Type.grid(column = 1, row = 0)
        self.team2Type.grid(column = 1, row = 1)

        self.colsText = tk.StringVar(value="4")
        self.rowsText = tk.StringVar(value="5")
        tk.Label(self.optionsFrame, text="Columns").grid(column = 0, row = 2)
        tk.Label(self.optionsFrame, text="Rows").grid(column = 0, row = 3)
        self.colsSpinbox = tk.Spinbox(self.optionsFrame, from_=3, to=6, textvariable=self.colsText)
        self.colsSpinbox.grid(column = 1, row = 2)
        self.rowsSpinbox = tk.Spinbox(self.optionsFrame, from_=3, to=6, textvariable=self.rowsText)
        self.rowsSpinbox.grid(column = 1, row = 3)

        self.started = False

        self.gameCountLabel = tk.Label(self.scoresFrame, text="# Games")
        self.gameCountValue = tk.Label(self.scoresFrame, text="0")
        self.gameCountLabel.grid(row=0, column=0)
        self.gameCountValue.grid(row=1, column=0)

        self.drawsCountLabel = tk.Label(self.scoresFrame, text="Draws")
        self.drawsCountValue = tk.Label(self.scoresFrame, text="0")
        self.drawsCountLabel.grid(row=0, column=1)
        self.drawsCountValue.grid(row=1, column=1)

        self.team1CountLabel = tk.Label(self.scoresFrame, text="Team 1")
        self.team1CountValue = tk.Label(self.scoresFrame, text="0")
        self.team2CountLabel = tk.Label(self.scoresFrame, text="Team 2")
        self.team2CountValue = tk.Label(self.scoresFrame, text="0")
        self.team1CountLabel.grid(row=0, column=2)
        self.team1CountValue.grid(row=1, column=2)
        self.team2CountLabel.grid(row=0, column=3)
        self.team2CountValue.grid(row=1, column=3)

        self.reset()
        self.gameloop()

    def startStop(self):
        if self.started:
            self.started = False
            self.startStopLabel["text"] = "stopped"
            self.startStopButton["text"] = "Start"
        else:
            self.started = True
            self.startStopLabel["text"] = "started"
            self.startStopButton["text"] = "Stop"
            self.reset()

    def newAgent(self, team, type):
        if type == "Pure Random":
            return PureRandomMoveAgent(team, self.environment)
        if type == "Random":
            return RandomMoveAgent(team, self.environment)
        if type == "Best Move":
            return BestMoveAgent(team, self.environment)
        if type == "Defensive":
            return DefensiveMoveAgent(team, self.environment)
        return PureRandomMoveAgent(team, self.environment)

    def reset(self):
        self.gamecount = 0
        self.wincounts = [0, 0, 0]
        self.width = int(self.colsSpinbox.get())
        self.height = int(self.rowsSpinbox.get())
        self.environment = Environment(self.width, self.height)

        agent1 = self.newAgent(1, self.team1AgentType.get())
        agent2 = self.newAgent(2, self.team2AgentType.get())
        self.agents = [
            agent1,
            agent2
        ]

        self.gameInnerFrame.destroy()
        self.gameInnerFrame = tk.Frame(self.gameFrame)
        self.gameInnerFrame.pack()
        self.frames = [ [ 0 for i in range(self.width) ] for j in range(self.height) ]
        for i in range(self.width):
            for j in range(self.height):
                self.frames[j][i] = tk.Label(self.gameInnerFrame, font=self.gamefont)
                self.frames[j][i]["text"] = "0"
                self.frames[j][i].grid(row=j, column=i)

    def run(self):
        '''runs the simulation'''
        if self.gamecount >= 100:
            self.startStop()
            return

        winner = 0
        count = 0
        turn = 0
        self.environment.reset()
        while winner == 0:
            self.agents[turn].sense([], self.environment)
            self.agents[turn].think()
            move = self.agents[turn].action()
            self.environment.put(move[0], move[1], move[2])
            winner = self.environment.getWinner()
            count = count + 1
            turn = 1 - turn
            # print("Turn {}".format(count))
            # print(self.environment)

        if True:
            for i in range(self.width):
                for j in range(self.height):
                    text = " "
                    e = self.environment.get(i, j)
                    if e == 1:
                        text = 'X'
                    elif e == 2:
                        text = 'O'
                    elif e == 3:
                        text = 'Y'
                    elif e == 4:
                        text = 'Z'

                    self.frames[j][i]["text"] = text

        if winner > 0:
            self.wincounts[winner] = self.wincounts[winner] + 1
        else:
            self.wincounts[0] = self.wincounts[0] + 1
        self.gamecount = self.gamecount + 1

    def update(self):
        '''Update simulation'''
        if not self.started:
            return
        self.run()

    def draw(self):
        '''Draw simulation'''
        if not self.started:
            return
        
        self.gameCountValue["text"] = self.gamecount
        # print(self.gamecount)
        # print(self.environment)

        for i in range(self.width):
            for j in range(self.height):
                # self.frames[j][i] = tk.Label(self.gameFrame, font=("Helvetica", 16))
                text = " "
                e = self.environment.get(i, j)
                if e == 1:
                    text = 'X'
                elif e == 2:
                    text = 'O'
                elif e == 3:
                    text = 'Y'
                elif e == 4:
                    text = 'Z'

                self.frames[j][i]["text"] = text
                # self.frames[j][i].grid(row=j, column=i)

        # print("Winners")
        self.drawsCountValue["text"] = self.wincounts[0]
        self.team1CountValue["text"] = self.wincounts[1]
        self.team2CountValue["text"] = self.wincounts[2]

    def gameloop(self):
        self.update()
        self.draw()
        if (self.started):
            self.master.after_idle(self.gameloop)
        else:
            self.master.after(100, self.gameloop)

# sim = Simulation()
# sim.run()


root = tk.Tk()
sim = Simulation(master=root)
sim.mainloop()
