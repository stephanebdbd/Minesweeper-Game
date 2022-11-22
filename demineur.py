from random import randint, seed


def create_board(n, m):
    return [['' for _ in range(n)] for _ in range(m)]


def get_size(board):
    return len(board[0]), len(board)


def get_neighbors(board, pos_x, pos_y):
    (x, y), res = get_size(board), []
    if x > pos_x + 1 >= 0 <= pos_y + 1 < y:
        res.append([pos_x + 1, pos_y])
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
    while mines < number_of_mines:
        abs_x, ord_y = randint(0, x), randint(0, y)
        if [abs_x, ord_y] not in voisins:
            reference_board[abs_x][ord_y] = 'F'
            res.append([abs_x, ord_y])
            mines += 1
    return res
