from random import *


def create_board(n, m):
    return [['' for _ in range(n)] for _ in range(m)]


def print_board(board):
    x, y = get_size(board)
    implem = len(str(x))
    ligne = str(' ' * (implem + 4))
    for i in range(len(str(y))):
        ligne += str(' ' * ((10 ** i) - 1))
        for j in range(((10 ** i) - 1), y):
            ligne += str(j) + ' '
        print(ligne)
    print((implem + 2) * ' ' + ((2 * x) + 3) * '_')
    for i in range(len(str(x))):
        for j in range(((10 ** i) - 1), x):
            print(str(' ' * (implem - i)) + str(j) + ' | ' + str('. ' * x) + '|')
    print((implem + 2) * ' ' + ((2 * x) + 3) * '_')


def get_size(board):
    return len(board[0]), len(board)


def get_neighbors(board, pos_x, pos_y):
    (x, y), res = get_size(board), []
    if x > pos_x + 1 >= 0 <= pos_y + 1 < y:
        res.append([pos_x + 1, pos_y])
    if x > pos_x - 1 >= 0 <= pos_y - 1 < y:
        res.append([pos_x - 1, pos_y - 1])
    if x > pos_x + 1 >= 0 <= pos_y < y:
        res.append([pos_x + 1, pos_y])
    if x > pos_x >= 0 <= pos_y + 1 < y:
        res.append([pos_x, pos_y + 1])
    if x > pos_x + 1 >= 0 <= pos_y - 1 < y:
        res.append([pos_x + 1, pos_y - 1])
    if x > pos_x - 1 >= 0 <= pos_y + 1 < y:
        res.append([pos_x - 1, pos_y + 1])
    if x > pos_x - 1 >= 0 <= pos_y < y:
        res.append([pos_x - 1, pos_y])
    if x > pos_x >= 0 <= pos_y - 1 < y:
        res.append([pos_x, pos_y - 1])
    return res


def place_mines(reference_board, number_of_mines, first_pos_x, first_pos_y):
    voisins, mines = get_neighbors(reference_board, first_pos_x, first_pos_y), 0
    (x, y), res = get_size(reference_board), []
    seed(420)
    while mines < number_of_mines:
        abs_x, ord_y = randint(0, x), randint(0, y)
        if [abs_x, ord_y] not in voisins:
            reference_board[abs_x][ord_y] = 'F'
            res.append([abs_x, ord_y])
            mines += 1
    return res


# Code principal
