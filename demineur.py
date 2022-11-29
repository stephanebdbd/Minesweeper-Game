"""
Prenom : Stéphane
Nom : Badi Budu
Matricule : 569 082

"""

from random import *
from sys import *


def create_board(n, m):
    return [['.' for _ in range(n)] for _ in range(m)]


def print_board(board):
    implem, (x, y) = len(str(len(board[0]) - 1)), get_size(board)
    for i in range(1 - len(str(x - 1)), 1):
        ligne = str(' ' * (2 * (10 * (-i)) + implem + 2))
        for j in range(10 * (-i), x):
            ligne += ' ' + str(j)[len(str(j)) - 1 + i]
        print(ligne)
    print((implem + 1) * ' ' + ((2 * x) + 3) * '_')
    for i in range(y):
        ligne = ''
        for j in board[i]:
            if j == 'X':
                j = u"\u001b[31mX\u001b[0m"
            elif j == 'F':
                j = u"\u001b[32mF\u001b[0m"
            ligne += str(j) + ' '
        print(' ' * (implem - len(str(i))) + str(i) + ' | ' + str(ligne) + '|')
    print((implem + 1) * ' ' + ((2 * x) + 3) * '_')


def get_size(board):
    return len(board[0]), len(board)


def get_neighbors(board, pos_x, pos_y):
    (x, y), res = get_size(board), []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if x > pos_x + j >= 0 <= pos_y + i < y and (i != 0 or j != 0):
                res.append([pos_x + j, pos_y + i])
    return res


def place_mines(reference_board, number_of_mines, first_pos_x, first_pos_y):
    voisins, bombes, (x, y) = get_neighbors(reference_board, first_pos_x, first_pos_y), [], get_size(reference_board)
    while len(bombes) != number_of_mines:
        abs_x, ord_y = randint(0, x - 1), randint(0, y - 1)
        case = [abs_x, ord_y]
        if case not in bombes and case not in voisins and case != [first_pos_x, first_pos_y]:
            reference_board[ord_y][abs_x] = 'X'
            bombes.append(case)
    return bombes


def fill_in_board(reference_board):
    for i in range(len(reference_board[0])):
        for j in range(len(reference_board)):
            if reference_board[j][i] == '.':
                valeurs = [reference_board[l][k] for k, l in get_neighbors(reference_board, i, j)]
                reference_board[j][i] = str(valeurs.count('X'))


def propagate_click(game_board, reference_board, pos_x, pos_y):
    game_board[pos_y][pos_x] = reference_board[pos_y][pos_x]
    if reference_board[pos_y][pos_x] == '0':
        zero = []
        for i, j in get_neighbors(game_board, pos_x, pos_y):
            game_board[j][i] = reference_board[j][i]
            if game_board[j][i] == '0':
                for k, l in get_neighbors(game_board, i, j):
                    if (i, j) != (k, l) != (pos_x, pos_y) and (k, l) not in zero and game_board[l][k] != reference_board[l][k]:
                        zero.append((k, l))
        if len(zero) > 0:
            for i, j in zero:
                propagate_click(game_board, reference_board, i, j)


def parse_input(n, m):
    jeu = str(input("Choix d'une case : ")).strip().split()
    if len(jeu) == 3 and jeu[0] in ['c', 'f'] and jeu[1].isdigit() and jeu[2].isdigit() and n > int(jeu[1]) >= 0 <= int(jeu[2]) < m:
        action, pos_y, pos_x = jeu[0], int(jeu[1]), int(jeu[2])
    else:
        action, pos_y, pos_x = parse_input(n, m)
    return [action, pos_x, pos_y]


def check_win(game_board, reference_board, mines_list, total_flags):
    hide, (x, y) = 0, get_size(game_board)
    for i in range(y):
        for j in range(x):
            if game_board[i][j] == 'X':
                for k, l in mines_list:
                    if game_board[l][k] != 'F':
                        game_board[l][k] = reference_board[l][k]
                return True
            elif game_board[i][j] in ['F', '.'] and reference_board[i][j] == 'X':
                hide += 1
            elif game_board[i][j] == '.':
                total_flags -= 1
    return hide == len(mines_list) and total_flags == 0


def init_game(n, m, number_of_mines):
    game_board, reference_board = create_board(n, m), create_board(n, m)
    print_board(game_board)
    case = str(input('Choix de la première case : ')).strip().split()
    while not (len(case) == 2 and case[0].isdigit() and case[1].isdigit() and n > int(case[0]) >= 0 <= int(case[1]) < m):
        case = str(input('Choix de la première case : ')).strip().split()
    first_pos_y, first_pos_x = int(case[0]), int(case[1])
    mines_list = place_mines(reference_board, number_of_mines, first_pos_x, first_pos_y)
    reference_board[first_pos_y][first_pos_x], game_board[first_pos_y][first_pos_x] = '0', '0'
    fill_in_board(reference_board)
    propagate_click(game_board, reference_board, first_pos_x, first_pos_y)
    print_board(game_board)
    return game_board, reference_board, mines_list


def main():
    game = []
    if len(argv) == 4:
        for i in argv:
            if i.isdigit():
                game.append(int(i))
        if len(game) == 3:
            n, m, number_of_mines = game
            setrecursionlimit(n * m)
            (game_board, reference_board, mines_list) = init_game(n, m, number_of_mines)
            while not check_win(game_board, reference_board, mines_list, sum([1 for j, i in mines_list if game_board[i][j] == 'F'])):
                action, pos_x, pos_y = parse_input(n, m)
                if action == 'c':
                    propagate_click(game_board, reference_board, pos_x, pos_y)
                else:
                    game_board[pos_y][pos_x] = 'F'
                check_win(game_board, reference_board, mines_list, sum([1 for j, i in mines_list if game_board[i][j] == 'F']))
                print_board(game_board)
            if sum([1 for j, i in mines_list if game_board[i][j] == 'X']) == 0:
                print("Bravo, vous avez gagné !")
            else:
                print("Dommage, c'est perdu.")


if __name__ == '__main__':
    main()
