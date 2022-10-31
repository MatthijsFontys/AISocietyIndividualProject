import pickle

import pygame
import os
import neat
import neurolab as nl
from math import floor

# Game setup
from snake_ai.strategy.mycinema_strat import MyCinemaStrat
from snake_ai.strategy.mydefault_strat import MyDefaultStrat
from snake_ai.strategy.mypixelinput_strat import MyPixelInputStrat
from snake_ai.strategy.neat_strat import NeatStrat
from snake_ai.strategy.neatcinema_strat import NeatCinemaStrat

WIN_SIZE = 960
GRID_SIZE = 60  # 45 x 16 = 720  THERE IS A GRID BASED SYSTEM SO THAT THE FOOD AND THE SNAKE CAN REASONABLY ALIGN
COLS = floor(WIN_SIZE / GRID_SIZE)
WINDOW: pygame.surface.Surface
pygame.display.set_caption("Snake AI")

# Snake setup
CINEMA_MODE = False
LOAD_PREVIOUS = True  # not CINEMA_MODE


def draw(game):
    WINDOW.fill("#292929")
    for segment in game.snake.segments:
        pygame.draw.rect(WINDOW,  "#34DDC4", pos_to_rect(segment))

    pygame.draw.rect(WINDOW, "#DC1111", pos_to_rect(game.food))
    pygame.draw.rect(WINDOW, "#34DDC4", pos_to_rect(game.snake.pos))

    pygame.display.update()


def main():
    strats = [MyDefaultStrat(COLS, start_new=True), MyPixelInputStrat(COLS), MyCinemaStrat(COLS),
              NeatStrat(COLS, start_new=True), NeatCinemaStrat(COLS)]
    #strat = strats[-1]
    strat = strats[-1]
    # Game speed
    fps_cap = strat.min_fps
    slow_down = False

    # Population setup
    generation = 1
    no_pygame_save_interval = 500
    pygame_threshold = 5
    population = []

    clock = pygame.time.Clock()
    # Todo: put these values in the strats instead
    should_run_pygame = True
    should_run_neat = False
    if should_run_neat:
        winner: neat.genome.DefaultGenome = strat.neat_population.run(lambda genomes, config: run_neat(strat, genomes))
        population = strat.get_initial_population([(1, winner)])
        with open(f'nets/trained/snake_80mil_winner.pkl', 'wb') as save_file:
            pickle.dump(winner, save_file)
    else:
        population = strat.get_initial_population()

    while not strat.should_run_pygame:
        _, alive_counter = play_games(population, strat)
        if alive_counter == 0:
            population = strat.repopulate(population)
            generation += 1
            print('Starting generation: {}'.format(generation))
            if generation % no_pygame_save_interval == 0:
                strat.save_population(population)
            if generation == pygame_threshold:
                strat.should_run_pygame = True

    init_window()
    while strat.should_run_pygame:
        clock.tick(fps_cap)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                strat.should_run_pygame = False
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
            generation += 1
            print('Starting generation: {}'.format(generation))

    pygame.quit()


def run_neat(strat, genomes):
    population = strat.get_initial_population(genomes)
    alive_counter = len(population)
    while alive_counter > 0:
        _, alive_counter = play_games(population, strat)
    strat.score_genomes(population)


# Plays games with the use of their neural network
# returns the best game to be drawn by PyGame and the alive counter for a new generation check
def play_games(population, strat: MyDefaultStrat):
    alive_counter = len(population)
    best_game = population[0]

    # Controlling all games in the population
    for game in population:
        if not game.is_alive():
            alive_counter -= 1
            continue
        game.time_alive += 1
        direction = strat.feed_forward(game)
        game.move_in_direction(direction)
        game.try_eat_food()

        if not best_game.is_alive() or game.get_score() > best_game.get_score():
            best_game = game

    return best_game, alive_counter


def pos_to_rect(pos):
    return pygame.Rect(pos.x * GRID_SIZE, pos.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)


def init_window():
    global WINDOW
    WINDOW = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))
    #WINDOW =pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


if __name__ == "__main__":
    main()
