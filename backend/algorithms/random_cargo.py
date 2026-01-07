"""
Random search algorithm for cargo container loading.
Tries random orderings and keeps the best solution found.
"""

import random
from typing import List
from copy import deepcopy

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from main import Cargo, Container, Solution
from cargo_placement import place_cargo
from fitness import calculate_fitness


def random_search(cargo_items: List[Cargo], 
                 container: Container, 
                 max_iterations: int = 1000,
                 verbose: bool = False) -> Solution:
    """
    Random search algorithm - tries random orderings.
    
    Args:
        cargo_items: List of Cargo objects to place
        container: Container object with dimensions
        max_iterations: Number of random orders to try
        verbose: If True, print progress updates
        
    Returns:
        Best solution found
    """
    best_solution = None
    best_fitness = float('inf')
    
    # Generate list of cargo IDs
    num_cargo = len(cargo_items)
    
    for iteration in range(max_iterations):
        # Generate random order (permutation)
        order = list(range(num_cargo))
        random.shuffle(order)
        
        # Place cargo using this order
        solution = place_cargo(order, cargo_items, container)
        
        # Calculate fitness
        fitness, violations = calculate_fitness(solution)
        solution.fitness = fitness
        solution.violations = violations
        
        # Keep track of best solution
        if fitness < best_fitness:
            best_solution = solution
            best_fitness = fitness
            
            if verbose:
                print(f"Iteration {iteration+1}: New best fitness = {fitness:.2f}")
            
            # If perfect solution found, stop early
            if fitness == 0.0:
                if verbose:
                    print(f"Perfect solution found at iteration {iteration+1}!")
                break
        
        # Progress update every 100 iterations
        if verbose and (iteration + 1) % 100 == 0:
            print(f"Iteration {iteration+1}/{max_iterations}, Best fitness so far: {best_fitness:.2f}")
    
    if verbose:
        print(f"\nRandom Search Complete:")
        print(f"  Total iterations: {iteration+1}")
        print(f"  Best fitness: {best_fitness:.2f}")
        print(f"  Solution complete: {best_solution.complete}")
        print(f"  Violations: {best_solution.violations}")
    
    return best_solution