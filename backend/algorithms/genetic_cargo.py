import random
from typing import List

class GeneticAlgorithm:
    def __init__(self, cargo_items: container,
                population_size: int =50,
                generations: int = 100,
                mutation_rate: float = 0.2):
        self.cargo_items = cargo_items
        self.container = container
        self.num_items = len(cargo_items)

        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        
        self.population = []
        self.best_solution = None
        self.best_fitness = float('inf')

    def init_population(self):
        from cargo_placement import place_cargo
        from fitness import calculate_fitness