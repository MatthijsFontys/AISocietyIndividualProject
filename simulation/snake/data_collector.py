import pandas as pd
from pathlib import Path

class DataCollector:

    def __init__(self):
        self.random_best = []
        self.genetic_best = []

    def collect_data(self, rand_population, genetic_population):
        rand_score = max(rand_population, key=lambda x: len(x.snake))
        genetic_score = max(genetic_population, key=lambda x: len(x.snake))
        self.random_best.append(len(rand_score.snake))
        self.genetic_best.append(len(genetic_score.snake))

    def save_data(self, generation):
        filepath = Path('data/genetic_vs_random_gen_1_to_{}.csv'.format(generation))
        df = pd.DataFrame({
           'random best': self.random_best,
           'genetic best': self.genetic_best
        })
        df.index += 1
        df.index.name = 'gen'
        df.to_csv(filepath)
