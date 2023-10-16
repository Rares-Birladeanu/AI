import numpy as np


class Cell:
    def __init__(self, value, isMovable):
        self.value = value
        self.isMovable = isMovable


def init(listOfValues):
    matrix = np.zeros((3, 3), dtype=Cell)
    for i in range(3):
        for j in range(3):
            matrix[i, j] = Cell(listOfValues[i * 3 + j], True)

    return matrix


def checkFinalOrder(matrix):
    max = -1
    for i in range(3):
        for j in range(3):
            if matrix[i, j].value != 0:
                if matrix[i, j].value > max:
                    max = matrix[i, j].value
                else:
                    return False

    return True


def printMatrix(matrix):
    for i in range(3):
        for j in range(3):
            print(matrix[i, j].value, end=" ")
        print()


def areMovable(matrix, x1, x2, y1, y2):
    return matrix[x1, y1].isMovable and matrix[x2, y2].isMovable


def oneIsZero(matrix, x1, x2, y1, y2):
    return matrix[x1, y1].value == 0 or matrix[x2, y2].value == 0


def resetIsMovable(matrix):
    for i in range(3):
        for j in range(3):
            matrix[i, j].isMovable = True


def swapValues(matrix, x1, y1, x2, y2):
    aux = matrix[x1, y1].value
    matrix[x1, y1].value = matrix[x2, y2].value
    matrix[x2, y2].value = aux


def checkZeroAndSetIsMovable(matrix, x1, y1, x2, y2):
    if matrix[x1, y1].value == 0:
        matrix[x2, y2].isMovable = False
    else:
        matrix[x1, y1].isMovable = False


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


def swapCells(matrix, x1, y1, x2, y2):
    if not areAdjacent(x1, y1, x2, y2):
        return False
    if not areMovable(matrix, x1, x2, y1, y2):
        return False
    if not oneIsZero(matrix, x1, x2, y1, y2):
        return False
    else:
        resetIsMovable(matrix)
        swapValues(matrix, x1, y1, x2, y2)
        global counter
        counter += 1
        checkZeroAndSetIsMovable(matrix, x1, y1, x2, y2)
        return True


def findZero(matrix):
    for i in range(3):
        for j in range(3):
            if matrix[i, j].value == 0:
                return i, j


def transition(matrix, moveDirection):
    x, y = findZero(matrix)

    if moveDirection == "up":
        if x == 0:
            return False
        else:
            if swapCells(matrix, x, y, x - 1, y):
                return True
            else:
                return False
    elif moveDirection == "down":
        if x == 2:
            return False
        else:
            if swapCells(matrix, x, y, x + 1, y):
                return True
            else:
                return False
    elif moveDirection == "left":
        if y == 0:
            return False
        else:
            if swapCells(matrix, x, y, x, y - 1):
                return True
            else:
                return False
    elif moveDirection == "right":
        if y == 2:
            return False
        else:
            if swapCells(matrix, x, y, x, y + 1):
                return True
            else:
                return False
    else:
        return False


listOfValues = [2, 5, 3, 1, 0, 6, 4, 7, 8]
matrix = init(listOfValues)

counter = 0


def opposite(moveDirection):
    if moveDirection == "up":
        return "down"
    elif moveDirection == "down":
        return "up"
    elif moveDirection == "left":
        return "right"
    elif moveDirection == "right":
        return "left"
    else:
        return None


def DFS(matrix, depth):
    if depth == 0:
        return False
    if checkFinalOrder(matrix):
        return True

    x, y = findZero(matrix)

    for moveDirection in ["up", "down", "left", "right"]:

        if transition(matrix, moveDirection):
            print("Counter: ", counter)
            if DFS(matrix, depth - 1):
                return True
            transition(matrix, opposite(moveDirection))

    return False


print('Initial matrix: ')
printMatrix(matrix)


def IDDFS(matrix):
    depth = 0
    while True:
        print("Current depth: ", depth)

        if DFS(matrix, depth):
            return True
        depth += 1


result = IDDFS(matrix)

if result:
    print("Solution found:")
    printMatrix(matrix)
else:
    print("No solution found.")
