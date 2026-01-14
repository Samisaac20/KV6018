import random
import time
from typing import List

from main import Cargo, Container, Solution, place_cargo, calculate_fitness

class RandomSearch:
    """
    Random search baseline algorithm.
    Tries random orderings and keeps the best solution found.
    """

    def __init__(self, cargo_items: List[Cargo], container: Container):
        self.cargo_items = cargo_items
        self.container = container
        self.num_items = len(cargo_items)
        
        # State
        self.best_solution = None
        self.best_fitness = float('inf')
        self.history = []

    def run(self, max_iterations: int = 1000, verbose: bool = True) -> Solution:
        """
        Run random search for specified iterations.

        Args:
            max_iterations: Number of random attempts
            verbose: Print progress

        Returns:
            Best solution found
        """

        if verbose:
            print("\n" + "=" * 70)
            print("RANDOM SEARCH ALGORITHM")
            print("=" * 70)
            print(f"Items: {self.num_items}")
            print(f"Container: {self.container.width}m × {self.container.depth}m")
            print(f"Max iterations: {max_iterations}")
            print("-" * 70)

        start_time = time.time()
        improvements = 0

        for iteration in range(max_iterations):
            # Generate random ordering
            order = list(range(self.num_items))
            random.shuffle(order)

            # Place cargo using this ordering
            solution = place_cargo(order, self.cargo_items, self.container)

            # Calculate fitness
            calculate_fitness(solution)
            fitness = solution.fitness

            # Track history
            if iteration % 10 == 0:
                self.history.append((iteration, fitness))

            # Update best solution
            if fitness < self.best_fitness:
                self.best_fitness = fitness
                self.best_solution = solution
                improvements += 1

                if verbose and iteration % 100 == 0:
                    num_placed = sum(1 for c in solution.cargo_items if c.placed)
                    print(f"Iteration {iteration:4d}: New best! "
                          f"Fitness={fitness:.2f}, Placed={num_placed}/{self.num_items}")

            elif verbose and iteration > 0 and iteration % 200 == 0:
                print(f"Iteration {iteration:4d}: Current={fitness:.2f}, "
                      f"Best={self.best_fitness:.2f}")
            
            # Perfect solution found
            if self.best_fitness == 0.0:
                if verbose:
                    print(f"\n PERFECT SOLUTION FOUND at iteration {iteration}!")
                break

        elapsed = time.time() - start_time

        if verbose:
            print("-" * 70)
            print("Random Search Complete!")
            print(f"Time: {elapsed:.2f}s")
            print(f"Improvements: {improvements}")
            print(f"Best fitness: {self.best_fitness:.2f}")

            num_placed = sum(1 for c in self.best_solution.cargo_items if c.placed)
            print(f"Items placed: {num_placed}/{self.num_items}")

            com = self.best_solution.get_center_of_mass()
            print(f"Center of mass: ({com[0]:.2f}, {com[1]:.2f})")
            print("=" * 70)

        return self.best_solution

    def get_statistics(self) -> dict:
        """Return statistics about the search."""
        return {
            "best_fitness": self.best_fitness,
            "iterations_run": len(self.history) * 10 if self.history else 0,
            "history": self.history,
        }
