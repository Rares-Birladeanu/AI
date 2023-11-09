class Player:
    def __init__(self, name, isTurn):
        self.name = name
        self.isTurn = isTurn
        self.listOfMoves = []

    def isTurn(self):
        return self.isTurn

    def addMove(self, move):
        self.listOfMoves.append(move)

    def getMoves(self):
        return self.listOfMoves

    def getName(self):
        return self.name

    def undoMovePlayer(self, move):
        if move in self.listOfMoves:
            self.listOfMoves.remove(move)


"""
The Game:
Two players alternately choose a number between 1 and 9 without repeating a number previously chosen by either player. The player who has chosen from the beginning of the game three numbers that add up to a total of 15 wins. If no more numbers can be chosen and no player has won, the game ends in a draw. 
Example: A:3 B:9 A:5 B:7 A:2 B:8 A:4 B:1 A:6 A wins (6+5+4)

1. Implement a heuristic.
2. Implement the MinMax strategy for player B anticipating at least two opponent moves.
"""


class Game:
    def __init__(self, human, computer):
        self.human = human
        self.computer = computer
        self.possibleMoves = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.human.isTurn = True
        self.computer.isTurn = False
        self.winner = None

    def getWinner(self):
        return self.winner

    def setWinner(self, winner):
        self.winner = winner

    def getMoves(self):
        return self.possibleMoves

    def move(self, player, move):
        if move in self.possibleMoves:
            player.addMove(move)
            self.possibleMoves.remove(move)
            player.isTurn = False
            if player == self.human:
                self.computer.isTurn = True
                self.human.isTurn = False
            else:
                self.human.isTurn = True
                self.computer.isTurn = False
            return True
        else:
            return False

    def checkIsWinner(self, player):
        if self.getWinningMoves(player) is not None:
            return True
        return False

    def getWinningMoves(self, player):
        moves = player.getMoves()
        if len(moves) >= 3:
            for i in range(len(moves)):
                for j in range(i + 1, len(moves)):
                    for k in range(j + 1, len(moves)):
                        if moves[i] + moves[j] + moves[k] == 15:
                            return [moves[i], moves[j], moves[k]]
        return None

    def checkDraw(self):
        if len(self.possibleMoves) == 0:
            self.setWinner(None)
            return True
        return False

    def printPossibleMoves(self):
        for i in range(1, 10):
            if i in self.possibleMoves:
                print(i, end=" ")
            else:
                print("x", end=" ")
        print()

    def undoMove(self, player, move):
        player.undoMovePlayer(move)
        self.possibleMoves.append(move)
        player.isTurn = False
        if player == self.human:
            self.computer.isTurn = True
            self.human.isTurn = False
        else:
            self.human.isTurn = True
            self.computer.isTurn = False

    def play(self):
        while True:
            self.printPossibleMoves()
            if self.checkIsWinner(self.human):
                self.setWinner(self.human)
                print(self.human.getName(), "wins!")
                break
            if self.checkIsWinner(self.computer):
                self.setWinner(self.computer)
                print(self.computer.getName(), "wins!")
                break
            if self.checkDraw():
                print("Draw!")
                break
            if self.human.isTurn:
                move = int(input(self.human.getName() + " enter your move: "))
                if not self.move(self.human, move):
                    print("Invalid move")
            else:  # the computer's turn
                move = self.bestMove()
                self.move(self.computer, move)
                print(self.computer.getName(), "moves", move)

    def bestMove(self):
        # iterate through all possible moves
        bestScore = -100000000
        bestMove = None
        for move in self.possibleMoves:
            # move with that move
            self.move(self.computer, move)
            score = self.minimax(self.computer, 0, False)
            # undo the move
            self.undoMove(self.computer, move)
            if score > bestScore:
                bestScore = score
                bestMove = move
        return bestMove

    def minimax(self, player, depth, isMaximizing):
        # check if the game is over
        if self.checkIsWinner(self.computer):
            return 1
        if self.checkIsWinner(self.human):
            return -1
        if self.checkDraw():
            return 0

        if isMaximizing:
            bestScore = -100000000
            for move in self.possibleMoves:
                self.move(self.computer, move)
                score = self.minimax(self.computer, depth + 1, False)
                self.undoMove(self.computer, move)
                bestScore = max(score, bestScore)
            return bestScore
        else:
            bestScore = 100000000
            for move in self.possibleMoves:
                score = self.minimax(self.human, depth + 1, True)
                self.undoMove(self.human, move)
                bestScore = min(score, bestScore)
            return bestScore


player1 = Player("Player", True)
player2 = Player("Computer", False)

game = Game(player1, player2)
game.play()
