class DataCollector:

    def __init__(self, survivors, trees):
        self.survivors = survivors
        self.trees = trees

        self.collection_interval = 5000  # is this in milliseconds IDK yet???

        # data
        self.average_fitness = 0
        self.population = 0
        self.fruit_available = 0
        self.fruit_picked = 0


    def collect_data(self):
        pass
