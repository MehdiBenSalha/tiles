import pygame
import random
import heapq


import sys
sys.setrecursionlimit(200000) 

# Initialize Pygame
pygame.init()

# Define movement directions
DIRECTIONS = {
    'right': (0, 1, '→'),
    'down': (1, 0, '↓'),
    'left': (0, -1, '←'),
    'up': (-1, 0, '↑')
}

# Tile map for transitions
tiles_map = {
    ("right", "right"): 5, ("right", "down"): 3, ("right", "up"): 9,
    ("down", "right"): 12, ("down", "down"): 10, ("down", "left"): 9,
    ("left", "down"): 6, ("left", "left"): 5, ("left", "up"): 12,
    ("up", "right"): 6, ("up", "left"): 3, ("up", "up"): 10,
    ("left", "right"): 5, ("down", "up"): 10, ("right", "left"): 5, ("up", "down"): 10

}

# Rotation transitions
transitions = {3: 9, 9: 12, 12: 6, 6: 3, 5: 10, 10: 5,
               1: 8, 8: 4, 4: 2, 2: 1,
               7: 11, 11: 13, 13: 14, 14: 7}

# Load images for each tile
image_dict = {
    5: pygame.image.load('tiles/5.png'),
    3: pygame.image.load('tiles/3.png'),
    9: pygame.image.load('tiles/9.png'),
    12: pygame.image.load('tiles/12.png'),
    10: pygame.image.load('tiles/10.png'),
    6: pygame.image.load('tiles/6.png'),
    0: pygame.image.load('tiles/0.png')  # Placeholder for empty tile
}

# Shuffle function
def shuffle(grid, grid_size):
    new_grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    for i in range(grid_size):
        for j in range(grid_size):
            tile = grid[i][j]
            if tile == 0:
                new_grid[i][j] = 0
                continue
            rotations = random.randint(0, 3)
            for _ in range(rotations):
                tile = transitions[tile]
            new_grid[i][j] = tile
    return new_grid

# Generate a random path grid
def generate_random_path(n):
    while True:
        grid = [['empty' for _ in range(n)] for _ in range(n)]
        x, y = 0, 0
        grid[x][y] = 'start'
        path_directions = []
        while (x, y) != (n - 1, n - 1):
            valid_moves = []
            for direction, (dx, dy, _) in DIRECTIONS.items():
                nx, ny = x + dx, y + dy
                if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] == 'empty':
                    valid_moves.append((direction, nx, ny))
            if not valid_moves:
                break
            direction, x_next, y_next = random.choice(valid_moves)
            path_directions.append(direction)
            x, y = x_next, y_next
            grid[x][y] = 'path'
        if (x, y) == (n - 1, n - 1):
            grid[n - 1][n - 1] = 'end'
            return grid, path_directions

# Generate a number grid based on directions
def generate_number_grid(path_directions, grid_size):
    grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
    init_pos = (0, 0)
    for i in range(1, len(path_directions)):
        prev_dir = path_directions[i - 1]
        curr_dir = path_directions[i]
        grid[init_pos[0]][init_pos[1]] = tiles_map[(prev_dir, curr_dir)]
        if curr_dir == "right":
            init_pos = (init_pos[0], init_pos[1] + 1)
        elif curr_dir == "down":
            init_pos = (init_pos[0] + 1, init_pos[1])
        elif curr_dir == "left":
            init_pos = (init_pos[0], init_pos[1] - 1)
        elif curr_dir == "up":
            init_pos = (init_pos[0] - 1, init_pos[1])
    return grid

def rotate_tile(grid, clicked_col, clicked_row, transitions):
    """
    Rotates the tile at the specified grid position using the transitions map.
    :param grid: The current grid.
    :param clicked_col: Column of the clicked tile.
    :param clicked_row: Row of the clicked tile.
    :param transitions: Dictionary for tile rotation transitions.
    """
    tile_value = grid[clicked_row][clicked_col]
    if tile_value != 0:  # Only rotate non-empty tiles
        grid[clicked_row][clicked_col] = transitions[tile_value]  # Rotate the tile


# Display grid with images and shuffle button
def display_grid(screen, grid, tile_size=50):
    grid_size = len(grid)
    screen.fill((255, 255, 255))
    for y in range(grid_size):
        for x in range(grid_size):
            tile_value = grid[y][x]
            if tile_value in image_dict:
                tile_image = pygame.transform.scale(image_dict[tile_value], (tile_size, tile_size))
                screen.blit(tile_image, (x * tile_size, y * tile_size + 60))
            pygame.draw.rect(screen, (0, 0, 0), (x * tile_size, y * tile_size + 60, tile_size, tile_size), 2)
    

def check_win(grid, grid_size):
    
    """
    Checks if the grid is in the winning state.
    :param grid: The current grid.
    :param grid_size: Size of the grid (default is 6x6).
    :return: True if the grid is in the winning state, False otherwise.
    """
    
    for i in range (1,grid_size-1):
        for j in range(1,grid_size-1):
            if grid[i][j]==0:
                continue
            if ((grid[i][j] >>3)&1) != ((grid[i-1][j]>>1)&1):
               
                return False
            if ((grid[i][j] >>2)&1) != ((grid[i][j+1]>>0)&1):
                

                return False
            if ((grid[i][j] >>1)&1) != ((grid[i+1][j]>>3)&1):
                
                return False
            if ((grid[i][j] >>0)&1) != ((grid[i][j-1]>>2)&1):
                
                return False
    
 
    #check for the top left corner

    if ((grid[0][0] >>2)&1) != ((grid[0][0+1]>>0)&1):
        return False
    if ((grid[0][0] >>1)&1) != ((grid[0+1][0]>>3)&1):
        return False
    
    #check for the top right corner
    if ((grid[0][grid_size-1] >>0)&1) != ((grid[0][grid_size-1-1]>>2)&1):
        return False
    if ((grid[0][grid_size-1] >>1)&1) != ((grid[0+1][grid_size-1]>>3)&1):
        return False
    
    #check for the bottom left corner
    if ((grid[grid_size-1][0] >>2)&1) != ((grid[grid_size-1][0+1]>>0)&1):
        return False
    if ((grid[grid_size-1][0] >>3)&1) != ((grid[grid_size-1-1][0]>>1)&1):
        return False
    
    #check for the bottom right corner
    if ((grid[grid_size-1][grid_size-1] >>0)&1) != ((grid[grid_size-1][grid_size-1-1]>>2)&1):
        return False
    if ((grid[grid_size-1][grid_size-1] >>3)&1) != ((grid[grid_size-1-1][grid_size-1]>>1)&1):
        return False
    
    #check for the top row without the corners

    
    
    for i in range (1,grid_size-1):
        if ((grid[0][i] >>2)&1) != ((grid[0][1+i]>>0)&1):
            return False
        if ((grid[0][i] >>1)&1) != ((grid[1][i]>>3)&1):
            return False
        if ((grid[0][i] >>0)&1) != ((grid[0][i-1]>>2)&1):
            return False

#check for the bottom row without the corners
    for i in range (1,grid_size-1):
        if ((grid[grid_size-1][i] >>2)&1) != ((grid[grid_size-1][i+1]>>0)&1):
            return False
        if ((grid[grid_size-1][i] >>3)&1) != ((grid[grid_size-1-1][i]>>1)&1):
            return False
        if ((grid[grid_size-1][i] >>0)&1) != ((grid[grid_size-1][i-1]>>2)&1):
            return False
        
    #check for the left column without the corners

    for i in range (1,grid_size-1):
        if ((grid[i][0] >>3)&1) != ((grid[i-1][0]>>1)&1):
            return False
        if ((grid[i][0] >>2)&1) != ((grid[i][0+1]>>0)&1):
            return False
        if ((grid[i][0] >>1)&1) != ((grid[i+1][0]>>3)&1):
            return False
        
    #check for the right column without the corners

    for i in range (1,grid_size-1):
        if ((grid[i][grid_size-1] >>3)&1) != ((grid[i-1][grid_size-1]>>1)&1):
            return False
        if ((grid[i][grid_size-1] >>2)&1) != ((grid[i][grid_size-1-1]>>0)&1):
            return False
        if ((grid[i][grid_size-1] >>1)&1) != ((grid[i+1][grid_size-1]>>3)&1):
            return False
            
    return True
   
   
def heuristic(grid, grid_size):
    """check for every cell if is it safe or not check all directions"""
    res=0
     #     H = (tile >> 3) & 1  # Haut
    #     D = (tile >> 2) & 1  # Droite
    #     B = (tile >> 1) & 1  # Bas
    #     G = tile & 1         # Gauche
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j]==0:
                res+=1
                continue
            if i-1>=0:
                if ((grid[i][j] >>3)&1) != ((grid[i-1][j]>>1)&1):
                    continue
            if i+1<grid_size:
                if ((grid[i][j] >>1)&1) != ((grid[i+1][j]>>3)&1):
                    continue
            if j+1<grid_size:
                if ((grid[i][j] >>2)&1) != ((grid[i][j+1]>>0)&1):
                    continue
            if j-1>=0:
                if ((grid[i][j] >>0)&1) != ((grid[i][j-1]>>2)&1):
                    continue
            res+=1
    return  grid_size**2- res

class PriorityQueue(object):
    def __init__(self):
        self.queue = []
 
    def __str__(self):
        return ' '.join([str(i) for i in self.queue])
 
    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0
 
    # for inserting an element in the queue
    def insert(self, data):
        self.queue.append(data)
 
    # for popping an element based on Priority
    def delete(self):
        try:
            max_val = 0
            for i in range(len(self.queue)):
                if self.queue[i].f < self.queue[max_val].f:
                    max_val = i
            item = self.queue[max_val]
            del self.queue[max_val]
            return item
        except IndexError:
            print()
            exit()


class puzzle:
    def __init__(self, start, size):
        self.state = start
        
        self.size = size
        self.actions_possible = self.actions()
        self.parent = None
        self.level = 0
        self.h=heuristic(self.state,self.size)
        self.g=0
        self.f=self.h+self.g

    def __str__(self):
        return str(tuple(tuple(row) for row in self.state))
    
    def actions(self):
        actions = []
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i][j] != 0:
                    actions.append((i, j))
        return actions
    
    def move(self, action):
        new_state = [row[:] for row in self.state]
        i, j = action
        new_state[i][j] = transitions[new_state[i][j]]
        return new_state
    
    def is_goal(self):
        return check_win(self.state, self.size)
    
    def solve_dfs(self):
        
        path=[]
        visited = set()
        stack = [self]
        while stack:
            current = stack.pop()
            print(current)
            if current.is_goal():
                while(current.parent!=None):
                    path.append(current)
                    current=current.parent
                path.append(current)
                return path
            visited.add(current)
            for action in current.actions_possible:
                new_state = current.move(action)
                new_puzzle = puzzle(new_state, self.size)
                new_puzzle.parent = current
                new_puzzle.level = current.level + 1
                if new_puzzle not in visited:
                    stack.append(new_puzzle)
        return None
        
    def solve_astar(self):
        print("astar")
        visited = set()
        path=[]
        priority_queue = PriorityQueue()
        priority_queue.insert(self)
        while not priority_queue.isEmpty():
            current = priority_queue.delete()
            print(current)
            if current.is_goal():
                while(current.parent!=None):
                    path.append(current)
                    current=current.parent
                path.append(current)
                return path
            for action in current.actions_possible:
                new_state = current.move(action)
                new_puzzle = puzzle(new_state, self.size)
                new_puzzle.parent = current
                new_puzzle.level = current.level + 1
                new_puzzle.g = current.g + 1
                new_puzzle.h = heuristic(new_state, self.size)
                new_puzzle.f = new_puzzle.g + new_puzzle.h
                
                priority_queue.insert(new_puzzle)
        return None