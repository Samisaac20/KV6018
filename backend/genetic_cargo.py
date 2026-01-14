"""
KV6018 Cargo Container Loading - Genetic Algorithm
Order-based GA for cargo placement optimization
"""

import random
from typing import List

from main import Cargo, Container, Solution, place_cargo, calculate_fitness


class GeneticAlgorithm:
    """
    Genetic Algorithm for cargo container loading.
    Uses order-based encoding with bottom-left placement heuristic.
    """
    
    def __init__(
        self,
        cargo_items: List[Cargo],
        container: Container,
        population_size: int = 300,
        generations: int = 1500,
        mutation_rate: float = 0.2,
        crossover_rate: float = 0.9,
        tournament_size: int = 4,
        elite_size: int = 8,
        stagnation_limit: int = 400
    ):
        self.cargo_items = cargo_items
        self.container = container
        self.num_items = len(cargo_items)
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.tournament_size = tournament_size
        self.elite_size = elite_size
        self.stagnation_limit = stagnation_limit
        
        # State
        self.population = []
        self.best_solution = None
        self.best_fitness = float("inf")
        self.best_generation = 0
        self.fitness_history = []

    def _evaluate(self, genome: List[int]) -> tuple:
        """Evaluate a genome and return (genome, solution, fitness)."""
        solution = place_cargo(genome, self.cargo_items, self.container)
        calculate_fitness(solution)
        return (genome, solution, solution.fitness)

    def _update_best(self, solution: Solution, fitness: float, generation: int) -> bool:
        """Update best solution if fitness improved."""
        if fitness < self.best_fitness:
            self.best_fitness = fitness
            self.best_solution = solution
            self.best_generation = generation
            return True
        return False

    def initialise_population(self):
        """Create initial random population."""
        for _ in range(self.population_size):
            genome = list(range(self.num_items))
            random.shuffle(genome)
            solution = place_cargo(genome, self.cargo_items, self.container)
            calculate_fitness(solution)
            self.population.append((genome, solution, solution.fitness))

            if solution.fitness < self.best_fitness:
                self.best_fitness = solution.fitness
                self.best_solution = solution
                self.best_generation = 0

    def tournament_selection(self) -> List[int]:
        """Select parent using tournament selection."""
        tournament = random.sample(self.population, self.tournament_size)
        return min(tournament, key=lambda ind: ind[2])[0].copy()

    def order_crossover(self, parent1: List[int], parent2: List[int]) -> List[int]:
        """Order crossover (OX) for permutation encoding."""
        size = len(parent1)
        p1, p2 = sorted(random.sample(range(size), 2))

        child = [-1] * size
        child[p1 : p2 + 1] = parent1[p1 : p2 + 1]

        segment = set(child[p1 : p2 + 1])
        remaining = iter(x for x in parent2 if x not in segment)
        return [next(remaining) if x == -1 else x for x in child]

    def swap_mutation(self, genome: List[int]) -> List[int]:
        """Swap mutation for permutation encoding."""
        if random.random() >= self.mutation_rate:
            return genome
        mutated = genome.copy()
        p1, p2 = random.sample(range(len(mutated)), 2)
        mutated[p1], mutated[p2] = mutated[p2], mutated[p1]
        return mutated

    def evolve_generation(self) -> List:
        """Evolve one generation."""
        # Keep elites
        sorted_pop = sorted(self.population, key=lambda ind: ind[2])
        new_population = sorted_pop[: self.elite_size]

        # Generate offspring
        while len(new_population) < self.population_size:
            parent1, parent2 = self.tournament_selection(), self.tournament_selection()
            child = (
                self.order_crossover(parent1, parent2)
                if random.random() < self.crossover_rate
                else parent1.copy()
            )
            child = self.swap_mutation(child)
            new_population.append(self._evaluate(child))

        return new_population

    def run(self, verbose: bool = False) -> Solution:
        """
        Run the genetic algorithm.
        
        Args:
            verbose: Print progress during evolution
            
        Returns:
            Best solution found
        """
        if verbose:
            print(f"\n{'=' * 70}\nGENETIC ALGORITHM\n{'=' * 70}")
            print(f"\nPopulation: {self.population_size}, Generations: {self.generations}")
            print(f"Mutation: {self.mutation_rate}, Crossover: {self.crossover_rate}")

        self.initialise_population()
        self.fitness_history.append(self.best_fitness)

        if verbose:
            print(f"\nInitial best fitness: {self.best_fitness:.2f}\n")

        stagnant_count = 0
        original_mutation_rate = self.mutation_rate

        for gen in range(1, self.generations + 1):
            self.population = self.evolve_generation()

            improved = False

            for genome, solution, fitness in self.population:
                if fitness < self.best_fitness:
                    self.best_fitness = fitness
                    self.best_solution = solution
                    self.best_generation = gen
                    improved = True
                    stagnant_count = 0
                    self.mutation_rate = original_mutation_rate
                    if verbose:
                        print(f"Generation {gen}: New best = {fitness:.2f}")

            if not improved:
                stagnant_count += 1
                if stagnant_count >= self.stagnation_limit:
                    if verbose:
                        print(f"\n⚠ No improvement for {self.stagnation_limit} generations")
                        print(f"Stopping early at generation {gen}")
                    break

            # Adaptive mutation - increase when stagnant
            if stagnant_count > 30:
                self.mutation_rate = min(0.5, self.mutation_rate * 1.5)
                if verbose and stagnant_count == 31:
                    print(f"  Increasing mutation to {self.mutation_rate:.2f}")

            self.fitness_history.append(self.best_fitness)

            # Perfect solution found
            if self.best_fitness == 0.0:
                if verbose:
                    print(f"\n{'=' * 70}")
                    print("✓ PERFECT SOLUTION FOUND!")
                    print(f"Generation: {gen}/{self.generations}")
                    print("=" * 70)
                break

            # Progress report
            if verbose and gen % 100 == 0:
                avg = sum(ind[2] for ind in self.population) / len(self.population)
                print(f"Generation {gen}: Best={self.best_fitness:.2f}, Avg={avg:.2f}")

        if verbose:
            print(f"\n{'=' * 70}\nEVOLUTION COMPLETE\n{'=' * 70}")
            print(f"Best fitness: {self.best_fitness:.2f}")
            print(f"Found in generation: {self.best_generation}")

        return self.best_solution

    def get_statistics(self) -> dict:
        """Return statistics about the GA run."""
        return {
            "best_fitness": self.best_fitness,
            "best_generation": self.best_generation,
            "generations_run": len(self.fitness_history) - 1,
            "fitness_history": self.fitness_history,
            "population_size": self.population_size,
        }
