"""
Jeu démineur.
Prenom : Stéphane.
Nom : Badi Budu.
Matricule : 569 082.
Petit jeu à jouer dans le terminal qui consiste à trouver les mines du
plateau de jeu, ou à dévoiler toutes les cases sans tomber sur une mine.
Date : 29 novembre 2022.
Entrée : la longueur et la largeur du tableau, le nombre de mines et on clique sur les cases.
Sorties : le tableau du jeu actualisé.
"""

# Import de modules.
from random import *  # Module random pour choisir les mines aléatoirement.
import sys
# Module sys pour récupérer les valeurs entrées au début du jeu et pour augmenter la limite récursive en fonction des dimensions du tableau de jeu.


# Définition de fonctions.
def create_board(n, m):
    """
    Fonction qui crée une matrice pour les plateaux du jeu de dimension n x m.
    Entrée : les dimensions n et m du tableau.
    Sortie : matrice de listes de strings (list[list[str]]).
    """
    return [['.' for _ in range(m)] for _ in range(n)]  # On retourne la matrice.


def print_board(board):
    """
    Affiche le plateau de jeu.
    Entrée : un plateau (list[list[str]]).
    """
    implem, (n, m) = len(str(len(board[0]) - 1)), get_size(board)  # Variable implem pour la longueur de l'implémentation.
    # n et m, les dimensions du tableau.
    for i in range(1 - len(str(m - 1)), 1):  # Boucle pour écrire les chiffres au-dessus du tableau.
        ligne = ''  # Variable pour l'écriture de la ligne
        for j in range(10 * (-i), m):  # Boucle pour décaler l'écriture de 10 places pour le chiffre de dizaine des dizaines.
            ligne += ' ' + str(j)[len(str(j)) - 1 + i]  # On ajoute progressivement les chiffres dans la variable de la ligne.
        print(' ' * (2 * (10 * (-i)) + implem + 2) + ligne)  # On imprime la ligne.
    print((implem + 1) * ' ' + ((2 * m) + 3) * '_')  # On trace une ligne pour séparer le tableau des chiffres.
    for i in range(n):  # On crée une boucle de la dimension n pour écrire les lignes et les chiffres de l'ordonnée n.
        ligne = ''
        for j in board[i]:  # Seconde boucle pour sortir les valeurs du board.
            if j == 'X':  # Si la valeur est une mine,
                j = u"\u001b[31mX\u001b[0m"  # elle devient rouge.
            elif j == 'F':  # Si la valeur est un flag sur une mine,
                j = u"\u001b[32mF\u001b[0m"  # elle devient verte.
            elif j == 'Fx':  # Si la valeur est un flag qui n'est pas sur une mine,
                j = u"\u001b[31mF\u001b[0m"  # elle devient rouge.
            ligne += str(j) + ' '  # On ajoute à la ligne, la ligne des valeurs.
        print(' ' * (implem - len(str(i))) + str(i) + ' | ' + str(ligne) + '|')  # On imprime la ligne.
    print((implem + 1) * ' ' + ((2 * m) + 3) * '_')  # On trace une ligne en dessous du tableau pour le fermer


def get_size(board):
    """
    Retourne les dimensions du tableau/plateau de jeu.
    Entrée : un des 2 plateaux (list[list[str]]).
    Sortie : Tuple des dimensions données au début n x m (Tuple[int,int]).
    """
    return len(board), len(board[0])  # On retourne les dimensions de la matrice crée au début du jeu


def get_neighbors(board, pos_x, pos_y):
    """
    Fonction qui retourne une liste des coordonnées des cases qui entourent celle du paramètre.
    Entrée : la matrice d'un des plateaux (list), les coordonnées n et m (int) de la case choisie.
    Sortie : liste de tuples qui sont les coordonnées des cases voisines (List[Tuple[int,int]]).
    """
    (n, m), voisins = get_size(board), []  # Variable des dimensions n et m du tableau et liste des coordonnées des voisins.
    for i in range(-1, 2):  # 2 boucles allant de -1 à +1 pour déterminer les cases qui entourent la case choisie.
        for j in range(-1, 2):
            if m > pos_x + j >= 0 <= pos_y + i < n and (i != 0 or j != 0):  # Si c'est une case du board et ce n'est pas la case choisie,
                voisins.append([pos_x + j, pos_y + i])  # on ajoute les coordonnées des cases voisines dans la liste "voisins".
    return voisins  # On retourne la liste "voisins".


def place_mines(reference_board, number_of_mines, first_pos_x, first_pos_y):
    """
    Fonction qui place aléatoirement les mines du jeu dans le tableau de référence.
    Entrée : la matrice du plateau référent (List[Tuple[int,int]]),
    le nombre de mines et les coordonnées n et m de la première case choisie (int).
    Sortie : liste des coordonnées des cases où ont été placées les mines (List[Tuple[int,int]]).
    """
    voisins, mines_list, (n, m) = get_neighbors(reference_board, first_pos_x, first_pos_y), [], get_size(reference_board)
    # Liste des voisins de la première case choisie, une liste pour y ajouter les mines du tableau et les dimensions n et m du tableau.
    while len(mines_list) != number_of_mines:  # Tant qu'il n'y a pas autant de mines dans la liste que le nombre de mines choisi,
        ord_y, abs_x = randint(0, n - 1), randint(0, m - 1)  # On va déterminer une coordonnée de mine de manière aléatoire.
        if [ord_y, abs_x] not in mines_list and [abs_x, ord_y] not in voisins and [abs_x, ord_y] != [first_pos_x, first_pos_y]:
            # Si la mine fait déjà partie de la liste des mines, des voisins de la première case et que ce n'est pas la première case,
            reference_board[ord_y][abs_x] = 'X'  # on place la mine dans sa case au tableau de jeu référent
            mines_list.append([ord_y, abs_x])  # et on ajoute les coordonnées de la mine en question dans la liste des mines.
    return mines_list  # On retourne la liste des mines.


def fill_in_board(reference_board):
    """
    Fonction qui remplit la matrice du tableau de jeu référent en indiquant
    le nombre de mines autour de chaque case.
    Entrée : la matrice du plateau référent (List[Tuple[int,int]]).
    """
    for i in range(len(reference_board)):  # On crée 2 boucles pour examiner les différentes cases du tableau référent.
        for j in range(len(reference_board[0])):
            if reference_board[i][j] == '.':  # Si la case est vide,
                reference_board[i][j] = str(sum(1 for k, l in get_neighbors(reference_board, j, i) if reference_board[l][k] == 'X'))
                # on indiquera y le nombre de mines qui se trouvent autour d'elle.


def propagate_click(game_board, reference_board, pos_x, pos_y):
    """
    Fonction qui dévoile les cases voisines de celles qui sont révélées si dans les deux cas elles valent 0.
    Entrée : les matrices des plateaux référents et de jeu (List[List[str]])
             et la position x et la position y de la case traitée (int).
    """
    if game_board[pos_y][pos_x] != 'F':  # Si la case n'est pas un flag,
        game_board[pos_y][pos_x], zero = reference_board[pos_y][pos_x], []  # on actualise le tableau de jeu.
        # Création d'une liste qui va contenir les coordonnées des cases qui valent 0 si la case traitée vaut aussi 0.
        if reference_board[pos_y][pos_x] == '0':  # Si la case traitée vaut 0,
            for i, j in get_neighbors(game_board, pos_x, pos_y):  # on crée une boucle examiner les cases voisines de celle qui est traitée.
                if game_board[j][i] != 'F':  # Si ce n'est pas un flag,
                    game_board[j][i] = reference_board[j][i]  # On l'actualise.
                if game_board[j][i] == '0':  # Si l'une d'entre elles vaut 0,
                    for k, l in get_neighbors(game_board, i, j):  # on crée une boucle pour examiner toutes les cases qui l'entourent.
                        if (i, j) != (k, l) != (pos_x, pos_y) and (k, l) not in zero and game_board[l][k] != reference_board[l][k]:
                            # Si la cases n'est pas dans la liste zero, qu'elle ne correspond à aucune des cases traités plus haut et qu'elle n'a pas encore été révélée,
                            zero.append((k, l))  # on ajoute les coordonnées de cette case dans la liste zero.
            for i, j in zero:  # On crée une boucle pour traiter les cases dont les coordonnées sont dans la liste.
                propagate_click(game_board, reference_board, i, j)  # On applique la récursion à la fonction pour dévoiler les voisins de chacune d'entre elles.


def parse_input(n, m):
    """
    Permet d'entrer une chaine de caractère qui indique l'action que demande l'utilisateur par rapport à la case choisie
    Entrée : les dimensions n et m du tableau (int).
    Sortie : L'action choisie (str), et la position x et la position y de la case choisie (int) le tout dans un tuple (Tuple[str, int, int]).
    """
    jeu = str(input("Choix d'une case : ")).strip().split()  # On transforme en une liste les données entrées par personnage.
    if len(jeu) == 3 and jeu[0] in 'CcFf' and jeu[1].isdigit() and jeu[2].isdigit() and m > int(jeu[1]) >= 0 <= int(jeu[2]) < n:
        # S'il y a bien 3 éléments dans la liste qui correspondent bien aux actions déterminées et aux coordonnées qui sont dans le tableau,
        return [jeu[0].lower(), int(jeu[2]), int(jeu[1])]  # on retourne le tuple de données
    return parse_input(n, m)  # Sinon on rappelle la même fonction "parse_input" tant que l'utilisateur n'aura pas entré des données valables.


def check_win(game_board, reference_board, mines_list, total_flags):
    """
    Fonction qui renvoie True si l'utilisateur a gagné, sinon il renvoie False.
    Entrée : les plateaux de jeu et référents (List[List[str]]), les coordonnées des mines (List[Tuple[int,int]]]) et le nombre de flags (int).
    """
    (n, m) = get_size(game_board)  # On prend les dimensions du tableau.
    for i in range(n):  # On crée une boucle pour examiner chaque case des plateaux
        for j in range(m):
            if game_board[i][j] == 'X':  # Si dans le plateau il y a une mine,
                for o in range(n):  # on crée une autre boucle pour examiner de nouveau chaque case du plateau de jeu
                    for p in range(m):
                        if game_board[o][p] != 'F' and [p, o] in mines_list:  # Si la case était vide alors que c'était une mine,
                            game_board[o][p] = reference_board[o][p]  # on dévoile la case (qui est une mine).
                        if game_board[o][p] == 'F' and [p, o] not in mines_list:  # S'il y a un flag sur une case qui n'est pas celle d'une mine,
                            game_board[o][p] = 'Fx'  # on colorie ce "flag" en rouge pour spécifier qu'il était mal placé.
                return False  # On retourne le booléen "False" pour spécifier que le joueur a perdu la partie.
    # L'une de ces conditions sera vraie si le joueur a trouvé les mines.
    return total_flags == len(mines_list) or sum(1 for i in range(n) for j in range(m) if game_board[i][j] in '.F')


def init_game(n, m, number_of_mines):
    game_board, reference_board = create_board(n, m), create_board(n, m)
    print_board(game_board)
    action, first_pos_x, first_pos_y = parse_input(n, m)
    while action == 'f':
        game_board[first_pos_y][first_pos_x] = 'F'
        print_board(game_board)
        action, first_pos_x, first_pos_y = parse_input(n, m)
    mines_list = place_mines(reference_board, number_of_mines, first_pos_x, first_pos_y)
    reference_board[first_pos_y][first_pos_x], game_board[first_pos_y][first_pos_x] = '0', '0'
    fill_in_board(reference_board)
    propagate_click(game_board, reference_board, first_pos_x, first_pos_y)
    print_board(game_board)
    return game_board, reference_board, mines_list


def main():
    """
    Fonction principale du jeu qui contrôle le jeu
    """
    if len(sys.argv) == 4 and sys.argv[3].isdigit() and sys.argv[1].isdigit() and sys.argv[2].isdigit():
        if int(sys.argv[1]) * int(sys.argv[2]) > int(sys.argv[3]):
            n, m, number_of_mines = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
            sys.setrecursionlimit(n * m)
            mines, m_flags, flags, hide, (game_board, reference_board, mines_list) = True, 0, 0, 0, init_game(n, m, number_of_mines)
            while not ((m_flags == flags and hide + flags == number_of_mines) or m_flags == flags == number_of_mines) and mines:
                (action, pos_x, pos_y), flags = parse_input(n, m), sum(1 for i, j in mines_list if game_board[i][j] == 'F')
                if action == 'c':
                    game_board[pos_y][pos_x] = reference_board[pos_y][pos_x]
                    propagate_click(game_board, reference_board, pos_x, pos_y)
                elif action == 'f':
                    game_board[pos_y][pos_x], flags = 'F', flags + 1
                hide = sum(1 for i in range(n) for j in range(m) if game_board[i][j] == '.')
                m_flags = sum(1 for i, j in mines_list if game_board[i][j] == 'F')
                mines = sum(1 for i, j in mines_list if game_board[i][j] == 'X') == 0
                check_win(game_board, reference_board, mines_list, flags)
                print_board(game_board)
            if check_win(game_board, reference_board, mines_list, flags):
                print("Bravo, vous avez gagné !")
            else:
                print("Dommage, vous avez perdu.")


# Code principal.
if __name__ == '__main__':  # import du fichier via test conditionnel
    main()  # appel à la fonction principale du jeu
