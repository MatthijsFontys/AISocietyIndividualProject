import pygame
import random
import math
from math import floor
from agent import Agent
from util.vector import Vector

# Game setup
WIN_SIZE = 720
GRID_SIZE = 90  # 45 x 16 = 720  THERE IS A GRID BASED SYSTEM SO THAT THE FOOD AND THE SNAKE CAN REASONABLY ALIGN
COLS = floor(WIN_SIZE / GRID_SIZE)
WINDOW = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))
pygame.display.set_caption("Genetic algorithm")
box = pygame.transform.scale(pygame.image.load('assets/box.svg').convert(), (GRID_SIZE, GRID_SIZE))

# Snake setup
POPULATION_SIZE = 300


def draw(best_path, record_index, grid, grid_entry, grid_exit):
    WINDOW.fill("#292929")

    pygame.draw.rect(WINDOW, "#496daf", pos_to_rect(grid_entry))
    pygame.draw.rect(WINDOW, "#49af9f", pos_to_rect(grid_exit))

    # Draw path
    pos = grid_entry.copy()
    for i in range(record_index):
        movement = best_path[i]
        pygame.draw.line(WINDOW, "#e63e3e", *pos_to_path_line(pos, movement))
        pos.add(movement)
        pygame.draw.rect(WINDOW, "#e63e3e", pos_to_path_rect(pos))

    # Draw grid
    for x in range(COLS):
        for y in range(COLS):
            if grid[x][y]:
                #pygame.draw.rect(WINDOW, "#cdcdcd", pos_to_rect(Vector(x, y)))
                WINDOW.blit(box, pos_to_rect(Vector(x, y)))
            else:
                pygame.draw.rect(WINDOW, "#cdcdcd", pos_to_rect(Vector(x, y)), 1)

    pygame.display.update()


def main():
    # Game speed
    fps_cap = 1000
    slow_down = False

    # Population setup
    generation = 1
    population = []

    best_all_time_path = []
    best_all_time_score = 0
    record_index = 0

    # Grid has false if no box, true if box
    grid_entry = Vector(0, 0)
    grid_exit = Vector(COLS - 1, COLS - 1)
    grid = [[False for x in range(COLS)] for y in range(COLS)]

    for i in range(POPULATION_SIZE):
        game = Agent(COLS, grid_entry, grid_exit)
        population.append(game)

    # Pygame loop
    clock = pygame.time.Clock()
    should_run = True
    while should_run:
        clock.tick(fps_cap)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 1 - left click, 2 - middle click, 3 - right click, 4 - scroll up, 5 - scroll down
                if event.button == 1:
                    toggle_box(*pygame.mouse.get_pos(), grid, grid_entry, grid_exit)
                    # reset
                    best_all_time_score = 0
                    best_all_time_path = []
                    population = reset_population(grid_entry, grid_exit)
                elif event.button == 3:
                    slow_down = not slow_down
                    fps_cap = 10 if slow_down else 1000

        for agent in population:
            if is_agent_alive(agent, grid):
                agent.move()

        # if all agents are dead
        if not any(is_agent_alive(a, grid) for a in population):
            generation += 1
            print(f'Creating generation: {generation}')
            population = repopulate(population, grid_entry, grid_exit)

        best_agent = max(population, key=lambda a: a.get_score())
        if best_agent.get_score() > best_all_time_score:
            best_all_time_score = best_agent.get_score()
            best_all_time_path = best_agent.dna.data
            record_index = best_agent.dna.index
        draw(best_all_time_path, record_index, grid, grid_entry, grid_exit)

    pygame.quit()


def toggle_box(x, y, grid, grid_entry, grid_exit):
    x = math.floor(x / GRID_SIZE)
    y = math.floor(y / GRID_SIZE)
    pos = Vector(x, y)
    if not (pos.equals(grid_entry) or pos.equals(grid_exit)):
        grid[x][y] = not grid[x][y]


def is_agent_alive(agent, grid):
    if agent.pos.x < 0 or agent.pos.y < 0:
        return False
    if agent.pos.x >= COLS or agent.pos.y >= COLS:
        return False
    if agent.dna.get_moves_remaining() == 0:
        return False
    if agent.reached_finish():
        return False
    return not grid[agent.pos.x][agent.pos.y]


def repopulate(population, grid_entry, grid_exit):
    new_population = []
    summed_score = sum(a.get_score() for a in population)
    for _ in enumerate(population):
        parent_a = pick_parent(population, summed_score)
        parent_b = pick_parent(population, summed_score)
        while parent_a == parent_b:
            parent_b = pick_parent(population, summed_score)

        offspring = Agent(COLS, grid_entry, grid_exit)
        offspring.dna.cross_over(parent_a.dna, parent_b.dna)
        new_population.append(offspring)
    return new_population


def reset_population(grid_entry, grid_exit):
    new_population = []
    for i in range(POPULATION_SIZE):
        game = Agent(COLS, grid_entry, grid_exit)
        new_population.append(game)
    return new_population

def pick_parent(population, summed_score):
    rand = random.random()
    for member in population:
        rand -= member.get_score() / summed_score
        if rand <= 0:
            return member
    print('No parent found!')
    return random.choice(population)


def pos_to_rect(pos):
    return pygame.Rect(pos.x * GRID_SIZE, pos.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)


def pos_to_path_rect(pos):
    padding_scalar = 0.3
    padding = GRID_SIZE * padding_scalar
    width = (1 - padding_scalar * 2) * GRID_SIZE
    x = pos.x * GRID_SIZE + padding
    y = pos.y * GRID_SIZE + padding
    return pygame.Rect(x, y, width, width)


def pos_to_path_line(pos, movement):
    width = 2
    start_pos = pos.x * GRID_SIZE + (GRID_SIZE / 2), pos.y * GRID_SIZE + (GRID_SIZE / 2)
    end_pos = start_pos[0] + GRID_SIZE * movement.x, start_pos[1] + GRID_SIZE * movement.y
    return start_pos, end_pos, width




if __name__ == "__main__":
    main()
