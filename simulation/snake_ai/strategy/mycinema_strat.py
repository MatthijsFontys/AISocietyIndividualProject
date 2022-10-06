import random
from ai.neuralnetwork import NeuralNetwork
from snake_ai.game import Game
from snake_ai.gen_info import GenerationInfo


class MyCinemaStrat:

    def __init__(self, cols, population_size=10, start_new=False):
        self.SIGNATURE = 'DEFAULT_INPUT'
        self.COLS = cols
        self.data_collector = None
        self.min_fps = 10
        self.max_fps = 1000

        self.population_size = population_size
        self.start_new = start_new
        self.best_of_initial = None

    def create_brain(self):
        return NeuralNetwork(11, 4).add_layer(12).add_layer(12).build()

    def save_population(self, population):
        pass
        # for i, game in enumerate(population):
        #     game.brain.save(f'{self.SIGNATURE}_brain_{i}')

    def get_saved_population(self):
        return [Game(self.COLS, NeuralNetwork.load(f'location_input_no_collision/brain_{i}')) for i in
                range(self.population_size)]

    def get_initial_population(self):
        if self.start_new:
            return [Game(self.COLS, self.create_brain()) for _ in range(self.population_size)]
        else:
            return self.get_saved_population()

    def repopulate(self, population):
        if self.best_of_initial is None:
            self.best_of_initial = sorted(population, key=lambda x: x.get_score(), reverse=True)[:5]

        self.population_size = 1
        return [Game(self.COLS, random.choice(self.best_of_initial).brain)]

    def feed_forward(self, game):
        inputs = self.get_inputs(game)
        outputs = game.brain.feed_forward(inputs)
        highest = max(outputs)
        return outputs.index(highest)

    # would be private methods - not part of every strategy
    def get_inputs(self, game):
        segment_inputs = self.get_segment_inputs(game)
        inputs = [
            # Snake direction
            (game.snake.movement_index / 3),
            # Snake head position
            game.snake.pos.x / (self.COLS - 1),
            game.snake.pos.y / (self.COLS - 1),
            # Food position
            max(game.snake.pos.y - game.food.y, 0) / (self.COLS - 1),
            max(game.food.y - game.snake.pos.y, 0),
            max(game.food.x - game.snake.pos.x, 0),
            max(game.snake.pos.x - game.food.x, 0),
            # Rest of body position
            # Left (x is lower, y is the same) pos.x - segment.x | positive
            segment_inputs[0],
            # Right (x is higher, y is the same) pos.x - segment.x | negative
            segment_inputs[1],
            # Up (y is lower, x is the same) pos.y - segment.y | positive
            segment_inputs[2],
            # Down (y is higher, x is the same) pos.y - segment.y | negative
            segment_inputs[3],
        ]
        return inputs

    def get_segment_inputs(self, game):
        left_record = right_record = up_record = down_record = self.COLS - 1
        for segment in game.snake.segments:
            if segment.y == game.snake.pos.y:
                delta = game.snake.pos.x - segment.x
                if delta > 0:
                    left_record = min(delta, left_record)
                else:
                    right_record = min(abs(delta), right_record)
            elif segment.x == game.snake.pos.x:
                delta = game.snake.pos.y - segment.y
                if delta > 0:
                    up_record = min(delta, up_record)
                else:
                    down_record = min(abs(delta), down_record)
        output = map(lambda x: x / (self.COLS - 1), [left_record, right_record, up_record, down_record])
        return list(output)
    
