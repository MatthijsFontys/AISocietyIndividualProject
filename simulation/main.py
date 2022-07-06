import pygame
from random import randrange

# my imports
from survivor import Survivor
from tree import Tree
from vector import Vector
from game_tick_manager import GameTickManager
from my_enums import Direction as Dir
from drawing.camera import Camera
from collision_grid import CollisionGrid

# my drawing imports
from drawing.grid_painter import GridPainter
from drawing.tree_painter import TreePainter
from drawing.survivor_painter import SurvivorPainter

pygame.init()

# Game setup
FPS_CAP = 60  # CAMERA WASN'T SMOOTH BECAUSE FPS CAP WAS SO LOW FROM MAKING SNAKE
WORLD_SIZE = 1600
WIN_SIZE = 800
WINDOW = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))
pygame.display.set_caption("Survival")

# Allow a playable character for debugging
PLAYABLE_CHAR = True
PLAYER_SPEED = 3
PLAYER_MAP = {
    pygame.K_UP: [0, -PLAYER_SPEED],
    pygame.K_DOWN: [0, PLAYER_SPEED],
    pygame.K_LEFT: [-PLAYER_SPEED, 0],
    pygame.K_RIGHT: [PLAYER_SPEED, 0]
}

MOVEMENT_MAP = {
    pygame.K_UP: Dir.UP,
    pygame.K_DOWN: Dir.DOWN,
    pygame.K_LEFT: Dir.LEFT,
    pygame.K_RIGHT: Dir.RIGHT
}


def draw(tree_painter: TreePainter, survivor_painter, grid_painter):
    WINDOW.fill(pygame.Color(106, 148, 106))

    tree_painter.paint(survivor_painter.survivor_radius)
    survivor_painter.paint()
    grid_painter.paint()

    pygame.display.update()


def main():
    population = []
    if PLAYABLE_CHAR:
        population.append(Survivor(Vector(400, 400)))
    for i in range(100):
        population.append(Survivor(
            Vector(randrange(WORLD_SIZE), randrange(WORLD_SIZE))
        ))

    trees = []
    for i in range(30):
        trees.append(Tree(
            Vector(randrange(WORLD_SIZE), randrange(WORLD_SIZE))
        ))

    # world managing objects
    tick_manager = GameTickManager(trees, population)
    collision_grid = CollisionGrid(50, WORLD_SIZE, WORLD_SIZE, trees)

    # drawing objects
    camera = Camera(PLAYER_SPEED, WIN_SIZE, WIN_SIZE, WORLD_SIZE, WORLD_SIZE)
    grid_painter = GridPainter(WINDOW, camera, collision_grid)
    survivor_painter = SurvivorPainter(WINDOW, camera, population)
    tree_painter = TreePainter(WINDOW, camera, trees)


    clock = pygame.time.Clock()
    should_run = True
    zoom_speed = 0  # 10 or something when not testing or when zoom isn't broken anymore
    while should_run:
        clock.tick(FPS_CAP)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    camera.set_zoom(zoom_speed)
                elif event.button == 5:
                    camera.set_zoom(-zoom_speed)

        keys = pygame.key.get_pressed()
        for key in MOVEMENT_MAP.keys():
            if keys[key]:
                if PLAYABLE_CHAR:
                    dir = PLAYER_MAP[key]
                    player = population[0]
                    player.position.add(Vector(dir[0], dir[1]))
                    camera.follow_player(player.position)
                else:
                    camera.move(MOVEMENT_MAP[key])

        # draw stuff
        tick_manager.tick()
        draw(tree_painter, survivor_painter, grid_painter)

    pygame.quit()


if __name__ == "__main__":
    main()
