class Player:
    def __init__(self, name, isTurn):
        self.name = name
        self.isTurn = isTurn
        self.listOfMoves = []

    def addMove(self, move):
        self.listOfMoves.append(move)

    def getMoves(self):
        return self.listOfMoves

    def getName(self):
        return self.name


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

    def play(self):
        while True:
            self.printPossibleMoves()
            if self.checkIsWinner(self.human):
                self.setWinner(self.human)
                print(self.human.getName(), "wins!")
                print("Winning moves:", self.getWinningMoves(self.human))
                break
            if self.checkIsWinner(self.computer):
                self.setWinner(self.computer)
                print(self.computer.getName(), "wins!")
                print("Winning moves:", self.getWinningMoves(self.computer))
                break
            if self.checkDraw():
                print("Draw!")
                break
            if self.human.isTurn:
                move = int(input(self.human.getName() + " enter your move: "))
                if not self.move(self.human, move):
                    print("Invalid move")
            else:  # the computer's turn
                computer_move = self.minmax_strategy()
                print(f"{self.computer.getName()} chooses {computer_move}")
                if not self.move(self.computer, computer_move):
                    print("Invalid move")

    def heuristic_available_moves(self):
        valid_moves = [move for move in self.possibleMoves if
                       move not in self.human.getMoves() and move not in self.computer.getMoves()]
        return sorted(valid_moves, key=lambda x: abs(x - 5))

    def minmax_decision(self, player, depth):
        if depth == 0 or self.game_over():
            return self.evaluate()

        if player == self.computer:
            best_value = float('-inf')
            for move in self.heuristic_available_moves():
                self.move(self.computer, move)
                value = self.minmax_decision(self.human, depth - 1)
                best_value = max(best_value, value)
                self.possibleMoves.append(move)
                self.computer.getMoves().remove(move)
                player.isTurn = False
                self.human.isTurn = True
            return best_value
        else:
            best_value = float('inf')
            for move in self.heuristic_available_moves():
                self.move(self.human, move)
                value = self.minmax_decision(self.computer, depth - 1)
                best_value = min(best_value, value)
                self.possibleMoves.append(move)
                self.human.getMoves().remove(move)
                player.isTurn = False
                self.computer.isTurn = True
            return best_value

    def minmax_strategy(self):
        best_move = None
        best_value = float('-inf')
        for move in self.heuristic_available_moves():
            self.move(self.computer, move)
            value = self.minmax_decision(self.human, 3)
            if value > best_value:
                best_value = value
                best_move = move
            self.possibleMoves.append(move)
            self.computer.getMoves().remove(move)
            self.computer.isTurn = False
            self.human.isTurn = True

        return best_move

    def evaluate(self):
        if self.getWinningMoves(self.human):
            return -10

        if self.getWinningMoves(self.computer):
            return 10

        return len(self.computer.getMoves()) - len(self.human.getMoves())

    def game_over(self):
        return self.getWinner() is not None or self.checkDraw()


player1 = Player("Player", True)
player2 = Player("Computer", False)

game = Game(player1, player2)
game.play()
