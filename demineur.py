from random import *


def create_board(n, m):
    return [['.' for _ in range(n)] for _ in range(m)]


def print_board(board):
    x, y = get_size(board)
    implem = len(str(x - 1))
    for i in range(1 - len(str(x - 1)), 1):
        ligne = str(' ' * (2 * (10 * (-i)) + implem + 2))
        for j in range(10 * (-i), x):
            ligne += ' ' + str(j)[len(str(j)) - 1 + i]
        print(ligne)
    print((implem + 1) * ' ' + ((2 * y) + 3) * '_')
    for i in range(y):
        ligne = ''
        for j in board[i]:
            ligne += str(j) + ' '
        print(' ' * (implem - len(str(i))) + str(i) + ' | ' + str(ligne) + '|')
    print((implem + 1) * ' ' + ((2 * y) + 3) * '_')


def get_size(board):
    return len(board[0]), len(board)


def get_neighbors(board, pos_x, pos_y):
    (x, y), res = get_size(board), []
    if x > pos_x + 1 >= 0 <= pos_y + 1 < y:
        res.append([pos_x + 1, pos_y + 1])
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
    while mines != number_of_mines:
        abs_x, ord_y = randint(0, x - 1), randint(0, y - 1)
        if [abs_x, ord_y] not in voisins and (abs_x, ord_y) != (first_pos_x, first_pos_y):
            reference_board[ord_y][abs_x] = 'F'
            res.append([abs_x, ord_y])
            mines += 1
    return res


def fill_in_board(reference_board):
    for i in range(len(reference_board)):
        for j in range(len(reference_board[0])):
            if reference_board[i][j] != 'X':
                liste, reference_board[i][j] = get_neighbors(reference_board, j, i), 0
                for k in liste:
                    if reference_board[k[1]][k[0]] == 'X':
                        reference_board[i][j] += 1


def propagate_click(game_board, reference_board, pos_x, pos_y):
    voisinage = get_neighbors(reference, pos_x, pos_y)
    game_board[pos_y][pos_x] = reference_board[pos_y][pos_x]
    if {voisinage} & {bombes} & {[pos_x, pos_y]} == set():
        for x, y in voisinage:
            game_board[y][x] = reference_board[y][x]
    for i, j in voisinage:
        if reference_board[j][i] == 0:
            propagate_click(game_board, reference_board, i, j)


def parse_input(n, m):
    joueur = str(input())
    if joueur in ['c', 'f']:
        return [joueur, n, m]


def check_win(game_board, reference_board, mines_list, total_flags):
    hide = 0
    for i in range(len(game_board)):
        for j in range(len(game_board[0])):
            if reference_board[i][j] == 0 and game_board[i][j] == '.':
                hide += 1
    return total_flags == len(mines_list) or hide == len(mines_list)


# Code principal
ox, oy, bomba = int(input()), int(input()), int(input())
game, reference = create_board(ox, oy), create_board(ox, oy)
bombes = place_mines(reference, bomba, 0, 0)
for colonnes in range(len(reference)):
    for lignes in range(len(reference[0])):
        if [lignes, colonnes] in bombes:
            reference[colonnes][lignes] = 'X'
fill_in_board(reference)
print_board(reference)
