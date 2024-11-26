from enum import Enum

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

def is_adjacent_valid(grid, i, j, m, n):
    """
    Vérifie si la tuile à la position (i, j) satisfait les règles d'adjacence avec ses voisins,
    en ignorant les positions d'entrée (0,0) et de sortie (m-1,n-1).
    :param grid: La grille partielle ou complète.
    :param i: Ligne de la tuile actuelle.
    :param j: Colonne de la tuile actuelle.
    :param m: Nombre de lignes de la grille.
    :param n: Nombre de colonnes de la grille.
    :return: True si les règles d'adjacence sont respectées, False sinon.
    """
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


# --- Tests ---

# Grille de test

grid = [[5,3,1,7,3],
        [1,15,7,11,10],
        [2,14,13,9,10],
        [12,15,5,7,11],
        [0,8,0,8,12]]



#print grid
for row in grid:
    print("".join([tile_characters_dict[tile] for tile in row]))

for i in range(len(grid)):
    for j in range(len(grid[0])):
        print(is_adjacent_valid(grid, i, j, len(grid), len(grid[0])))


def draw_pipe(ax, x, y, pipe_type, connections):
    """Draws a pipe on the grid."""
    cell_size = 1
    half_size = cell_size / 2
    cx, cy = x + 0.5, y + 0.5  # Center of the cell

    # Base square
    rect = patches.Rectangle((x, y), cell_size, cell_size, edgecolor='black', facecolor='white', lw=1)
    ax.add_patch(rect)

    if pipe_type == 'empty':
        return  # Skip drawing for empty cells

    # Draw pipe connections
    directions = {
        'left': (-half_size, 0),
        'right': (half_size, 0),
        'top': (0, half_size),
        'bottom': (0, -half_size)
    }

    for direction in connections:
        dx, dy = directions[direction]
        ax.plot([cx, cx + dx], [cy, cy + dy], color='blue', lw=3)

    # Label the cell with pipe type
    ax.text(cx, cy, pipe_type[0].upper(), color='red', ha='center', va='center', fontsize=12)

def visualize_puzzle(grid):
    """Visualizes the puzzle grid."""
    n = len(grid)
    fig, ax = plt.subplots(figsize=(n, n))
    ax.set_xlim(0, n)
    ax.set_ylim(0, n)

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell is None:
                pipe_type, connections = 'empty', []
            else:
                pipe_type, connections = cell
            draw_pipe(ax, x, n - y - 1, pipe_type, connections)  # Flip y-axis for visualization

    ax.set_aspect('equal')
    ax.axis('off')
    plt.show()