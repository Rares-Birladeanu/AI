from random import randint

import numpy as np


def initBoard():
    return np.full((9, 9), None)


def fillBoard(sudoku_board, list_of_values):
    for x, y, value in list_of_values:
        sudoku_board[x, y] = value


def initListOfValues():
    list_of_values = []
    for i in range(9):
        for j in range(9):
            list_of_values.append((i, j, randint(1, 9)))
    return list_of_values


def checkRowForValue(sudoku_board, row, value):
    for i in range(9):
        if sudoku_board[row, i] == value:
            return False
    return True


def checkRow(sudoku_board, row):
    for value in range(1, 10):
        if not checkRowForValue(sudoku_board, row, value):
            return False
    return True


def checkColForValue(sudoku_board, col, value):
    for i in range(9):
        if sudoku_board[i, col] == value:
            return False
    return True


def checkCol(sudoku_board, col):
    for value in range(1, 10):
        if not checkColForValue(sudoku_board, col, value):
            return False
    return True


def checkSquareForValue(sudoku_board, row, col, value):
    for i in range(3):
        for j in range(3):
            if sudoku_board[row + i, col + j] == value:
                return False
    return True


def checkSquare(sudoku_board, row, col):
    for value in range(1, 10):
        if not checkSquareForValue(sudoku_board, row, col, value):
            return False
    return True


def checkBoard(sudoku_board):
    for i in range(9):
        if not checkRow(sudoku_board, i):
            return False
        if not checkCol(sudoku_board, i):
            return False
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            if not checkSquare(sudoku_board, i, j):
                return False
    return True


list_of_values = initListOfValues()

sudoku_board = initBoard()
fillBoard(sudoku_board, list_of_values)

print(sudoku_board)
