import pygame
import numpy as np
from random import randrange, randint, choice
from math import floor
from game import Game
from data_collector import DataCollector


# Game setup
WIN_SIZE = 300
WINDOW = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))
pygame.display.set_caption("Snake")

# Snake setup
GRID_SIZE = 20  # 45 x 16 = 720  THERE IS A GRID BASED SYSTEM SO THAT THE FOOD AND THE SNAKE CAN REASONABLY ALIGN
SPEED = 1

# Genetic stuff
POPULATION = 200

def location_to_rect(arr):
    return pygame.Rect(arr[0] * GRID_SIZE, arr[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)


def draw(game):
    WINDOW.fill("black")
    pygame.draw.rect(WINDOW, "red", location_to_rect(game.food_location))
    for segment in game.snake:
        pygame.draw.rect(WINDOW, "green", location_to_rect(segment))
    pygame.display.update()


def main():
    fps_cap = 100
    # Snake setup
    generation = 1
    snake_games = []  # all games
    genetic_population = []  # only games with genetic dna
    new_population = []  # new genetic generation prep
    rand_population = []  # only games with random DNA
    data_collector = DataCollector()

    for i in range(POPULATION):
        genetic_population.append(Game(WIN_SIZE, GRID_SIZE))
        rand_population.append(Game(WIN_SIZE, GRID_SIZE))
        snake_games = np.concatenate((genetic_population, rand_population))

    best_game = snake_games[0]

    clock = pygame.time.Clock()
    should_run = True
    while should_run:
        clock.tick(fps_cap)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_run = False

        alive_counter = len(snake_games)

        for game in snake_games:
            if not game.is_alive:
                # todo: try find alternative for this alive counter
                alive_counter -= 1
                continue
            game.try_eat_food()
            game.time_alive += 1
            direction = game.choose_direction_index()
            game.move_in_direction(direction)
            # todo: fix that this game over thing is a method and a property, but the method does set the property, this is not going to be readable later
            if not game.is_game_over() and game.get_score() > best_game.get_score():
                best_game = game
            elif not best_game.is_alive:
                best_game = game

            if best_game.get_score() > 2000:
                fps_cap = 10
            else:
                fps_cap = 100

        draw(best_game)

        # all games died so do cross-over and mutation and make a new population
        if alive_counter == 0:
            data_collector.collect_data(rand_population, genetic_population)
            rand_population = []
            genetic_population.sort(key=lambda x: x.get_score(), reverse=True)
            best_games = genetic_population[:floor(POPULATION / 10)]
            print('Best score of generation: {}'.format(best_games[0].get_score()))
            for i in range(POPULATION):
                rand_population.append(Game(WIN_SIZE, GRID_SIZE))
                parent_a = None
                parent_b = None
                while parent_a == parent_b:
                    parent_a = choice(best_games)
                    parent_b = choice(best_games)

                offspring = Game(WIN_SIZE, GRID_SIZE)
                offspring.brain.cross_over(parent_a.brain, parent_b.brain)
                offspring.food_brain.cross_over(parent_a.food_brain, parent_b.food_brain)
                new_population.append(offspring)

            if generation % 10 == 0:
                data_collector.save_data(generation)
            generation += 1
            print('created generation: {}'.format(generation))
            genetic_population = new_population
            new_population = []
            snake_games = np.concatenate((genetic_population, rand_population))
            alive_counter = POPULATION

    pygame.quit()


if __name__ == "__main__":
    main()
