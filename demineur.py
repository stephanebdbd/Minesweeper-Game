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
    voisins, bombes, (x, y), res = get_neighbors(reference_board, first_pos_x, first_pos_y), 0, get_size(reference_board), []
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
                valeurs = [reference_board[l][k] for k, l in get_neighbors(reference_board, i, j)]
                reference_board[j][i] = str(valeurs.count('X'))


def propagate_click(game_board, reference_board, pos_x, pos_y):
    game_board[pos_y][pos_x], zero = reference_board[pos_y][pos_x], []
    if reference_board[pos_y][pos_x] == '0':
        for i, j in get_neighbors(game_board, pos_x, pos_y):
            game_board[j][i] = reference_board[j][i]
            if reference_board[j][i] == '0':
                for k, l in get_neighbors(game_board, i, j):
                    if (i, j) != (k, l) != (pos_x, pos_y) and (k, l) not in zero and game_board[l][k] in ['.', 'F']:
                        zero.append((k, l))
        if len(zero) > 0:
            for i, j in zero:
                propagate_click(game_board, reference_board, i, j)


def parse_input(n, m):
    choix = str(input("Choix d'une case : "))
    if choix.strip()[0] in ['c', 'f']:
        action, pos_x, pos_y = choix.strip()[0], int(choix[1:].strip().split()[0]), int(choix[1:].strip().split()[1])
        if n > pos_x >= 0 <= pos_y < m:
            return [action, pos_x, pos_y]


def check_win(game_board, reference_board, mines_list, total_flags):
    if len(mines_list) == total_flags:
        for i in range(len(game_board)):
            for j in range(len(game_board[0])):
                if reference_board[j][i] == 'X' and game_board[j][i] == 'F':
                    total_flags -= 1
                if game_board[j][i] == 'X':
                    for k, l in mines_list:
                        game_board[l][k] = 'X'
                        print("Dommage, c'est perdu.")
                    return True
        return total_flags == 0
    else:
        return False


def init_game(n, m, number_of_mines):
    game_board, reference_board = create_board(n, m), create_board(n, m)
    print_board(game_board)
    case = str(input('Choix de la première case : '))
    first_pos_y, first_pos_x = int(case.strip().split()[0]), int(case.strip().split()[1])
    mines_list = place_mines(reference_board, number_of_mines, first_pos_x, first_pos_y)
    reference_board[first_pos_y][first_pos_x], game_board[first_pos_y][first_pos_x] = '0', '0'
    fill_in_board(reference_board)
    propagate_click(game_board, reference_board, first_pos_x, first_pos_y)
    print_board(game_board)
    return game_board, reference_board, mines_list


def main():
    n, m, number_of_mines = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    (game_board, reference_board, mines_list), win = init_game(n, m, number_of_mines), False
    while not win:
        action, pos_x, pos_y = parse_input(n, m)
        if action == 'c':
            propagate_click(game_board, reference_board, pos_x, pos_y)
        else:
            game_board[pos_y][pos_x] = 'F'
        win = check_win(game_board, reference_board, mines_list, sum([i.count('F') for i in game_board]))
        print_board(game_board)
    for i, j in mines_list:
        if game_board[j][i] == 'X':
            win = False
    if win:
        print("Bravo, vous avez gagné !")


if __name__ == '__main__':
    main()
