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

    def minimax(self, depth, maximizingPlayer):
        if depth == 0 or self.checkIsWinner(self.human) or self.checkIsWinner(self.computer):
            return self.heuristic()

        if maximizingPlayer:
            value = float('-inf')
            for move in self.possibleMoves:
                if move in self.possibleMoves:
                    # Simulate the move
                    self.move(self.computer, move)
                    # Recursively call minimax on the child node
                    value = max(value, self.minimax(depth - 1, False))
                    # Undo the move (backtrack)
                    self.undoMove(move)
            return value
        else:
            value = float('inf')
            for move in self.possibleMoves:
                if move in self.possibleMoves:
                    # Simulate the move
                    self.move(self.human, move)
                    # Recursively call minimax on the child node
                    value = min(value, self.minimax(depth - 1, True))
                    # Undo the move (backtrack)
                    self.undoMove(move)
            return value

    def heuristic(self):
        pass

    def undoMove(self, move):
        # Implement the logic to undo a move
        # This is necessary for backtracking during the Minimax algorithm
        self.possibleMoves.append(move)
        if move in self.human.getMoves():
            self.human.getMoves().remove(move)
        else:
            self.computer.getMoves().remove(move)

    def findBestMove(self):
        pass

    def play(self):
        while True:
            self.printPossibleMoves()
            if self.checkIsWinner(self.human):
                self.human.setWinner(self.human)
                self.setWinner(self.human)
                print(self.human.getName(), "wins!")
                break
            if self.checkIsWinner(self.computer):
                self.computer.setWinner(self.computer)
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
                # self.computerBestMove()
                bestMove = self.findBestMove()
                print(self.computer.getName(), " chooses ", bestMove)
                self.move(self.computer, bestMove)


player1 = Player("Player", True)
player2 = Player("Computer", False)

game = Game(player1, player2)
game.play()
