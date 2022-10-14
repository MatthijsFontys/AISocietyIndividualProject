import math

import pygame
from math import pi, tau
from random import randrange

# my imports
from entities.entity_enums import EntityType
from entities.survivor import Survivor
from entities.tree import Tree
from util.vector import Vector
from util.vector_pool import VectorPool
from world.game_tick_manager import GameTickManager
from util.util_enums import Direction as Dir
from drawing.camera import Camera
from world.collision_grid import CollisionGrid

# my drawing imports
from drawing.grid_painter import GridPainter
from drawing.tree_painter import TreePainter
from drawing.survivor_painter import SurvivorPainter

pygame.init()

VECTOR_POOL = VectorPool()

# Game setup
FPS_CAP = 60  # CAMERA WASN'T SMOOTH BECAUSE FPS CAP WAS SO LOW FROM MAKING SNAKE
WORLD_SIZE = 1600  # Todo: Make it so stuff like this is in world object
WIN_SIZE = 900
WINDOW = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))
pygame.display.set_caption("Map creator for survival sim")

# Allow a playable character for debugging
MOUSE_SPEED = 10

# Map from pygame keys to my enum to keep layers seperate
MOVEMENT_MAP = {
    pygame.K_UP: Dir.UP,
    pygame.K_DOWN: Dir.DOWN,
    pygame.K_LEFT: Dir.LEFT,
    pygame.K_RIGHT: Dir.RIGHT
}


def draw(trees, tree_sprite, camera):
    WINDOW.fill(pygame.Color(106, 148, 106))
    tree_size = camera.apply_zoom(80)
    tree_sprite = pygame.transform.scale(tree_sprite, (tree_size, tree_size))

    for tree in trees:
        l2 = VECTOR_POOL.acquire(tree.x - tree_size / 2, tree.y - tree_size / 2)
        r2 = VECTOR_POOL.acquire(tree.x + tree_size / 2, tree.y + tree_size / 2)
        if camera.is_in_view(l2, r2 or True):
            pos = camera.map_to_camera(tree)
            # Why in the world does this need to be - half tree size? I thought I already translated it.
            # Todo: make something so that I have to stop translating so much because it causes bugs every single time
            # Todo: figure out why the position is widly off when placing trees when not entirely zoomed out
            WINDOW.blit(tree_sprite, (pos.x - tree_size / 2, pos.y - tree_size / 2))
        VECTOR_POOL.release(l2, r2)

    # Draw tree at mouse pos
    mouse_pos = pygame.mouse.get_pos()
    mouse_pos = VECTOR_POOL.acquire(mouse_pos[0], mouse_pos[1])
    WINDOW.blit(tree_sprite, (mouse_pos.x - tree_size / 2, mouse_pos.y - tree_size / 2))
    VECTOR_POOL.release(mouse_pos)

    # Draw grid
    # Draw trees
    pygame.display.update()


def main():
    tree_sprite = pygame.image.load('../assets/fruit_tree_3.svg')
    trees = []

    #collision_grid = CollisionGrid(200, WORLD_SIZE, WORLD_SIZE, trees)
    #tree_painter = TreePainter(WINDOW, camera, trees)
    camera = Camera(MOUSE_SPEED, WIN_SIZE, WIN_SIZE, WORLD_SIZE, WORLD_SIZE)

    # pygame stuff
    clock = pygame.time.Clock()
    should_run = True

    # Main loop and camera controls
    while should_run:
        clock.tick(FPS_CAP)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # 1 - left click
                # 2 - middle click
                # 3 - right click
                # 4 - scroll up
                # 5 - scroll down
                if event.button == 4:
                    camera.set_zoom(True, *mouse_pos)
                elif event.button == 5:
                    camera.set_zoom(False, *mouse_pos)
                elif event.button == 1:
                    mouse_world_x, mouse_world_y = camera.get_mouse_world_pos(mouse_pos[0], mouse_pos[1])
                    print(*mouse_pos)
                    print(mouse_world_x, mouse_world_y)
                    trees.append(Vector(mouse_world_x, mouse_world_y))
                elif event.button == 3:
                    # Left click place tree
                    # Right click save ?
                    pass

        # Player and camera movement
        keys = pygame.key.get_pressed()
        for key in MOVEMENT_MAP.keys():
            if keys[key]:
                camera.move(MOVEMENT_MAP[key])

        # Drawing
        draw(trees, tree_sprite, camera)

    pygame.quit()



if __name__ == "__main__":
    main()
