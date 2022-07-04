import pygame
from random import randrange

# my imports
from survivor import Survivor
from tree import Tree
from vector import Vector
from game_tick_manager import GameTickManager
from camera import Camera

pygame.init()

# Game setup
FPS_CAP = 10
WIN_SIZE = 800  # 720
WINDOW = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))
pygame.display.set_caption("Survival")


# CAMERA RELATED TODO: WILL MAKE A CAMERA CLASS LATER
WORLD_SIZE = 1600


def is_in_camera(camera_x, camera_y, l2, r2):
    # l1 = top left coordinate of camera
    # r1 = bottom right coordinate of camera
    # l1 is top left of object to check
    # r2 is bottom right of object to check
    l1 = Vector(camera_x, camera_y)
    r1 = Vector(camera_x + WIN_SIZE, camera_y + WIN_SIZE)

    to_return = False

    # if one rectangle is within the other rectangle
    if (l2.x > l1.x and l2.y > l1.y) and (r2.x < r1.x and r2.y < r1.y):
        to_return = True
    # if rectangle has area 0, no overlap
    elif l1.x == r1.x or l1.y == r1.y or r2.x == l2.x or l2.y == r2.y:
        to_return = False

    # If one rectangle is on left side of other
    elif l1.x > r2.x or l2.x > r1.x:
        to_return = False

    # If one rectangle is above other
    elif r1.y > l2.y or r2.y > l1.y:
        to_return = False

    return to_return


# Survivor actions
SPEED = 1
MOVEMENT = {pygame.K_UP: [0, -SPEED], pygame.K_DOWN: [0, SPEED], pygame.K_LEFT: [-SPEED, 0], pygame.K_RIGHT: [SPEED, 0]}

# DRAWING STUFF
FONT = pygame.font.SysFont("arial", 48)


def draw(population, trees, camera_x, camera_y):
    WINDOW.fill(pygame.Color(106, 148, 106))

    # DRAW OBJECTS HERE
    camera_position = Vector(camera_x, camera_y)
    creature_size = 20
    for survivor in population:  # AKA survivor
        survivor.move()

        for tree in trees:
            tree.try_forage_food(survivor)

        l2 = survivor.position
        r2 = Vector.add_new(l2, Vector(creature_size, creature_size))
        if is_in_camera(camera_x, camera_y, l2, r2):
            offset_position = Vector.subtract_new(survivor.position, camera_position)
            pygame.draw.circle(WINDOW, pygame.Color(58, 103, 176), (offset_position.x, offset_position.y), creature_size)

    tree_size = 80
    for tree in trees:  # AKA tree
        l2 = tree.position
        r2 = Vector.add_new(l2, Vector(tree_size, tree_size))
        if is_in_camera(camera_x, camera_y, l2, r2):
            offset_position = Vector.subtract_new(tree.position, camera_position)
            tree_rect = pygame.Rect(offset_position.x, offset_position.y, tree_size, tree_size)
            pygame.draw.rect(WINDOW, pygame.Color(13, 56, 13), tree_rect)
            text = FONT.render(str(tree.food_count), True, 'white')
            text_rect = text.get_rect()
            text_rect.center = tree_rect.center
            WINDOW.blit(text, text_rect)

    pygame.display.update()


def main():
    camera_x = 0
    camera_y = 0

    population = []
    for i in range(50):
        population.append(Survivor(
            Vector(randrange(WORLD_SIZE), randrange(WORLD_SIZE))
        ))

    trees = []
    for i in range(10):
        trees.append(Tree(
            Vector(randrange(WORLD_SIZE), randrange(WORLD_SIZE))
        ))

    tick_manager = GameTickManager(trees, population)

    clock = pygame.time.Clock()
    should_run = True
    while should_run:
        clock.tick(FPS_CAP)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_run = False

        camera_speed = 20
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            camera_x += camera_speed
        elif keys[pygame.K_LEFT]:
            camera_x -= camera_speed
        if keys[pygame.K_UP]:
            camera_y -= camera_speed
        elif keys[pygame.K_DOWN]:
            camera_y += camera_speed

        camera_x = min(camera_x, WORLD_SIZE - WIN_SIZE)
        camera_x = max(camera_x, 0)

        camera_y = min(camera_y, WORLD_SIZE - WIN_SIZE)
        camera_y = max(camera_y, 0)

        # draw stuff
        tick_manager.tick()
        draw(population, trees, camera_x, camera_y)

    pygame.quit()


if __name__ == "__main__":
    main()
