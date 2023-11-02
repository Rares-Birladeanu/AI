import numpy as np

class Board:
    def __init__(self, listOfValues, evenCells):
        self.matrix = np.full((9, 9), None)
        self.even_cells = evenCells
        self.possible_values = [[set() for _ in range(9)] for _ in range(9)]
        self.fillBoard(listOfValues)

    def __str__(self):
        return str(self.matrix)

    def print(self):
        print("Matrix: \n", self.matrix)
        print("Even cells: \n", self.even_cells)

    def fillBoard(self, list_of_values):
        for i in range(9):
            for j in range(9):
                if list_of_values[i * 9 + j] is not None:
                    value = list_of_values[i * 9 + j]
                    self.matrix[i, j] = value
                    self.possible_values[i][j] = set([value])

    def setPossibleValues(self, row, col, values):
        self.possible_values[row][col] = values

    def getPossibleValues(self, row, col):
        return self.possible_values[row][col]

    def generatePossibleValues(self, row, col):
        possible_values = set()
        for value in range(1, 10):
            if self.checkRowForValue(row, value) and self.checkColForValue(col, value) and self.checkSquareForValue(row, col, value):
                possible_values.add(value)
        return possible_values

    def checkRowForValue(self, row, value):
        for i in range(9):
            if self.matrix[row, i] == value:
                return False
        return True

    def checkRow(self, row):
        for value in range(1, 10):
            if not self.checkRowForValue(row, value):
                return False
        return True

    def checkColForValue(self, col, value):
        for i in range(9):
            if self.matrix[i, col] == value:
                return False
        return True

    def checkCol(self, col):
        for value in range(1, 10):
            if not self.checkColForValue(col, value):
                return False
        return True

    def checkSquareForValue(self, row, col, value):
        square_row, square_col = row // 3 * 3, col // 3 * 3
        for i in range(3):
            for j in range(3):
                if self.matrix[square_row + i, square_col + j] == value:
                    return False
        return True

    def checkSquare(self, row, col):
        for value in range(1, 10):
            if not self.checkSquareForValue(row, col, value):
                return False
        return True

    def checkBoard(self):
        for row in range(9):
            if not self.checkRow(row):
                return False
        for col in range(9):
            if not self.checkCol(col):
                return False
        for row in range(0, 9, 3):
            for col in range(0, 9, 3):
                if not self.checkSquare(row, col):
                    return False
        return True

    def placeValue(self, row, col, value):
        if self.matrix[row, col] is None and value in self.getPossibleValues(row, col):
            self.matrix[row, col] = value
            self.setPossibleValues(row, col, set([value]))

            for i in range(9):
                if value in self.getPossibleValues(row, i):
                    self.getPossibleValues(row, i).discard(value)

            for i in range(9):
                if value in self.getPossibleValues(i, col):
                    self.getPossibleValues(i, col).discard(value)

            square_row, square_col = row // 3 * 3, col // 3 * 3
            for i in range(3):
                for j in range(3):
                    if value in self.getPossibleValues(square_row + i, square_col + j):
                        self.getPossibleValues(square_row + i, square_col + j).discard(value)

            return True
        else:
            return False

    def isValidAssignment(self, row, col, value):
        if self.matrix[row, col] is None and self.checkRowForValue(row, value) and self.checkColForValue(col, value) and self.checkSquareForValue(row, col, value):
            return True
        else:
            return False

    def findMRVCell(self):
        min_possible_values = 10
        min_row, min_col = None, None
        for i in range(9):
            for j in range(9):
                if self.matrix[i, j] is None and len(self.getPossibleValues(i, j)) < min_possible_values:
                    min_possible_values = len(self.getPossibleValues(i, j))
                    min_row, min_col = i, j
        if min_row is not None and min_col is not None:
            return min_row, min_col
        else:
            return None

    def forwardCheck(self):
        for i in range(9):
            for j in range(9):
                if self.matrix[i, j] is None:
                    possible_values = self.generatePossibleValues(i, j)
                    self.setPossibleValues(i, j, possible_values)
                    if len(possible_values) == 0:
                        return False
        return True

    def solve(self):
        if not self.forwardCheck():
            return False

        if self.checkBoard():
            return True

        if self.findMRVCell() is None:
            return True

        row, col = self.findMRVCell()
        possible_values = self.getPossibleValues(row, col)
        for value in possible_values:
            if self.isValidAssignment(row, col, value):
                self.placeValue(row, col, value)
                if self.solve():
                    return True
                self.matrix[row, col] = None
                self.setPossibleValues(row, col, possible_values)
        return False



def initListOfValues():
    values = [None, 3, None, None, None, 7, None, 5, None,
              4, None, None, None, None, None, None, 3, 1,
              9, None, None, None, 2, 8, None, None, None,
              5, None, None, 8, None, None, None, None, 7,
              None, None, 6, None, 5, None, 3, None, None,
              None, 4, None, 2, 7, 3, None, None, None,
              8, None, None, 7, None, 2, None, None, None,
              None, 5, 7, None, None, 4, None, 2, None,
              None, None, 1, None, None, 9, 7, 8, None]
    return values

list_of_values = initListOfValues()
even_cells = [(0, 0), (0, 2), (0, 3), (0, 8),
              (1, 0), (1, 2), (1, 3), (1, 6),
              (2, 4), (2, 5), (2, 6), (2, 8),
              (3, 1), (3, 3), (3, 4), (3, 5),
              (4, 1), (4, 2), (4, 7), (4, 8),
              (5, 1), (5, 3), (5, 6), (5, 7),
              (6, 0), (6, 2), (6, 4), (6, 5),
              (7, 4), (7, 5), (7, 6), (7, 7),
              (8, 0), (8, 1), (8, 7), (8, 8)]

sudoku_board = Board(list_of_values, even_cells)

if sudoku_board.solve():
    print("Solution found!")
    sudoku_board.print()
else:
    print("No solution found!")
