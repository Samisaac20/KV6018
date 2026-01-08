import random
from typing import List

class GeneticAlgorithm:
    def __init__(self, cargo_items: List, container,
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

        for _ in range(self.population_size):
            gnome = list(range(slef.num_items))
            random.shuffle(gnome)

            solution = place_cargo(gnome, self.cargo_items, self.container)
            fitness = calculate_fitness(solution)

            self.population.append((gnome, solution, fitness))

            if fitness < self.best.fitness:
                self.best_fitness = fitness
                self.best_solution = solution

    def select_parent(self) -> List[int]:
        individual = random.choice(self.population)
        return individual[0].copy()

    def crossover(self, parent1: List[int], parent2: List[int]) -> List[int]:
        size = len(parent1)
        point = random.randint(1, size -1)

        child = parent1[:point].copy()

        for gene in parent2:
            if gene not in child:
                child.append(gene)

        return child

    def mutate(self, genome: List[int]) -> List[int]:
        """Swap two random positions."""
        if random.random() < self.mutation_rate:
            mutated = genome.copy()
            pos1 = random.randint(0, len(mutated) - 1)
            pos2 = random.randint(0, len(mutated) - 1)
            mutated[pos1], mutated[pos2] = mutated[pos2], mutated[pos1]
            return mutated
        return genome

    def run(self, verbose: bool = False):
        """Run the genetic algorithm."""
        from cargo_placement import place_cargo
        from fitness import calculate_fitness
        
        if verbose:
            print("\nRunning basic GA...")
            print(f"Population: {self.population_size}, Generations: {self.generations}")
        
        # Initialize
        self.initialize_population()
        
        if verbose:
            print(f"Initial best fitness: {self.best_fitness:.2f}")
        
        # Evolution loop
        for generation in range(self.generations):
            new_population = []
            
            # Create new generation
            for _ in range(self.population_size):
                # Select parents
                parent1 = self.select_parent()
                parent2 = self.select_parent()
                
                # Create child
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                
                # Evaluate
                solution = place_cargo(child, self.cargo_items, self.container)
                fitness = calculate_fitness(solution)
                
                new_population.append((child, solution, fitness))
                
                # Track best
                if fitness < self.best_fitness:
                    self.best_fitness = fitness
                    self.best_solution = solution
                    if verbose:
                        print(f"Generation {generation}: New best = {fitness:.2f}")
            
            self.population = new_population
            
            # Early stopping
            if self.best_fitness == 0.0:
                if verbose:
                    print(f"\nPerfect solution found at generation {generation}!")
                break
        
        if verbose:
            print(f"\nFinal best fitness: {self.best_fitness:.2f}")
        
        return self.best_solution
    
    def get_statistics(self) -> dict:
        """Get basic statistics."""
        return {
            'best_fitness': self.best_fitness,
            'population_size': self.population_size
        }