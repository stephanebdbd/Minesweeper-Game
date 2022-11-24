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


def is_there_a_mine(board, pos_x, pos_y):
    res = True
    for i, j in get_neighbors(board, pos_x, pos_y):
        if board[i][j] == 'X':
            res = False
    return res


def propagate_click(game_board, reference_board, pos_x, pos_y):
    (x, y), game_board[pos_y][pos_x] = get_size(game_board), reference_board[pos_y][pos_x]
    if game_board[pos_y][pos_x] != 'F':
        if pos_y - 1 >= 0:
            if is_there_a_mine(reference_board, pos_x - 1, pos_y):
                propagate_click(game_board, reference_board, pos_x, pos_y - 1)
        if pos_y + 1 < y:
            if is_there_a_mine(reference_board, pos_x, pos_y + 1):
                propagate_click(game_board, reference_board, pos_x, pos_y + 1)
        if pos_x - 1 >= 0:
            if is_there_a_mine(reference_board, pos_x - 1, pos_y):
                propagate_click(game_board, reference_board, pos_x - 1, pos_y)
        if pos_x + 1 < x:
            if is_there_a_mine(reference_board, pos_x + 1, pos_y):
                propagate_click(game_board, reference_board, pos_x + 1, pos_y)


def parse_input(n, m):
    action, pos_x, pos_y = -1, -1, -1
    while action not in ['c', 'f'] and not n > pos_x >= 0 <= pos_y < m:
        action, pos_x, pos_y = str(input()), int(input()), int(input())
    return [action, pos_x, pos_y]


def check_win(game_board, reference_board, mines_list, total_flags):
    hide = 0
    for i in range(len(game_board)):
        for j in range(len(game_board[0])):
            if reference_board[i][j] == 0 and game_board[i][j] == '.':
                hide += 1
    return total_flags == len(mines_list) or hide == len(mines_list)


def init_game(n, m, number_of_mines):
    game_board, reference_board = create_board(n, m), create_board(n, m)
    print_board(game_board)
    case = str(input())
    first_pos_x, first_pos_y = int(case.split(' ')[0]), int(case.split(' ')[1])
    mines_list = place_mines(reference_board, number_of_mines, first_pos_x, first_pos_y)
    for colonnes in range(len(reference_board)):
        for lignes in range(len(reference_board[0])):
            if [lignes, colonnes] in mines_list:
                reference_board[colonnes][lignes] = 'X'
    fill_in_board(reference_board)
    propagate_click(game_board, reference_board, first_pos_x, first_pos_y)
    print_board(game_board)
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


def main():
    win1, win2, win = False, False, False
    choix = str(input("Choix d'une case : "))
    n, m, number_of_mines = int(choix.split(' ')[1]), int(choix.split(' ')[2]), int(choix.split(' ')[3])
    game_board, reference_board, mines_list = init_game(n, m, number_of_mines)
    while not win:
        game, pos_x, pos_y = parse_input(n, m)
        if game == 'c':
            propagate_click(game_board, reference_board, pos_x, pos_y)
        elif game == 'f':
            reference_board[pos_y][pos_x], game_board[pos_y][pos_x] = 'F', 'F'
        print_board(game_board)
        win1 = check_win(game_board, reference_board, mines_list, number_of_flags(game_board))
        win2 = boom(len(mines_list), game_board)
        win = win2 or win1
    if win2:
        print("Bravo vous avez gagné !")
    else:
        for i, j in mines_list:
            game_board[i][j] = reference_board[i][j]
        print_board(game_board)
        print("Dommage, c'est perdu.")


# Code principal
main()
while (input("Souhaitez-vous recommencer le jeu ? oui/non : ")) == 'oui':
    main()
