import math

import numpy as np
import random
from Sprites import Sprite


def initialize_grid(width, height):
    # Initialize grid with walls (7s)
    grid = np.full((height, width), 7, dtype=int)
    return grid

def generate_maze(width, height,p_speler_x,p_speler_y):
    # Ensure dimensions are odd for better maze structure
    if width % 2 == 0:
        width += 1
    if height % 2 == 0:
        height += 1

    p_speler_x = width // 2
    p_speler_y = height // 2

    # Create an empty grid and a stack for DFS
    maze = initialize_grid(width, height)
    stack = []

    # Carve out a 2x2 area in the center of the maze
    center_x, center_y = width // 2, height // 2
    for x in range(center_x - 1, center_x + 2):  # carve out 2x2 area
        for y in range(center_y - 1, center_y + 2):
            if 0 <= x < width and 0 <= y < height:  # check bounds
                maze[y, x] = 0

    # Start position - make sure it's inside the grid and on an odd index
    start_x, start_y = center_x, center_y
    stack.append((start_x, start_y))

    # Define the directions (up, down, left, right)
    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

    # DFS with backtracking
    while stack:
        x, y = stack[-1]
        random.shuffle(directions)  # Randomize directions for a varied maze
        moved = False

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # Check if the new cell is within bounds and still a wall
            if 1 <= nx < width - 1 and 1 <= ny < height - 1 and maze[ny, nx] == 7:
                # Carve a path between the current cell and the new cell
                maze[ny, nx] = 0
                maze[y + dy // 2, x + dx // 2] = 0
                stack.append((nx, ny))
                moved = True
                break

        if not moved:
            stack.pop()  # Backtrack if no moves are possible

    return maze, p_speler_x, p_speler_y


def is_area_free(maze, x, y, buffer_size):
    """
    Controleert of een gebied rondom (x, y) vrij is van muren.
    """
    height, width = maze.shape
    for dy in range(-buffer_size, buffer_size + 1):
        for dx in range(-buffer_size, buffer_size + 1):
            check_x = x + dx
            check_y = y + dy
            if check_x < 0 or check_x >= width or check_y < 0 or check_y >= height:
                return False  # Buiten de grenzen van de maze
            if maze[check_y, check_x] != 0:
                return False  # Niet vrij (muur of obstakel)
    return True


def spawn_sprites_in_maze(maze, sprite_count, renderer):
    sprites = []
    height, width = maze.shape
    center_x, center_y = width // 2, height // 2
    buffer_size = 2  # Voor het vermijden van het midden
    spawnedsprite = 'resources/Sprites/rijst.png'
    spawnedspritecounter = 0
    for i in range(sprite_count):
        while True:
            x = random.randint(1, width - 2)
            y = random.randint(1, height - 2)


            if spawnedspritecounter == 2:
                spawnedsprite = 'resources/Sprites/rollebolle.png'

            # Vermijd middengebied en controleer op vrij gebied
            if (
                    maze[y, x] == 0  and
                    not (center_x - buffer_size <= x <= center_x + buffer_size and
                         center_y - buffer_size <= y <= center_y + buffer_size)
            ):
                # Voeg sprite toe
                sprites.append(
                    Sprite(x=x+0.5, y=y+0.5, scale=0.4, image_path=spawnedsprite, renderer=renderer))
                break
        spawnedspritecounter += 1
    return sprites

