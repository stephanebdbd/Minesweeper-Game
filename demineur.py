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
from random import *  # Module random pour choisir les mines aléatoirement.
import sys  # Module sys pour récupérer les valeurs entrées au début du jeu et pour augmenter la limite récursive en fonction des dimensions du tableau.


# Définition de fonctions.
def create_board(n, m):
    """
    Fonction qui crée une matrice pour les plateaux du jeu de dimension n x m.
    Entrée : les dimensions n et m du plateau.
    Sortie : matrice de listes de strings (list[list[str]]).
    """
    return [['.' for _ in range(m)] for _ in range(n)]  # On retourne la matrice.


def print_board(board):
    """
    Affiche le plateau de jeu.
    Entrée : un plateau (list[list[str]]).
    """
    implem, (n, m) = len(str(len(board[0]) - 1)), get_size(board)  # Variable implem pour la longueur de l'implémentation.
    # n et m, les dimensions du plateau.
    for i in range(1 - len(str(m - 1)), 1):  # Boucle pour écrire les chiffres au-dessus du plateau.
        ligne = ''  # Variable pour l'écriture de la ligne
        for j in range(10 * (-i), m):  # Boucle pour décaler l'écriture de 10 places pour le chiffre de dizaine des dizaines.
            ligne += ' ' + str(j)[len(str(j)) - 1 + i]  # On ajoute progressivement les chiffres dans la variable de la ligne.
        print(' ' * (2 * (10 * (-i)) + implem + 2) + ligne)  # On imprime la ligne.
    print((implem + 1) * ' ' + ((2 * m) + 3) * '—')  # On trace une ligne pour séparer le plateau des chiffres.
    for i in range(n):  # On crée une boucle de la dimension n pour écrire les lignes et les chiffres de l'ordonnée n.
        ligne = ''  # Variable pour l'écriture de la ligne
        for j in board[i]:  # Seconde boucle pour sortir les valeurs du board.
            if j == 'X':  # Si la case est une mine,
                j = u"\u001b[31mX\u001b[0m"  # elle devient rouge.
            elif j == 'F':  # Si la case est un flag,
                j = u"\u001b[32mF\u001b[0m"  # elle devient verte.
            elif j == 'Fx':  # Si la case était un flag qui n'est pas sur une mine,
                j = u"\u001b[31mF\u001b[0m"  # elle devient rouge.
            ligne += str(j) + ' '  # On ajoute à la ligne, la ligne des valeurs.
        print(' ' * (implem - len(str(i))) + str(i) + ' | ' + str(ligne) + '|')  # On imprime la ligne.
    print((implem + 1) * ' ' + ((2 * m) + 3) * '—')  # On trace une ligne en dessous du plateau pour le fermer.


def get_size(board):
    """
    Retourne les dimensions du plateau de jeu.
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
    (n, m), voisins = get_size(board), []  # Variable des dimensions n et m du plateau et liste des coordonnées des voisins.
    for i in range(-1, 2):  # 2 boucles allant de -1 à +1 pour déterminer les cases qui entourent la case choisie.
        for j in range(-1, 2):
            if m > pos_x + j >= 0 <= pos_y + i < n and (i != 0 or j != 0):  # Si c'est une case du board et ce n'est pas la case choisie,
                voisins.append([pos_x + j, pos_y + i])  # on ajoute les coordonnées des cases voisines dans la liste "voisins".
    return voisins  # On retourne la liste "voisins".


def place_mines(reference_board, number_of_mines, first_pos_x, first_pos_y):
    """
    Fonction qui place aléatoirement les mines du jeu dans le plateau de référence.
    Entrée : la matrice du plateau de référence (List[Tuple[int,int]]), le nombre de mines et les coordonnées n et m de la première case choisie (int).
    Sortie : liste des coordonnées des cases où ont été placées les mines (List[Tuple[int,int]]).
    """
    voisins, mines_list, (n, m) = get_neighbors(reference_board, first_pos_x, first_pos_y), [], get_size(reference_board)
    # Liste des voisins de la première case choisie, une liste pour y ajouter les mines du plateau et les dimensions n et m du plateau.
    while len(mines_list) != number_of_mines:  # Tant qu'il n'y a pas autant de mines dans la liste que le nombre de mines choisi,
        ord_y, abs_x = randint(0, n - 1), randint(0, m - 1)  # On va déterminer une coordonnée de mine de manière aléatoire.
        if [ord_y, abs_x] not in mines_list and [abs_x, ord_y] not in voisins and [abs_x, ord_y] != [first_pos_x, first_pos_y]:
            # Si la mine fait déjà partie de la liste des mines, des voisins de la première case et que ce n'est pas la première case,
            reference_board[ord_y][abs_x] = 'X'  # on place la mine dans sa case au plateau de jeu de référence
            mines_list.append([ord_y, abs_x])  # et on ajoute les coordonnées de la mine en question dans la liste des mines.
    return mines_list  # On retourne la liste des mines.


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
    if game_board[pos_y][pos_x] != 'F':  # Si la case n'est pas un flag, on actualise le plateau de jeu.
        game_board[pos_y][pos_x], zero = reference_board[pos_y][pos_x], []  # zero : liste contenant les coordonnées des cases qui valent 0 si la case traitée vaut aussi 0.
        if reference_board[pos_y][pos_x] == '0':  # Si la case traitée vaut 0,
            for i, j in get_neighbors(game_board, pos_x, pos_y):  # on crée une boucle examiner les cases voisines de celle qui est traitée.
                if game_board[j][i] != 'F':  # Si la case n'est pas sous pas un flag,
                    game_board[j][i] = reference_board[j][i]  # on la dévoile.
                if game_board[j][i] == '0':  # Si l'une d'entre elles vaut 0,
                    for k, l in get_neighbors(game_board, i, j):  # on crée une boucle pour examiner toutes les cases qui l'entourent.
                        if (i, j) != (k, l) != (pos_x, pos_y) and (k, l) not in zero and game_board[l][k] != reference_board[l][k]:
                            # Si la cases n'est pas dans la liste zero, qu'elle ne correspond à aucune des cases traités plus haut et qu'elle n'a pas encore été révélée,
                            zero.append((k, l))  # on ajoute les coordonnées de cette case dans la liste zero.
            for i, j in zero:  # On crée une boucle pour traiter les cases dont les coordonnées sont dans la liste.
                propagate_click(game_board, reference_board, i, j)  # On applique la récursion à la fonction pour dévoiler les voisins de chacune d'entre elles.


def parse_input(n, m):
    """
    Permet au joueur d'entrer une chaine de caractère qui indique l'action qu'il demande sur la case qu'il a choisie.
    Entrée : les dimensions n et m du plateau (int).
    Sortie : L'action choisie (str), et la position x et la position y de la case choisie (int) le tout dans un tuple (Tuple[str, int, int]).
    """
    jeu = str(input("Choix d'une case : ")).strip().split()  # On transforme en une liste les données entrées par personnage.
    while not (len(jeu) == 3 and jeu[0] in 'CcFf' and jeu[1].isdigit() and jeu[2].isdigit() and m > int(jeu[1]) >= 0 <= int(jeu[2]) < n):
        # Tant qu'il y n'y a pas 3 éléments dans la liste qui correspondent bien aux actions déterminées et aux coordonnées qui sont dans le plateau,
        jeu = str(input("Choix d'une case : ")).strip().split()  # on redemande au joueur d'entrer ses données correctement.
    return jeu[0].lower(), int(jeu[2]), int(jeu[1])  # on retourne le tuple de données


def check_win(game_board, reference_board, mines_list, total_flags):
    """
    Fonction qui renvoie True si le joueur a gagné, sinon il renvoie False.
    Entrée : les plateaux de jeu et de référence (List[List[str]]), les coordonnées des mines (List[Tuple[int,int]]]) et le nombre de flags (int).
    Sortie : Booléen qui indique si le joueur a gagné ou pas (Bool)
    """
    (n, m), mines = get_size(game_board), sum(1 for i, j in mines_list if game_board[i][j] == 'X') == 0  # On prend les dimensions du plateau, et on vérifie s'il y a une mine.
    if not mines:  # S'il y a une mine dans le plateau :
        for i in range(n):  # On crée une double boucle pour examiner chaque case des plateaux
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
    reference_board[first_pos_y][first_pos_x], game_board[first_pos_y][first_pos_x] = '0', '0'  # La première case dévoilée est d'office un zéro dans les deux plateaux.
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
        # si le nombre de mines (supérieur à 0) est inférieur au nombre de cases disponibles moins 9 (1ère case + 8 (nombre de voisins maximal)),
        if int(sys.argv[1]) * int(sys.argv[2]) - 8 > int(sys.argv[3]) > 0 and int(sys.argv[1]) <= 100 >= int(sys.argv[2]):  # et si n et m sont inférieurs à 100,
            n, m, number_of_mines = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])  # création des variables des dimensions n et m et de celui du nombre de mines.
            sys.setrecursionlimit(n * m)  # On détermine la limite de récursion au produit des dimensions n et m.
            game_board, reference_board, mines_list = init_game(n, m, number_of_mines)  # Initialisation du début du jeu et création de variables :
            m_flags, flags, mines = sum(1 for i, j in mines_list if game_board[i][j] == 'F'), sum(1 for i, j in mines_list if game_board[i][j] == 'F'), True
            # m_flags : nombre de flags sur des mines, flags : nombre total de flags sur le plateau de jeu, mines : booléen qui indique si une mine est dévoilée,
            # win : dit si le joueur a gagné, hide : nombre de cases (hors flags) non dévoilées.
            hide, win = sum(1 for i in range(n) for j in range(m) if game_board[i][j] == '.'), check_win(game_board, reference_board, mines_list, flags)
            if not win:  # Si le joueur n'a pas gagné la partie avant qu'elle ne commence,
                while not ((m_flags == flags and hide + flags == number_of_mines) or m_flags == flags == number_of_mines) and mines:
                    # Tant que le joueur n'a pas touché de mines et qu'il n'a pas posé de flags sur les mines ou dévoilé toutes les cases sauf les mines,
                    action, pos_x, pos_y = parse_input(n, m)  # On demande au joueur les données de jeu qu'il veut entrer.
                    if action == 'c':  # Si l'action choisie par le joueur est un 'c',
                        game_board[pos_y][pos_x] = reference_board[pos_y][pos_x]  # on dévoile la case en avance au cas où c'est un flag.
                        propagate_click(game_board, reference_board, pos_x, pos_y)  # et on dévoile les cases voisines si la case est un 0.
                    else:  # Si l'action choisie par le joueur est 'f',
                        game_board[pos_y][pos_x] = 'F'  # on pose un flag sur la case choisie et on ajoute 1 au nombre total de
                    mines = sum(1 for i, j in mines_list if game_board[i][j] == 'X') == 0  # On inspecte si le joueur a choisi de dévoiler une mine.
                    m_flags, flags = sum(1 for i, j in mines_list if game_board[i][j] == 'F'), sum(1 for i, j in mines_list if game_board[i][j] == 'F')
                    # On compte le nombre de flags qui sont sur des mines et le nombre de flags sur le plateau de jeu.
                    hide = sum(1 for i in range(n) for j in range(m) if game_board[i][j] == '.')  # On compte le nombre de cases pas encore dévoilées.
                    win = check_win(game_board, reference_board, mines_list, flags)  # On vérifie si le joueur a perdu pour dévoiler toutes les mines.
                    print_board(game_board)
            if win:  # Si le joueur a gagné,
                print("Bravo, vous avez gagné !")  # on envoie un message de victoire.
            else:  # Sinon,
                print("Dommage, vous avez perdu.")  # on envoie un message de défaite.


# Code principal.
if __name__ == '__main__':  # Import du fichier via test conditionnel
    main()  # Appel à la fonction principale du jeu
