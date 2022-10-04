class MyShowcaseStrat:

    def __init__(self, cols):
        self.COLS = cols
        self.data_collector = None
        self.min_fps = 10
        self.max_fps = 1000

        self.population_size = 1
        self.start_new = False
        self.load_dir = ''
        self.save_dir = ''

    def create_brain(self):
        pass

    def save_population(self):
        pass

    def get_initial_population(self):
        pass

    def get_saved_population(self):
        pass

    def repopulate(self):
        pass


