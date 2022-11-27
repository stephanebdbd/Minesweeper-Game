"""
Prenom : Stéphane
Nom : Badi Budu
Matricule : 569 082
"""

from random import *
import sys


def create_board(n, m):
    return [['.' for _ in range(n)] for _ in range(m)]


def print_board(board):
    implem, (x, y) = len(str(len(board[0]) - 1)), get_size(board)
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
    while bombes != number_of_mines:
        abs_x, ord_y = randint(0, x - 1), randint(0, y - 1)
        if (abs_x, ord_y) not in voisins and (abs_x, ord_y) != (first_pos_x, first_pos_y):
            reference_board[ord_y][abs_x] = 'X'
            res.append((abs_x, ord_y))
            bombes += 1
    return res


def fill_in_board(reference_board):
    for i in range(len(reference_board)):
        for j in range(len(reference_board[0])):
            if reference_board[j][i] == '.':
                liste, number = get_neighbors(reference_board, i, j), 0
                for k, l in liste:
                    if reference_board[l][k] == 'X':
                        number += 1
                reference_board[j][i] = str(number)


def propagate_click(game_board, reference_board, pos_x, pos_y):
    (x, y), game_board[pos_y][pos_x] = get_size(game_board), reference_board[pos_y][pos_x]
    if reference_board[pos_y][pos_x] == '0':
        for i, j in get_neighbors(reference_board, pos_x, pos_y):
            game_board[j][i] = reference_board[j][i]
        if pos_x - 1 >= 0:
            propagate_click(game_board, reference_board, pos_x - 1, pos_y)
        if pos_x + 1 < x:
            propagate_click(game_board, reference_board, pos_x + 1, pos_y)
        if pos_y - 1 >= 0:
            propagate_click(game_board, reference_board, pos_x, pos_y - 1)
        if pos_y + 1 < y:
            propagate_click(game_board, reference_board, pos_x, pos_y + 1)


def parse_input(n, m):
    action, pos_x, pos_y = str(input()), int(input()), int(input())
    if action in ['c', 'f'] and n > pos_x >= 0 <= pos_y < m:
        return [action, pos_x, pos_y]


def check_win(game_board, reference_board, mines_list, total_flags):
    hide = len(mines_list)
    for i in range(len(game_board)):
        for j in range(len(game_board[0])):
            if reference_board[j][i] == 'X' and game_board[j][i] == '.':
                hide -= 1
    return total_flags == len(mines_list) or hide == 0


def init_game(n, m, number_of_mines):
    game_board, reference_board = create_board(n, m), create_board(n, m)
    print_board(game_board)
    first_pos_y, first_pos_x = int(input()), int(input())
    mines_list = place_mines(reference_board, number_of_mines, first_pos_x, first_pos_y)
    for i, j in mines_list:
        reference_board[j][i] = 'X'
    reference_board[first_pos_y][first_pos_x], game_board[first_pos_y][first_pos_x] = '0', '0'
    fill_in_board(reference_board)
    propagate_click(game_board, reference_board, first_pos_x, first_pos_y)
    print_board(game_board)
    return game_board, reference_board, mines_list


def main():
    flags, bombes, n, m, number_of_mines = 0, 0, int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    game_board, reference_board, mines_list = init_game(n, m, number_of_mines)
    while not (check_win(game_board, reference_board, mines_list, flags) or bombes == 0):
        flags, (game, pos_x, pos_y) = 0, parse_input(n, m)
        if game == 'c':
            propagate_click(game_board, reference_board, pos_x, pos_y)
        else:
            game_board[pos_y][pos_x] = 'F'
        for i in range(n):
            for j in range(m):
                if reference_board[j][i] == 'X' and game_board[j][i] == 'F':
                    flags += 1
                if game_board[j][i] == 'X':
                    bombes += 1
        if not (check_win(game_board, reference_board, mines_list, flags) or bombes == 0):
            print_board(game_board)
    if not (check_win(game_board, reference_board, mines_list, flags) or bombes == 0):
        print_board(game_board)
    else:
        for i, j in mines_list:
            game_board[j][i] = 'X'
        print_board(game_board)


if __name__ == '__main__':
    main()
