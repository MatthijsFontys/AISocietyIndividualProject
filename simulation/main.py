import math

import pygame
from math import pi, tau
from random import randrange

# my imports
from entities.survivor import Survivor
from entities.tree import Tree
from util.vector import Vector
from world.game_tick_manager import GameTickManager
from util.util_enums import Direction as Dir
from drawing.camera import Camera
from world.collision_grid import CollisionGrid

# my drawing imports
from drawing.grid_painter import GridPainter
from drawing.tree_painter import TreePainter
from drawing.survivor_painter import SurvivorPainter

# Neural network
from ai.neuralnetwork import NeuralNetwork

pygame.init()

# Game setup
FPS_CAP = 60  # CAMERA WASN'T SMOOTH BECAUSE FPS CAP WAS SO LOW FROM MAKING SNAKE
WORLD_SIZE = 1600
WIN_SIZE = 900
WINDOW = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))
pygame.display.set_caption("Survival")

# Allow a playable character for debugging
PLAYABLE_CHAR = False
PLAYER_SPEED = 3
MOUSE_SPEED = 10
PLAYER_MAP = {
    pygame.K_UP: [0, -PLAYER_SPEED],
    pygame.K_DOWN: [0, PLAYER_SPEED],
    pygame.K_LEFT: [-PLAYER_SPEED, 0],
    pygame.K_RIGHT: [PLAYER_SPEED, 0]
}

# Map from pygame keys to my enum to keep layers seperate
MOVEMENT_MAP = {
    pygame.K_UP: Dir.UP,
    pygame.K_DOWN: Dir.DOWN,
    pygame.K_LEFT: Dir.LEFT,
    pygame.K_RIGHT: Dir.RIGHT
}


def draw(tree_painter: TreePainter, survivor_painter, grid_painter):
    WINDOW.fill(pygame.Color(106, 148, 106))

    tree_painter.paint(survivor_painter.survivor_radius, False)
    survivor_painter.paint()
    # todo: fix drawing the grid, the zoom broke it
    grid_painter.paint(False)

    pygame.display.update()


def main():
    population = []
    if PLAYABLE_CHAR:
        population.append(Survivor(Vector(400, 400)))
    for i in range(50):
        population.append(Survivor(
            Vector(randrange(WORLD_SIZE), randrange(WORLD_SIZE))
        ))

    trees = []

    for i in range(15):
        trees.append(Tree(
            Vector(randrange(WORLD_SIZE), randrange(WORLD_SIZE))
        ))

    # world managing objects
    tick_manager = GameTickManager(trees, population)
    collision_grid = CollisionGrid(200, WORLD_SIZE, WORLD_SIZE, trees)

    # drawing objects
    camera = Camera(MOUSE_SPEED, WIN_SIZE, WIN_SIZE, WORLD_SIZE, WORLD_SIZE)
    grid_painter = GridPainter(WINDOW, camera, collision_grid)
    survivor_painter = SurvivorPainter(WINDOW, camera, population)
    tree_painter = TreePainter(WINDOW, camera, trees)

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
                if event.button == 4:
                    camera.set_zoom(True, *mouse_pos)
                elif event.button == 5:
                    camera.set_zoom(False, *mouse_pos)

        # Player and camera movement
        keys = pygame.key.get_pressed()
        for key in MOVEMENT_MAP.keys():
            if keys[key]:
                if PLAYABLE_CHAR:
                    player_dir = PLAYER_MAP[key]
                    player = population[0]
                    player.position.add(Vector(player_dir[0], player_dir[1]))
                    camera.follow_player(player.position)
                else:
                    camera.move(MOVEMENT_MAP[key])

        # Handling the game world
        tick_manager.tick()

        # Actions before drawing
        do_survivor_actions(population, collision_grid)

        # Drawing
        draw(tree_painter, survivor_painter, grid_painter)

    pygame.quit()


def do_survivor_actions(population, grid: CollisionGrid):
    for survivor in population:
        # getting the inputs for the neural network and performing the chosen action
        tree = grid.get_closest_tree(survivor.position.x, survivor.position.y)
        tree_x_dist = 1
        tree_y_dist = 1
        tree_fruit_count = 0

        # todo: make a nullable survivor and tree instead
        if tree is not None:
            tree_x_dist = (survivor.position.x - tree.position.x) / WORLD_SIZE
            tree_y_dist = (survivor.position.y - tree.position.y) / WORLD_SIZE
            tree_fruit_count = tree.food_count / tree.max_food_count

        inputs = [
            survivor.fullness / 100,
            survivor.position.x / WORLD_SIZE,
            survivor.position.y / WORLD_SIZE,
            tree_x_dist,
            tree_y_dist,
            tree_fruit_count
        ]

        outputs = survivor.brain.feed_forward(inputs)
        action_index = outputs.index(max(outputs))

        # do stuff as survivor
        survivor.move(action_index + 1)
        if tree is not None:
            tree.try_forage_food(survivor)


if __name__ == "__main__":
    main()
