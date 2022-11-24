# Prenom : Stéphane
# Nom : Badi Budu
# Matricule : 569 082
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
        res.append((pos_x + 1, pos_y + 1))
    if x > pos_x - 1 >= 0 <= pos_y - 1 < y:
        res.append((pos_x - 1, pos_y - 1))
    if x > pos_x + 1 >= 0 <= pos_y < y:
        res.append((pos_x + 1, pos_y))
    if x > pos_x >= 0 <= pos_y + 1 < y:
        res.append((pos_x, pos_y + 1))
    if x > pos_x + 1 >= 0 <= pos_y - 1 < y:
        res.append((pos_x + 1, pos_y - 1))
    if x > pos_x - 1 >= 0 <= pos_y + 1 < y:
        res.append((pos_x - 1, pos_y + 1))
    if x > pos_x - 1 >= 0 <= pos_y < y:
        res.append((pos_x - 1, pos_y))
    if x > pos_x >= 0 <= pos_y - 1 < y:
        res.append((pos_x, pos_y - 1))
    return res


def place_mines(reference_board, number_of_mines, first_pos_x, first_pos_y):
    voisins, bombes = get_neighbors(reference_board, first_pos_x, first_pos_y), 0
    (x, y), res = get_size(reference_board), []
    seed(420)
    while bombes != number_of_mines:
        abs_x, ord_y = randint(0, x - 1), randint(0, y - 1)
        if [abs_x, ord_y] not in voisins and (abs_x, ord_y) != (first_pos_x, first_pos_y):
            reference_board[ord_y][abs_x] = 'X'
            res.append((abs_x, ord_y))
            bombes += 1
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
    voisinage = get_neighbors(reference_board, pos_x, pos_y)
    game_board[pos_y][pos_x] = reference_board[pos_y][pos_x]
    mines_list = place_mines(reference_board, mines(reference_board), get_size(game_board))
    if {voisinage} & {mines_list} & {[pos_x, pos_y]} == set():
        for x, y in voisinage:
            game_board[y][x] = reference_board[y][x]
    for i, j in voisinage:
        if reference_board[j][i] == 0:
            propagate_click(game_board, reference_board, i, j)


def parse_input(action, n, m):
    if action in ['c', 'f']:
        return [action, n, m]


def check_win(game_board, reference_board, mines_list, total_flags):
    hide = 0
    for i in range(len(game_board)):
        for j in range(len(game_board[0])):
            if reference_board[i][j] == 0 and game_board[i][j] == '.':
                hide += 1
    return total_flags == len(mines_list) or hide == len(mines_list)


def init_game(n, m, number_of_mines):
    game_board, reference_board = create_board(n, m), create_board(n, m)
    first_pos_x, first_pos_y = int(input()), int(input())
    propagate_click(game_board, reference_board, first_pos_x, first_pos_y)
    mines_list = place_mines(reference_board, number_of_mines, first_pos_x, first_pos_y)
    for colonnes in range(len(reference_board)):
        for lignes in range(len(reference_board[0])):
            if [lignes, colonnes] in mines_list:
                reference_board[colonnes][lignes] = 'X'
    fill_in_board(reference_board)
    print_board(reference_board)
    return game_board, reference_board, mines_list


def number_of_flags(game_board):
    flags = 0
    for i in game_board:
        for j in i:
            if j == 'F':
                flags += 1
    return flags


def boom(bombes, game_board):
    for i in game_board:
        for j in i:
            if j == 'X':
                bombes -= 1
    return bombes == 0


def mines(board):
    mine = 0
    for i in board:
        for j in i:
            if j == 'X':
                mine += 1
    return mine


def main():
    n, m, number_of_mines, win = int(input()), int(input()), int(input()), False
    game_board, reference_board, mines_list = init_game(n, m, number_of_mines)
    while not win:
        action, pos_x, pos_y = str(input), int(input()), int(input())
        game = parse_input(action, pos_x, pos_y)
        if game[0] == 'c':
            propagate_click(game_board, reference_board, pos_x, pos_y)
        elif game[0] == 'f':
            reference_board[pos_y][pos_x], game_board[pos_y][pos_x] = 'F', 'F'
        print_board(game_board)
        win1 = check_win(game_board, reference_board, mines_list, number_of_flags(game_board))
        win2 = boom(len(mines_list), game_board)
        win = win2 or win1
    if str(input("Souhaitez-vous recommencer le jeu ? oui/non : ")) is 'oui':
        main()


# Code principal
main()
