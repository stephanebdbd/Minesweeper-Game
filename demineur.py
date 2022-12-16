"""
Jeu démineur.
Prenom : Stéphane.
Nom : Badi Budu.
Matricule : 569 082.
Petit jeu à jouer dans le terminal qui consiste à trouver les mines du
plateau de jeu, ou à dévoiler toutes les cases sans tomber sur une mine.
Date : 1er décembre 2022.
Entrée : la longueur et la largeur du plateau, le nombre de mines et on clique sur les cases.
Sorties : le plateau de jeu.
"""
# Import de modules.
from random import *
import sys


# Définition de fonctions.
def create_board(n, m):
    """
    Fonction qui crée une matrice pour les plateaux du jeu de dimension n x m.
    Entrée : les dimensions n et m du plateau.
    Sortie : matrice de listes de strings (list[list[str]]).
    """
    return [['.' for _ in range(m)] for _ in range(n)]


def print_board(board):
    """
    Affiche le plateau de jeu.
    Entrée : un plateau (list[list[str]]).
    """
    implementation, (n, m), colors = len(str(len(board[0]) - 1)), get_size(board), {'Fx': u"\u001b[31mF\u001b[0m", 'F': u"\u001b[32mF\u001b[0m", 'X': u"\u001b[31mX\u001b[0m"}
    for i in range(1 - len(str(m - 1)), 1):  # Boucle pour écrire les chiffres au-dessus du plateau.
        ligne = ''
        for j in range(10 * (-i), m):  # Boucle pour décaler l'écriture de 10 places pour le chiffre de dizaine des dizaines.
            ligne += ' ' + str(j)[len(str(j)) - 1 + i]  # On ajoute progressivement les chiffres dans la variable de la ligne.
        print(' ' * (2 * (10 * (-i)) + implementation + 2) + ligne)  # On imprime la ligne.
    print((implementation + 1) * ' ' + ((2 * m) + 3) * '—')
    for i in range(n):  # On crée une boucle de la dimension n pour écrire les lignes et les chiffres de l'ordonnée n.
        ligne = ''
        for j in board[i]:  # Seconde boucle pour sortir les valeurs du board.
            if j in colors:
                j = colors[j]
            ligne += str(j) + ' '  # On ajoute à la ligne, la ligne des valeurs.
        print(' ' * (implementation - len(str(i))) + str(i) + ' | ' + str(ligne) + '|')  # On imprime la ligne.
    print((implementation + 1) * ' ' + ((2 * m) + 3) * '—')


def get_size(board):
    """
    Retourne les dimensions du plateau de jeu.
    Entrée : un des 2 plateaux (list[list[str]]).
    Sortie : Tuple des dimensions données au début n x m (Tuple[int,int]).
    """
    return len(board), len(board[0])


def get_neighbors(board, pos_x, pos_y):
    """
    Fonction qui retourne une liste des coordonnées des cases qui entourent celle du paramètre.
    Entrée : la matrice d'un des plateaux (list), les coordonnées n et m (int) de la case choisie.
    Sortie : liste de tuples qui sont les coordonnées des cases voisines (List[Tuple[int,int]]).
    """
    (n, m), neighbors = get_size(board), []  # Variable des dimensions n et m du plateau et liste des coordonnées des voisins de la case choisie.
    for i in range(-1, 2):  # 2 boucles allant de -1 à +1 pour déterminer les cases qui entourent la case choisie.
        for j in range(-1, 2):
            if m > pos_x + j >= 0 <= pos_y + i < n and (i != 0 or j != 0):
                neighbors.append([pos_x + j, pos_y + i])  # on ajoute les coordonnées des cases voisines dans la liste si elle est dans le board et s'il
    return neighbors


def place_mines(reference_board, number_of_mines, first_pos_x, first_pos_y):
    """
    Fonction qui place aléatoirement les mines du jeu dans le plateau de référence.
    Entrée : la matrice du plateau de référence (List[Tuple[int,int]]), le nombre de mines et les coordonnées n et m de la première case choisie (int).
    Sortie : liste des coordonnées des cases où ont été placées les mines (List[Tuple[int,int]]).
    """
    neighbors, mines_list, (n, m) = get_neighbors(reference_board, first_pos_x, first_pos_y), [], get_size(reference_board)
    while len(mines_list) != number_of_mines:  # Tant qu'il n'y a pas autant de mines dans la liste que le nombre de mines choisi,
        ord_y, abs_x = randint(0, n - 1), randint(0, m - 1)  # On va déterminer une coordonnée de mine de manière aléatoire.
        if [ord_y, abs_x] not in mines_list and [abs_x, ord_y] not in neighbors and [abs_x, ord_y] != [first_pos_x, first_pos_y]:
            reference_board[ord_y][abs_x] = 'X'  # on place la mine dans sa case au plateau de jeu de référence
            mines_list.append([ord_y, abs_x])  # et on ajoute les coordonnées de la mine en question dans la liste des mines.
    return mines_list


def fill_in_board(reference_board):
    """
    Remplit chaque case du plateau de jeu de référence en y indiquant le nombre de mines autour de celle-ci.
    Entrée : la matrice du plateau de référence (List[Tuple[int,int]]).
    """
    for i in range(len(reference_board)):  # On crée 2 boucles pour examiner les différentes cases du plateau de référence.
        for j in range(len(reference_board[0])):
            if reference_board[i][j] == '.':  # Si la case est vide, on y indiquera le nombre de mines qui se trouvent autour d'elle.
                reference_board[i][j] = str(sum(1 for k, l in get_neighbors(reference_board, j, i) if reference_board[l][k] == 'X'))


def propagate_click(game_board, reference_board, pos_x, pos_y):
    """
    Fonction qui dévoile les cases voisines de celles qui sont révélées si dans les deux cas elles valent 0.
    Entrée : les matrices des plateaux de référence et de jeu (List[List[str]])et les coordonnées n et m de la case traitée (int).
    """
    if game_board[pos_y][pos_x] != 'F':
        game_board[pos_y][pos_x], zero = reference_board[pos_y][pos_x], []
        if reference_board[pos_y][pos_x] == '0':
            for i, j in get_neighbors(game_board, pos_x, pos_y):  # on crée une boucle examiner les cases voisines de celle qui est traitée.
                if game_board[j][i] != 'F':
                    game_board[j][i] = reference_board[j][i]
                if game_board[j][i] == '0':
                    for k, l in get_neighbors(game_board, i, j):  # on crée une boucle pour examiner toutes les cases qui l'entourent.
                        if (i, j) != (k, l) != (pos_x, pos_y) and (k, l) not in zero and game_board[l][k] != reference_board[l][k]:
                            zero.append((k, l))  # on ajoute les coordonnées de cette case dans la liste zero si la case n'a pas été traitée plus haut.
            for i, j in zero:
                propagate_click(game_board, reference_board, i, j)  # On applique la récursion à la fonction pour dévoiler les voisins de chacune d'entre elles.


def parse_input(n, m):
    """
    Permet au joueur d'entrer une chaine de caractère qui indique l'action qu'il demande sur la case qu'il a choisie.
    Entrée : les dimensions n et m du plateau (int).
    Sortie : L'action choisie (str), et la position x et la position y de la case choisie (int) le tout dans un tuple (Tuple[str, int, int]).
    """
    game = str(input("Choix d'une case : ")).split()  # On transforme en une liste les données entrées par personnage.
    if not (len(game) == 3 and game[0].isalpha() and game[0].lower() in 'cf' and game[1].isdigit() and game[2].isdigit() and m > int(game[1]) >= 0 <= int(game[2]) < n):
        game = parse_input(n, m)  # on redemande au joueur d'entrer ses données jusqu'à ce qu'ils les entrent correctement si ça n'avait pas été le cas.
    return game[0].lower(), int(game[2]), int(game[1])


def check_win(game_board, reference_board, mines_list, total_flags):
    """
    Fonction qui renvoie True si le joueur a gagné, sinon il renvoie False.
    Entrée : les plateaux de jeu et de référence (List[List[str]]), les coordonnées des mines (List[Tuple[int,int]]]) et le nombre de flags (int).
    Sortie : Booléen qui indique si le joueur a gagné ou pas (Bool)
    """
    (n, m), mines = get_size(game_board), sum(1 for i, j in mines_list if game_board[i][j] == 'X') == 0
    if not mines:
        for i in range(n):
            for j in range(m):
                if game_board[i][j] != 'F' and [i, j] in mines_list:  # Si la case était vide alors que c'était une mine,
                    game_board[i][j] = reference_board[i][j]  # on dévoile la case (qui est une mine).
                elif game_board[i][j] == 'F' and [i, j] not in mines_list:  # S'il y a un flag sur une case qui n'est pas celle d'une mine,
                    game_board[i][j] = 'Fx'  # on colorie ce "flag" en rouge pour spécifier qu'il était mal placé.
    win1 = total_flags + sum(1 for i in range(n) for j in range(m) if game_board[i][j] in '.') == len(mines_list)
    win2 = total_flags == len(mines_list) or sum(1 for i in range(n) for j in range(m) if game_board[i][j] in '.') == len(mines_list)
    return (win1 or win2) and mines  # Le joueur a gagné si toutes les cases ont été dévoilées sauf les mines et/ou si les mines ne sont pas dévoilées ou sous un flag.


def init_game(n, m, number_of_mines):
    """
    Fonction qui met en place le début du jeu.
    Entrées : les dimensions n et m des plateaux (int), et le nombre de mines (int).
    Sorties : les plateaux du jeu et de référence (List[List[str]]) et la liste des coordonnées des mines (List[Tuple[int,int]]).
    """
    game_board, reference_board = create_board(n, m), create_board(n, m)  # Création des plateaux du jeu et de référence.
    print_board(game_board)
    action, first_pos_x, first_pos_y = parse_input(n, m)  # On demande au joueur d'entrer la première case choisie
    while action == 'f':  # Tant que l'action choisie est de mettre un flag (et non de dévoiler une case),
        game_board[first_pos_y][first_pos_x] = 'F'  # on place ce flag à la case choisie,
        print_board(game_board)
        action, first_pos_x, first_pos_y = parse_input(n, m)  # et on redemande au joueur d'entrer sa commande.
    mines_list = place_mines(reference_board, number_of_mines, first_pos_x, first_pos_y)  # On place les mines et on récupère la liste des coordonnées de celles-ci.
    reference_board[first_pos_y][first_pos_x], game_board[first_pos_y][first_pos_x] = '0', '0'
    fill_in_board(reference_board)  # On remplit le plateau de référence.
    propagate_click(game_board, reference_board, first_pos_x, first_pos_y)  # On dévoile les cases voisines de celle qui a été révélée.
    print_board(game_board)
    return game_board, reference_board, mines_list  # On retourne les deux plateaux et la liste des coordonnées des mines.


def main():
    """
    Fonction principale qui contrôle le jeu en recevant les premières commandes du jeu, c'est-à-dire,
    les dimensions du plateau et le nombre de mines et contient une boucle qui finira à la fin de la partie.
    """
    if len(sys.argv) == 4 and sys.argv[3].isdigit() and sys.argv[1].isdigit() and sys.argv[2].isdigit():  # Si les 3 valeurs entrées sont bien des chiffres,
        n, m, number_of_mines = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
        if n * m - 8 > number_of_mines > 0 and n <= 100 >= m:  # et si n et m sont inférieurs à 100 et qu'il n'y a pas trop de mines,
            sys.setrecursionlimit((n * m) ** 2)  # On limite la récursion.
            (game_board, reference_board, mines_list), win_dictionary = init_game(n, m, number_of_mines), {True: "Bravo, vous avez gagné !", False: "Dommage, vous avez perdu."}
            flags_on_mines, total_flags, mines = sum(1 for i, j in mines_list if game_board[i][j] == 'F'), sum(1 for i, j in mines_list if game_board[i][j] == 'F'), True
            hidden_boxes, game_win = sum(1 for i in range(n) for j in range(m) if game_board[i][j] == '.'), check_win(game_board, reference_board, mines_list, total_flags)
            if not game_win:  # Si le joueur n'a pas gagné la partie avant qu'elle ne commence et si c'est le cas, tant que l'utilisateur n'a pas perdu ou gagné,
                while not ((flags_on_mines == total_flags and hidden_boxes + total_flags == number_of_mines) or flags_on_mines == total_flags == number_of_mines) and mines:
                    action, pos_x, pos_y = parse_input(n, m)
                    if action == 'c':
                        game_board[pos_y][pos_x] = reference_board[pos_y][pos_x]  # on dévoile la case en avance au cas où c'est un flag.
                        propagate_click(game_board, reference_board, pos_x, pos_y)  # et on dévoile les cases voisines si la case est un 0.
                    elif action == 'f' and game_board[pos_y][pos_x] == 'F':  # Si la case est déjà sous un flag,
                        game_board[pos_y][pos_x] = reference_board[pos_y][pos_x]  # ça veut dire que l'utilisateur désire dévoiler la case sous flag.
                    elif action == 'f' and game_board[pos_y][pos_x] == '.':
                        game_board[pos_y][pos_x] = 'F'
                    mines, hidden_boxes = sum(1 for i, j in mines_list if game_board[i][j] == 'X') == 0, sum(1 for i in range(n) for j in range(m) if game_board[i][j] == '.')
                    flags_on_mines, total_flags = sum(1 for i, j in mines_list if game_board[i][j] == 'F'), sum(1 for i, j in mines_list if game_board[i][j] == 'F')
                    game_win = check_win(game_board, reference_board, mines_list, total_flags)
                    print_board(game_board)
            print(win_dictionary[game_win])  # On retourne un message de victoire ou de défaite à l'utilisateur à la fin du jeu.


# Code principal.
if __name__ == '__main__':
    main()
