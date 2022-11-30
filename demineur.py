"""
Jeu démineur
Prenom : Stéphane
Nom : Badi Budu
Matricule : 569 082
Petit jeu à jouer dans le terminal qui consiste à trouver les mines du
plateau de jeu, ou à dévoiler toutes les cases sans tomber sur une mine
Date : 29 novembre 2022.
Entrée : la longueur et la largeur du tableau, le nombre de mines et on clique sur les cases.
Sorties : le tableau du jeu actualisé.
"""
# Import de modules
from random import *
import sys


# Définition de fonctions
def create_board(n, m):
    """
    Fonction qui crée une matrice pour le tableau du jeu de dimension n x m.
    Entrée : les dimensions n et m du tableau.
    Sortie : matrice de listes de strings (list[list[str]]).
    """
    return [['.' for _ in range(n)] for _ in range(m)]  # On retourne la matrice


def print_board(board):
    """
    Affiche le plateau de jeu
    Entrée : le board/tableau du jeu (list[list[str]])..
    """
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
    """
    Retourne les dimensions du tableau/plateau de jeu.
    Entrée : le board/tableau du jeu (list[list[str]]).
    Sortie : Tuple des dimensions données au début n x m (Tuple[int,int]).
    """
    return len(board[0]), len(board)  # On retourne les dimensions de la matrice crée au début du jeu


def get_neighbors(board, pos_x, pos_y):
    """
    Fonction qui retourne une liste des coordonnées des cases qui entourent celle du paramètre.
    Entrée : la matrice du plateau de jeu (list), les coordonnées x et y (int) de la case choisie.
    Sortie : liste de tuples qui sont les coordonnées des cases voisines (List[Tuple[int,int]]).
    """
    (x, y), res = get_size(board), []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if x > pos_x + j >= 0 <= pos_y + i < y and (i != 0 or j != 0):
                res.append([pos_x + j, pos_y + i])
    return res


def place_mines(reference_board, number_of_mines, first_pos_x, first_pos_y):
    """
    Fonction qui place aléatoirement les mines du jeu dans le tableau de référence.
    Entrée : la matrice du tableau de jeu référent (list), le nombre de mines et les coordonnées x et y
             de la première case choisie (int).
    Sortie : liste des coordonnées des cases où ont été placées les mines (List[Tuple[int,int]]).
    """
    voisins, bombes, (x, y) = get_neighbors(reference_board, first_pos_x, first_pos_y), [], get_size(reference_board)
    while len(bombes) != number_of_mines:
        abs_x, ord_y = randint(0, x - 1), randint(0, y - 1)
        case = [abs_x, ord_y]
        if case not in bombes and case not in voisins and case != [first_pos_x, first_pos_y]:
            reference_board[ord_y][abs_x] = 'X'
            bombes.append(case)
    return bombes


def fill_in_board(reference_board):
    """
    Fonction qui remplit la matrice du tableau de jeu référent en comptant le nombre de mines autour
    de la case (exemple : si la case vaut 3, ça veut dire qu'il y a 3 mines autour de la case).
    """
    for i in range(len(reference_board[0])):
        for j in range(len(reference_board)):
            if reference_board[j][i] == '.':
                valeurs = [reference_board[l][k] for k, l in get_neighbors(reference_board, i, j)]
                reference_board[j][i] = str(valeurs.count('X'))


def propagate_click(game_board, reference_board, pos_x, pos_y):
    x, y = get_size(game_board)
    if x > pos_x >= 0 <= pos_y < y:
        game_board[pos_y][pos_x] = reference_board[pos_y][pos_x]
        if reference_board[pos_y][pos_x] == '0':
            zero = []
            for i, j in get_neighbors(game_board, pos_x, pos_y):
                game_board[j][i] = reference_board[j][i]
                if game_board[j][i] == '0':
                    for k, l in get_neighbors(game_board, i, j):
                        if (i, j) != (k, l) != (pos_x, pos_y) and (k, l) not in zero and game_board[l][k] != \
                                reference_board[l][k]:
                            zero.append((k, l))
            if len(zero) > 0:
                for i, j in zero:
                    propagate_click(game_board, reference_board, i, j)


def parse_input(n, m):
    jeu = str(input("Choix d'une case : ")).strip().split()
    if len(jeu) == 3 and jeu[0].isalpha() and jeu[1].isdigit() and jeu[2].isdigit():
        action, pos_y, pos_x = jeu[0], int(jeu[1]), int(jeu[2])
        if n > pos_x >= 0 <= pos_y < m and isinstance(action, str) and isinstance(pos_x, int) and isinstance(pos_y, int):
            return [action, pos_x, pos_y]


def check_win(game_board, reference_board, mines_list, total_flags):
    flag, hide, (x, y) = total_flags, 0, get_size(game_board)
    for i in range(y):
        for j in range(x):
            if game_board[i][j] == 'X':
                for k, l in mines_list:
                    if game_board[l][k] != 'F':
                        game_board[l][k] = reference_board[l][k]
                return True
            if game_board[i][j] == '.':
                hide += 1
            if game_board[i][j] == 'F' and reference_board[i][j] == 'X':
                total_flags -= 1
    if flag == len(mines_list):
        return total_flags == 0
    return hide == len(mines_list) or flag - total_flags + hide == len(mines_list)


def init_game(n, m, number_of_mines):
    game_board, reference_board = create_board(n, m), create_board(n, m)
    print_board(game_board)
    game = parse_input(n, m)
    if type(game) == list and len(game) == 3:
        action, first_pos_y, first_pos_x = game
        mines_list = place_mines(reference_board, number_of_mines, first_pos_x, first_pos_y)
        reference_board[first_pos_y][first_pos_x], game_board[first_pos_y][first_pos_x] = '0', '0'
        fill_in_board(reference_board)
        propagate_click(game_board, reference_board, first_pos_x, first_pos_y)
        print_board(game_board)
        if isinstance(game_board, list) and isinstance(reference_board, list) and isinstance(mines_list, list):
            return game_board, reference_board, mines_list


def main():
    """
    Fonction principale du jeu qui contrôle le jeu
    """
    if sys.argv[1].isdigit() and sys.argv[2].isdigit() and sys.argv[3].isdigit():
        n, m, number_of_mines = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
        sys.setrecursionlimit(n * m)
        start = init_game(n, m, number_of_mines)
        if isinstance(start, tuple) and len(start) == 3:
            game_board, reference_board, mines_list = start
            while not check_win(game_board, reference_board, mines_list, sum([1 for j, i in mines_list if game_board[i][j] == 'F'])):
                game = parse_input(n, m)
                if isinstance(game, list) and len(game) == 3:
                    action, pos_x, pos_y = game
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


# Code Principal
if __name__ == '__main__':  # test conditionnel
    main()  # appel à la fonction principale du jeu
