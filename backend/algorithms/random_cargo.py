import random
# from load_json import load_json
# from placement_algorithm import Placement_Algorithm

class random_search:
    def __init__(self, container, cargo_items, max_iterations=1000):
        self.container = container
        self.cargo_items = cargo_items
        self.max_iterations = max_iterations
        self.best_arrangement = None
        self.best_filled_volume = 0

    def run(self):
        
        for _ in range(self.max_iterations):
            random.shuffle(self.cargo_items)
            current_arrangement = []
            current_filled_volume = 0

            for item in self.cargo_items:
                if self.container.can_place(item):
                    self.container.place(item)
                    current_arrangement.append(item)
                    current_filled_volume += item.volume

            if current_filled_volume > self.best_filled_volume:
                self.best_filled_volume = current_filled_volume
                self.best_arrangement = current_arrangement.copy()

            self.container.reset()

        return self.best_arrangement, self.best_filled_volume