import random

class TileType(Enum):
    EMPTY = 0
    Open_E = 1
    Open_S = 2
    Open_W = 4
    Open_N = 8
    Corner_NW = 9
    Corner_SE = 6
    Corner_SW = 3
    Corner_NE = 12
    Straight_NS = 10
    Straight_EW = 5
    Cross = 15
    T_NEW = 13
    T_NES = 14
    T_NSW = 11
    T_SEW = 7

    

# class Tile:
#     def __init__(self, tile_type):
#         self.type = tile_type
#         self.rotation = 0

#     def rotate(self):
#         # Implement rotation logic based on the tile type and current rotation
#         self.type = (self.type << 1) & 15 | (self.type >> 3)

# class PipePuzzle:
#     def __init__(self, rows, cols):
#         self.grid = [[Tile(TileType.EMPTY) for _ in range(cols)] for _ in range(rows)]
#         self.rows = rows
#         self.cols = cols

    
    def is_adjacent_valid(grid, i, j, m, n):

        tile = grid[i][j]
        H = (tile >> 3) & 1  # Haut
        D = (tile >> 2) & 1  # Droite
        B = (tile >> 1) & 1  # Bas
        G = tile & 1         # Gauche

        # Cas 1 : Vérifier les règles pour la première ligne (i = 0) et colonne
        if i == 0 and j > 0:
            return check_left(grid, i, j, G) and check_single_open_side(grid, i, j, H, D, B, G)

        # Cas 2 : Vérifier les règles pour la première colonne (j = 0)
        if j == 0 and i > 0:
            return check_above(grid, i, j, H) and check_single_open_side(grid, i, j, H, D, B, G)

        # Cas 3 : Vérification générale pour les autres cas (haut et gauche)
        if 0 < i <= m - 1 and 0 < j <= n - 1:
            if not (check_above(grid, i, j, H) and check_left(grid, i, j, G)):
                return False
            return check_single_open_side(grid, i, j, H, D, B, G)

        return True

# --- Fonctions de vérification des côtés ---

def check_left(grid, i, j, G):
    """
    Vérifie l'adjacence avec la tuile à gauche.
    :param grid: La grille partielle ou complète.
    :param i: Ligne de la tuile actuelle.
    :param j: Colonne de la tuile actuelle.
    :param G: Le bit gauche de la tuile actuelle.
    :return: True si l'adjacence est valide, False sinon.
    """
    if j > 0:  # Vérifie s'il y a une tuile à gauche
        left_tile = grid[i][j - 1]
        left_D = (left_tile >> 2) & 1  # Le bit "Droite" de la tuile à gauche
        if G != left_D:  # Si la gauche ne correspond pas à la droite de la tuile à gauche
            return False
    return True

def check_above(grid, i, j, H):
    """
    Vérifie l'adjacence avec la tuile au-dessus.
    :param grid: La grille partielle ou complète.
    :param i: Ligne de la tuile actuelle.
    :param j: Colonne de la tuile actuelle.
    :param H: Le bit haut de la tuile actuelle.
    :return: True si l'adjacence est valide, False sinon.
    """
    if i > 0:  # Vérifie s'il y a une tuile au-dessus
        above_tile = grid[i - 1][j]
        above_B = (above_tile >> 1) & 1  # Le bit "Bas" de la tuile au-dessus
        if H != above_B:  # Si le haut de la tuile courante ne correspond pas au bas de la tuile au-dessus
            return False
    return True

def check_below(grid, i, j, B):
    """
    Vérifie l'adjacence avec la tuile en dessous.
    :param grid: La grille partielle ou complète.
    :param i: Ligne de la tuile actuelle.
    :param j: Colonne de la tuile actuelle.
    :param B: Le bit bas de la tuile actuelle.
    :return: True si l'adjacence est valide, False sinon.
    """
    if i < len(grid) - 1:  # Vérifie s'il y a une tuile en dessous
        below_tile = grid[i + 1][j]
        below_H = (below_tile >> 3) & 1  # Le bit "Haut" de la tuile en dessous
        if B != below_H:  # Si le bas de la tuile courante ne correspond pas au haut de la tuile en dessous
            return False
    return True

def check_single_open_side(grid, i, j, H, D, B, G):
    """
    Vérifie si la tuile courante a un seul côté ouvert et si les tuiles adjacentes (haut, bas, gauche et droite)
    ne capturent pas deux bords adjacents de nature différente (ouverte vs fermée).
    :param grid: La grille partielle ou complète.
    :param i: Ligne de la tuile actuelle.
    :param j: Colonne de la tuile actuelle.
    :param H: Le bit haut de la tuile actuelle.
    :param D: Le bit droite de la tuile actuelle.
    :param B: Le bit bas de la tuile actuelle.
    :param G: Le bit gauche de la tuile actuelle.
    :return: True si l'adjacence est valide, False sinon.
    """
    open_sides = sum([H, D, B, G])
    if open_sides == 1:  # Si la tuile courante n'a qu'un seul côté ouvert
        # Vérification des tuiles adjacentes : haut et gauche
        if i > 0:  # Vérification du voisin du dessus
            above_tile = grid[i - 1][j]
            above_open_sides = sum([(above_tile >> 3) & 1, (above_tile >> 2) & 1, (above_tile >> 1) & 1, above_tile & 1])
            if above_open_sides == 1:  # Si la tuile du dessus a un seul côté ouvert
                return False

        if j > 0:  # Vérification du voisin à gauche
            left_tile = grid[i][j - 1]
            left_open_sides = sum([(left_tile >> 3) & 1, (left_tile >> 2) & 1, (left_tile >> 1) & 1, left_tile & 1])
            if left_open_sides == 1:  # Si la tuile à gauche a un seul côté ouvert
                return False
    return True

#test is adjacent valid function

    def test_is_adjacent_valid():
        grid = [[Tile(TileType.EMPTY) for _ in range(3)] for _ in range(3)]
        grid[0][0].type = TileType.Open_E
        grid[0][1].type = TileType.Open_W
        grid[0][2].type = TileType.Open_E
        grid[1][0].type = TileType.Open_S
        grid[1][1].type = TileType.Cross
        grid[1][2].type = TileType.Open_N
        grid[2][0].type = TileType.Open_N
        grid[2][1].type = TileType.Open_S
        grid[2][2].type = TileType.Open_N

        assert is_adjacent_valid(grid, 0, 0, 3, 3) == False


    def solve_puzzle(self):
        # Implement a solver algorithm, such as depth-first search or A*
        # Consider optimization techniques and heuristics

    def is_solved(self):
        # Check if the puzzle is solved, e.g., if fluid can flow from source to destination

    def display_puzzle(self):
        # Visualize the puzzle using a library like Pygame or ASCII art

# Example usage:
puzzle = PipePuzzle(5, 5)
puzzle.generate_puzzle()
puzzle.display_puzzle()

# Solve the puzzle
puzzle.solve_puzzle()
puzzle.display_puzzle()