import pygame
import numpy as np
import random
from math import floor
from game import Game
from data_collector import DataCollector


# Game setup
WIN_SIZE = 240
WINDOW = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))
pygame.display.set_caption("Snake")

# Snake setup
GRID_SIZE = 20  # 45 x 16 = 720  THERE IS A GRID BASED SYSTEM SO THAT THE FOOD AND THE SNAKE CAN REASONABLY ALIGN
SPEED = 1

# Genetic stuff
POPULATION = 300

def location_to_rect(arr):
    return pygame.Rect(arr[0] * GRID_SIZE, arr[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)


def draw(game):
    WINDOW.fill("black")
    #pygame.draw.rect(WINDOW, "red", location_to_rect(game.food_location))
    for segment in game.snake:
        pygame.draw.rect(WINDOW, "green", location_to_rect(segment))
    pygame.display.update()


def main():
    fps_cap = 1000
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
        # snake_games = np.concatenate((genetic_population, rand_population))
        snake_games = genetic_population

    food_locations = []
    for i in range(20):
        food_locations.append(snake_games[0].get_random_location())

    for game in snake_games:
        game.set_initial_food(food_locations)

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
            game.try_eat_food(food_locations)
            game.time_alive += 1
            direction = game.choose_direction_index()
            game.move_in_direction(direction)
            # todo: fix that this game over thing is a method and a property, but the method does set the property, this is not going to be readable later
            if not game.is_game_over() and game.get_score() > best_game.get_score():
                best_game = game
            elif not best_game.is_alive:
                best_game = game

            if generation > 300:
                fps_cap = 10
            else:
                fps_cap = 1000

        draw(best_game)

        # all games died so do cross-over and mutation and make a new population
        if alive_counter == 0:
            # collect data of the current generation before creating the new one
            #data_collector.collect_data(rand_population, genetic_population)
            rand_population = []

            summed_score = 0
            record_len = 1
            for game in genetic_population:
                summed_score += game.get_score()
                if len(game.snake) > record_len:
                    record_len = len(game.snake)

            # ('Best snake {}'.format(record_len))
            print('Best snake {}'.format(game.get_score()))

            for i in range(POPULATION):
                rand_population.append(Game(WIN_SIZE, GRID_SIZE))
                parent_a = pick_parent(genetic_population, summed_score)
                parent_b = pick_parent(genetic_population, summed_score)
                while parent_a == parent_b:
                    parent_b = pick_parent(genetic_population, summed_score)
                # parent_a = None
                # parent_b = None
                # while parent_a == parent_b:
                #     parent_a = pick_parent(genetic_population, summed_score)
                #     parent_b = pick_parent(genetic_population, summed_score)

                offspring = Game(WIN_SIZE, GRID_SIZE)
                offspring.brain.cross_over(parent_a.brain, parent_b.brain)
                offspring.food_brain.cross_over(parent_a.food_brain, parent_b.food_brain)
                new_population.append(offspring)

            if generation % 10 == 0 and False:
                data_collector.save_data(generation)
            generation += 1
            print('created generation: {}'.format(generation))
            genetic_population = new_population
            new_population = []
            # snake_games = np.concatenate((genetic_population, rand_population))
            snake_games = genetic_population

    pygame.quit()


def pick_parent(population, summed_score):
    rand = random.random()
    for member in population:
        rand -= member.get_score() / summed_score
        if rand <= 0:
            return member
    print('No parent found!')
    return random.choice(population)


if __name__ == "__main__":
    main()
