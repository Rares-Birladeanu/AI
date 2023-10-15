import numpy as np

"""
    We have a 3x3 matrix with 8 cells numbered 1 to 8 and one empty cell. Knowing that the initial position of the 
cells is random and that we can move a cell only in place of the empty cell and only if it is adjacent to it, find, 
if there is one, a sequence of moves such that all cells are placed in ascending order in the matrix. After a cell is 
moved it cannot be moved again until one of its neighbors has been moved. The position of the empty cell does not 
matter for final state validation.
"""

"""" 
    Choose a representation of a state of the problem. The representation must be explicit enough to contain all the 
necessary information to continue finding a solution, but it must also be formal enough to be easy to process/store.
"""


class Cell:
    def __init__(self, value, isMovable):
        self.value = value
        self.isMovable = isMovable


"""
    Identify the special states (initial and final) and implement the initialization function (takes as parameters the 
problem instance, returns the initial state) and the boolean function that checks whether a state received as a 
parameter is final.
"""


def init(listOfValues):
    # create a matrix of new cells and place the values from the list in each cell and return the matrix
    matrix = np.zeros((3, 3), dtype=Cell)
    for i in range(3):
        for j in range(3):
            matrix[i, j] = Cell(listOfValues[i * 3 + j], True)

    return matrix


# make a function that prints the values of cells in the matrix
def printMatrix(matrix):
    for i in range(3):
        for j in range(3):
            print(matrix[i, j].value, end=" ")
        print()


# make a function that returns true or false if the value from the cells from the matrix are in the right order (from
# 1 to 8 and 0 at any place)

def checkFinalOrder(matrix):
    # use the value from the cells to check if they are in the right order using a max
    max = -1
    for i in range(3):
        for j in range(3):
            if matrix[i, j].value != 0:
                if matrix[i, j].value > max:
                    max = matrix[i, j].value
                else:
                    return False

    return True


"""
    Implement transitions as functions that take a state and transition parameters and return the state resulting from 
applying the transition. Validation of transitions is done in one or more boolean functions with the same parameters.
"""


def areMovable(matrix, x1, x2, y1, y2):
    # check if the cells have the flag isMovable set to True
    return matrix[x1, y1].isMovable and matrix[x2, y2].isMovable


def oneIsZero(matrix, x1, x2, y1, y2):
    # check if one of the cells is 0
    return matrix[x1, y1].value == 0 or matrix[x2, y2].value == 0


def resetIsMovable(matrix):
    # reset the isMovable value of all the cells in the matrix
    for i in range(3):
        for j in range(3):
            matrix[i, j].isMovable = True

    return matrix


def swapValues(matrix, x1, y1, x2, y2):
    # swap the values of the cells
    aux = matrix[x1, y1].value
    matrix[x1, y1].value = matrix[x2, y2].value
    matrix[x2, y2].value = aux

    return matrix


def checkZeroAndSetIsMovable(matrix, x1, y1, x2, y2):
    # check if one of the cells is 0 and set the isMovable value of the other cell to False
    if matrix[x1, y1].value == 0:
        matrix[x2, y2].isMovable = False
    else:
        matrix[x1, y1].isMovable = False

    return matrix


def areAdjacent(x1, y1, x2, y2):
    if x1 == x2:
        if y1 == y2 + 1 or y1 == y2 - 1:
            return True
        else:
            return False
    elif y1 == y2:
        if x1 == x2 + 1 or x1 == x2 - 1:
            return True
        else:
            return False


def swapCells(matrice, x1, y1, x2, y2):
    if not areAdjacent(x1, y1, x2, y2):
        return matrice
    if not areMovable(matrice, x1, x2, y1, y2):
        return matrice
    if not oneIsZero(matrice, x1, x2, y1, y2):
        return matrice
    else:
        matrix = resetIsMovable(matrice)
        matrix = swapValues(matrix, x1, y1, x2, y2)
        matrix = checkZeroAndSetIsMovable(matrix, x1, y1, x2, y2)
        return matrix


listOfValues = [1, 2, 3, 4, 5, 6, 7, 8, 0]
matrix = init(listOfValues)
printMatrix(matrix)
print(matrix[0, 0].value)
print(matrix[0, 1].value)
print()
matrix = swapCells(matrix, 2, 2, 1, 2)
printMatrix(matrix)
print(matrix[0, 0].value)
print(matrix[0, 1].value)
