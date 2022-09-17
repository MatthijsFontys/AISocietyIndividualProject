import pygame
import random
from math import floor
from game import Game
from ai.genetic_nl import GeneticNeurolab
from gen_info import GenerationInfo

# Game setup
WIN_SIZE = 340
GRID_SIZE = 20  # 45 x 16 = 720  THERE IS A GRID BASED SYSTEM SO THAT THE FOOD AND THE SNAKE CAN REASONABLY ALIGN
COLS = floor(WIN_SIZE / GRID_SIZE)
WINDOW = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))
pygame.display.set_caption("Snake")

# Snake setup
POPULATION_SIZE = 200


def draw(game):
    WINDOW.fill("black")
    pygame.draw.rect(WINDOW, "red", pos_to_rect(game.food))  # todo: actual location here
    # print(game.snake.pos.x)
    # print(game.snake.pos.y)
    pygame.draw.rect(WINDOW, "green", pos_to_rect(game.snake.pos))  # todo: actual location here
    for segment in game.snake.segments:
        pygame.draw.rect(WINDOW, "green", pos_to_rect(segment))  # todo: actual location here
    pygame.display.update()


def main():
    # Game speed
    fps_cap = 1000
    slow_down = False

    # Population setup
    generation = 1
    population = [Game(COLS) for _ in range(POPULATION_SIZE)]

    # Pygame loop
    clock = pygame.time.Clock()
    should_run = True
    while should_run:
        clock.tick(fps_cap)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                slow_down = not slow_down
                fps_cap = 20 if slow_down else 1000

        best_game, alive_counter = play_games(population)
        draw(best_game)

        # all games died so time to create a new generation
        if alive_counter == 0:
            gen_info = GenerationInfo(population)
            population = repopulate(population, gen_info)
            generation += 1
            print('Starting generation: {}'.format(generation))

    pygame.quit()


# Plays games with the use of their neural network
# returns the best game to be drawn by PyGame and the alive counter for a new generation check
def play_games(population):
    alive_counter = POPULATION_SIZE
    best_game = population[0]

    # Controlling all games in the population
    for game in population:
        if not game.is_alive():
            alive_counter -= 1
            continue
        game.time_alive += 1
        direction = game.choose_direction_index()
        game.move_in_direction(direction)
        game.try_eat_food()

        if not best_game.is_alive() or game.get_score() > best_game.get_score():
            best_game = game

    return best_game, alive_counter


def repopulate(population, info):
    new_population = []
    for _ in enumerate(population):
        parent_a = pick_parent(population, info.summed_score)
        parent_b = pick_parent(population, info.summed_score)
        while parent_a == parent_b:
            parent_b = pick_parent(population, info.summed_score)

        offspring = Game(COLS)
        offspring.brain = GeneticNeurolab.cross_over(parent_a.brain, parent_b.brain)
        new_population.append(offspring)
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


if __name__ == "__main__":
    main()
