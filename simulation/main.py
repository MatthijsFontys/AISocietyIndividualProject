import pygame
from random import randrange
import math
# my imports
from survivor import Survivor
from tree import Tree
from vector import Vector
from camera import Camera
from game_tick_manager import GameTickManager
from my_enums import Direction as Dir
from camera import Camera
from collision_grid import CollisionGrid

pygame.init()

# Game setup
FPS_CAP = 60  # CAMERA ISN'T SMOOTH BECAUSE FPS CAP WAS SO LOW FROM MAKING SNAKE
WORLD_SIZE = 1600
WIN_SIZE = 800
WINDOW = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))
pygame.display.set_caption("Survival")

MOVEMENT_MAP = {
    pygame.K_UP: Dir.UP,
    pygame.K_DOWN: Dir.DOWN,
    pygame.K_LEFT: Dir.LEFT,
    pygame.K_RIGHT: Dir.RIGHT
}


def draw(population, trees, camera, collision_grid):
    WINDOW.fill(pygame.Color(106, 148, 106))

    # DRAW OBJECTS HERE
    tree_size = camera.apply_zoom(80)
    creature_size = camera.apply_zoom(20)
    main_font = pygame.font.SysFont("arial", math.floor(camera.apply_zoom(48)))

    for tree in trees:  # AKA tree
        l2 = tree.position
        r2 = Vector.add_new(l2, Vector(tree_size, tree_size))
        if camera.is_in_view(l2, r2):
            offset_position = Vector.subtract_new(tree.position, camera.position)
            range_size = tree.forage_range * 2 - creature_size   # TODO: FIGURE OUT WHY THIS IS A LITTLE OFF STILL
            tree_rect = pygame.Rect(offset_position.x - tree_size / 2, offset_position.y - tree_size / 2, tree_size, tree_size)
            range_rect = pygame.Rect(offset_position.x - range_size / 2, offset_position.y - range_size / 2, range_size, range_size)
            pygame.draw.rect(WINDOW, pygame.Color(148, 22, 37), range_rect)
            pygame.draw.rect(WINDOW, pygame.Color(13, 56, 13), tree_rect)
            text = main_font.render(str(tree.food_count), True, 'white')
            text_rect = text.get_rect()
            text_rect.center = tree_rect.center
            WINDOW.blit(text, text_rect)

    for survivor in population:  # AKA survivor
        survivor.move()
        for tree in collision_grid.get_nearby_trees(survivor.position.x, survivor.position.y):
            # TODO: REMOVE STUPID TESTING LINE
            # sprint(len(collision_grid.get_nearby_trees(survivor.position.x, survivor.position.y)))
            tree.try_forage_food(survivor)

        l2 = survivor.position
        r2 = Vector.add_new(l2, Vector(creature_size, creature_size))
        if camera.is_in_view(l2, r2):
            offset_position = Vector.subtract_new(survivor.position, camera.position)
            pygame.draw.circle(WINDOW, pygame.Color(58, 103, 176), (offset_position.x - creature_size / 2, offset_position.y - creature_size / 2), creature_size)

    # GRID
    size = collision_grid.cell_size
    for i in range(collision_grid.width):
        for j in range(collision_grid.height):
            offset_position = Vector.subtract_new(Vector(i * size, j * size), camera.position)
            grid_rect = pygame.Rect(offset_position.x, offset_position.y, size, size)
            # TODO: check if is in camera view
            pygame.draw.rect(WINDOW, pygame.Color(255, 255, 255), grid_rect, 1)

    pygame.display.update()


def main():
    population = []
    for i in range(1):
        population.append(Survivor(
            Vector(randrange(WORLD_SIZE), randrange(WORLD_SIZE))
        ))

    trees = []
    for i in range(30):
        trees.append(Tree(
            Vector(randrange(WORLD_SIZE), randrange(WORLD_SIZE))
        ))

    tick_manager = GameTickManager(trees, population)
    camera = Camera(10, WIN_SIZE, WIN_SIZE, WORLD_SIZE, WORLD_SIZE)
    collision_grid = CollisionGrid(100, WORLD_SIZE, WORLD_SIZE, trees)

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
                camera.move(MOVEMENT_MAP[key])

        # draw stuff
        tick_manager.tick()
        draw(population, trees, camera, collision_grid)

    pygame.quit()


if __name__ == "__main__":
    main()
