import pygame
import random
import neurolab as nl
from math import floor
from game import Game
from ai.genetic_nl import GeneticNeurolab
from ai.neuralnetwork import NeuralNetwork

# Game setup
from snake_ai.gen_info import GenerationInfo
from snake_ai.strategy.mydefault_strat import MyDefaultStrat

WIN_SIZE = 720
GRID_SIZE = 40  # 45 x 16 = 720  THERE IS A GRID BASED SYSTEM SO THAT THE FOOD AND THE SNAKE CAN REASONABLY ALIGN
COLS = floor(WIN_SIZE / GRID_SIZE)
WINDOW = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))
pygame.display.set_caption("Snake")

# Snake setup
CINEMA_MODE = False
LOAD_PREVIOUS = True  # not CINEMA_MODE
# POPULATION_SIZE = 1 if CINEMA_MODE else 100


def draw(game):
    WINDOW.fill("#292929")
    for segment in game.snake.segments:
        pygame.draw.rect(WINDOW, "#34DDC4", pos_to_rect(segment))

    pygame.draw.rect(WINDOW, "#DC1111", pos_to_rect(game.food))
    pygame.draw.rect(WINDOW, "#34DDC4", pos_to_rect(game.snake.pos))

    pygame.display.update()


def main():
    strat: MyDefaultStrat = MyDefaultStrat(COLS)
    # Game speed
    fps_cap = strat.min_fps
    slow_down = False

    # Population setup
    generation = 1
    population = strat.get_saved_population()

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
                    slow_down = not slow_down
                    fps_cap = strat.min_fps if slow_down else strat.max_fps
                elif event.button == 3:
                    strat.save_population(population)

        best_game, alive_counter = play_games(population, strat)
        draw(best_game)

        # all games died so time to create a new generation
        if alive_counter == 0:
            population = strat.repopulate(population)
            print('Starting generation: {}'.format(generation))

    pygame.quit()


# Plays games with the use of their neural network
# returns the best game to be drawn by PyGame and the alive counter for a new generation check
def play_games(population, strat: MyDefaultStrat):
    alive_counter = strat.population_size
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


def pos_to_rect(pos):
    return pygame.Rect(pos.x * GRID_SIZE, pos.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)


if __name__ == "__main__":
    main()
