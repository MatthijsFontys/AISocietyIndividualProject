class GenerationInfo:
    def __init__(self, population, log_info=True):
        self.summed_score = 0
        self.record_len = 1
        self.record_score = 0
        self.gather_info(population, log_info)

    def gather_info(self, population, log_info):
        # Getting the info
        for game in population:
            self.summed_score += game.get_score()
            if game.get_score() > self.record_score:
                self.record_score = game.get_score()
            if game.snake.size() > self.record_len:
                self.record_len = game.snake.size()
        if log_info:
            print('Best snake {} | {}'.format(self.record_len, self.record_score))
