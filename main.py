import copy
import heapq
import time

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

    for moveDirection in ["up", "down", "left", "right"]:

        if transition(matrix, moveDirection):
            if DFS(matrix, depth - 1):
                return True
            transition(matrix, opposite(moveDirection))

    return False


def IDDFS(matrix):
    depth = 0
    while True:
        if DFS(matrix, depth):
            return True
        depth += 1


# Ex 5
def manhattan_distance(matrix):
    distance = 0
    for i in range(3):
        for j in range(3):
            value = matrix[i, j].value
            if value != 0:
                goal_row, goal_col = (value - 1) // 3, (value - 1) % 3
                distance += abs(goal_row - i) + abs(goal_col - j)
    return distance

def hamming_distance(matrix):
    distance = 0
    for i in range(3):
        for j in range(3):
            value = matrix[i, j].value
            if value != 0:
                goal_row, goal_col = (value - 1) // 3, (value - 1) % 3
                if goal_row != i or goal_col != j:
                    distance += 1
    return distance

def misplaced_tiles(matrix):
    misplaced = 0
    goal_matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

    for i in range(3):
        for j in range(3):
            if matrix[i, j].value != goal_matrix[i, j]:
                misplaced += 1

    return misplaced


def greedy_best_search(matrix, heuristic):
    visited_states = set()
    queue = [(matrix, 0)]  # (matrix, heuristic value)
    transition_counter = 0
    while queue:
        queue.sort(key=lambda x: heuristic(x[0]))
        current_matrix, depth = queue.pop(0)

        if checkFinalOrder(current_matrix):
            printMatrix(current_matrix)
            print("Solution found")
            print("Number of transitions: ", transition_counter)
            return True

        visited_states.add(tuple(map(tuple, current_matrix)))

        if depth >= 50:
            continue

        transition_counter += 1

        for moveDirection in ["up", "down", "left", "right"]:
            new_matrix = copy.deepcopy(current_matrix)
            if transition(new_matrix, moveDirection):
                if tuple(map(tuple, new_matrix)) not in visited_states:
                    queue.append((new_matrix, depth + 1))

    print("Solution not found")
    return False


def run_strategy(matrix, strategy, heuristic=None):
    start_time = time.time()
    if heuristic is None:
        result = strategy(matrix)
    else:
        result = strategy(matrix, heuristic)
    execution_time = time.time() - start_time
    return result, execution_time


matrix1_values = [8, 6, 7, 2, 5, 4, 0, 3, 1]
matrix2_values = [2, 7, 5, 0, 8, 4, 3, 1, 6]
matrix3_values = [2, 5, 3, 1, 0, 6, 4, 7, 8]

def run_all(*values_list):
    for values in values_list:
        matrix = init(values)
        print("Matrix: ", values)
        print("IDDFS: ", run_strategy(matrix, IDDFS))
        matrix = init(values)
        print("Greedy best search with manhattan distance: ", run_strategy(matrix, greedy_best_search, manhattan_distance))
        matrix = init(values)
        print("Greedy best search with hamming distance: ", run_strategy(matrix, greedy_best_search, hamming_distance))
        matrix = init(values)
        print("Greedy best search with misplaced tiles: ", run_strategy(matrix, greedy_best_search, misplaced_tiles))
        matrix = init(values)
        print("\n")


run_all(matrix1_values, matrix2_values, matrix3_values)
