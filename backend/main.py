#!/usr/bin/env python3
# main.py
"""
Cargo Container Loading - Main Program
KV6018 Evolutionary Computing Assessment
"""

import sys
from typing import List, Tuple, Dict
from dataclasses import dataclass

# ============================================================================
# PROBLEM DEFINITION (Data Structures)
# ============================================================================

@dataclass
class Cargo:
    """Cylindrical cargo item to be placed in container"""
    id: int
    diameter: float
    weight: float
    x: float = 0.0
    y: float = 0.0
    placed: bool = False


@dataclass
class Container:
    """Rectangular container specifications"""
    width: float
    depth: float
    max_weight: float


@dataclass
class Solution:
    """Complete solution with placement and evaluation"""
    order: List[int]
    cargo_items: List[Cargo]
    complete: bool
    fitness: float
    violations: Dict[str, float]
    container: Container
    
    def get_center_of_mass(self) -> Tuple[float, float]:
        """Calculate center of mass for placed cargo"""
        placed = [c for c in self.cargo_items if c.placed]
        if not placed:
            return (0, 0)
        
        total_weight = sum(c.weight for c in placed)
        weighted_x = sum(c.x * c.weight for c in placed)
        weighted_y = sum(c.y * c.weight for c in placed)
        
        return (weighted_x / total_weight, weighted_y / total_weight)

# ============================================================================
# MENU SYSTEM
# ============================================================================

def print_header():
    """Print program header"""
    print("\n" + "="*70)
    print("CARGO CONTAINER LOADING OPTIMIZER")
    print("KV6018 Evolutionary Computing Assessment")
    print("="*70 + "\n")


def select_instance():
    """Let user select a problem instance"""
    # Import here to avoid circular dependency
    from algorithms import load_json
    
    instances = load_json.list_all_instances()
    
    print("\nAvailable Instances:")
    print("-" * 70)
    
    # Group by category
    basic = [i for i in instances if 'basic' in i]
    challenging = [i for i in instances if 'challenge' in i]
    
    print("\nBASIC INSTANCES:")
    for idx, name in enumerate(basic, 1):
        print(f"  {idx}. {name}")
    
    print("\nCHALLENGING INSTANCES:")
    for idx, name in enumerate(challenging, len(basic) + 1):
        print(f"  {idx}. {name}")
    
    print("\n" + "-" * 70)
    
    while True:
        try:
            choice = input(f"\nSelect instance (1-{len(instances)}) or 'q' to quit: ").strip()
            
            if choice.lower() == 'q':
                return None
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(instances):
                selected = instances[choice_num - 1]
                print(f"\nSelected: {selected}")
                load_json.print_instance_info(selected)
                return selected
            else:
                print(f"Please enter a number between 1 and {len(instances)}")
        except ValueError:
            print("Invalid input. Please enter a number or 'q'")
        except Exception as e:
            print(f"Error: {e}")
            return None


def select_algorithm():
    """Let user select an algorithm"""
    print("\n" + "="*70)
    print("SELECT ALGORITHM")
    print("="*70)
    print("\nAvailable Algorithms:")
    print("  1. Random Search (baseline)")
    print("  2. Greedy Algorithm (baseline)")
    print("  3. Genetic Algorithm (main solution)")
    print("-" * 70)
    
    while True:
        try:
            choice = input("\nSelect algorithm (1-3) or 'b' to go back: ").strip()
            
            if choice.lower() == 'b':
                return None
            
            choice_num = int(choice)
            if 1 <= choice_num <= 3:
                algorithms = ['random', 'greedy', 'genetic']
                return algorithms[choice_num - 1]
            else:
                print("Please enter 1, 2, or 3")
        except ValueError:
            print("Invalid input. Please enter a number or 'b'")


def run_algorithm(algorithm: str, cargo_items: List[Cargo], container: Container):
    """Run the selected algorithm"""
    if algorithm == 'random':
        from algorithms.random_cargo import RandomSearch
        
        print("\n" + "="*70)
        print("RUNNING RANDOM SEARCH")
        print("="*70)
        
        iterations = input("\nEnter number of iterations (default: 1000): ").strip()
        iterations = int(iterations) if iterations else 1000
        
        print(f"\nSearching {iterations} random permutations...")
        search = RandomSearch(cargo_items, container, iterations)
        solution = search.run(verbose=True)
        
        return solution
    
    elif algorithm == 'greedy':
        from algorithms.greedy_cargo import run_greedy
        
        print("\n" + "="*70)
        print("RUNNING GREEDY ALGORITHM")
        print("="*70)
        
        print("\nApplying greedy heuristic (largest first)...")
        solution = run_greedy(cargo_items, container, verbose=True)
        
        return solution
    
    elif algorithm == 'genetic':
        from algorithms.genetic_cargo import GeneticAlgorithm
        
        print("\n" + "="*70)
        print("RUNNING GENETIC ALGORITHM")
        print("="*70)
        
        # Get parameters
        pop_size = input("\nPopulation size (default: 100): ").strip()
        pop_size = int(pop_size) if pop_size else 100
        
        generations = input("Generations (default: 500): ").strip()
        generations = int(generations) if generations else 500
        
        mutation_rate = input("Mutation rate (default: 0.15): ").strip()
        mutation_rate = float(mutation_rate) if mutation_rate else 0.15
        
        print(f"\nRunning GA with:")
        print(f"  Population: {pop_size}")
        print(f"  Generations: {generations}")
        print(f"  Mutation: {mutation_rate}")
        
        ga = GeneticAlgorithm(cargo_items, container, pop_size, generations, mutation_rate)
        solution = ga.run(verbose=True)
        
        return solution


def display_results(solution: Solution, instance_name: str, algorithm: str):
    """Display solution results"""
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)
    
    print(f"\nInstance: {instance_name}")
    print(f"Algorithm: {algorithm.upper()}")
    print(f"\nFitness: {solution.fitness:.2f}")
    print(f"Complete: {'Yes' if solution.complete else 'No'}")
    
    # Show cargo order
    print(f"\nCargo Order: {solution.order}")
    
    # Show placed positions
    placed_count = sum(1 for c in solution.cargo_items if c.placed)
    print(f"\nPlaced: {placed_count}/{len(solution.cargo_items)} items")
    
    if solution.complete:
        com_x, com_y = solution.get_center_of_mass()
        print(f"Center of Mass: ({com_x:.2f}, {com_y:.2f})")
        
        total_weight = sum(c.weight for c in solution.cargo_items if c.placed)
        print(f"Total Weight: {total_weight:.1f}kg / {solution.container.max_weight:.1f}kg")
    
    # Show violations
    if solution.violations:
        print(f"\nViolations:")
        for key, value in solution.violations.items():
            if 'penalty' not in key:
                print(f"  {key}: {value:.2f}")
    
    # Ask to visualize
    print("\n" + "-" * 70)
    show_viz = input("\nShow visualization? (y/n): ").strip().lower()
    
    if show_viz == 'y':
        try:
            from vis import CargoVisualizer
            import matplotlib.pyplot as plt
            
            visualizer = CargoVisualizer(solution)
            visualizer.draw(title=f"{instance_name} - {algorithm.upper()}")
            plt.show()
        except ImportError as e:
            print(f"Visualization error: {e}")
            print("Make sure matplotlib is installed: pip install matplotlib")
        except Exception as e:
            print(f"Error displaying visualization: {e}")


def main_menu():
    """Main program loop"""
    print_header()
    
    while True:
        # Step 1: Select instance
        instance_name = select_instance()
        if instance_name is None:
            print("\nExiting program. Goodbye!")
            break
        
        # Load instance
        try:
            from algorithms import load_json
            cargo_items, container = load_json.load_instance(instance_name)
        except Exception as e:
            print(f"\nError loading instance: {e}")
            continue
        
        # Step 2: Select algorithm
        algorithm = select_algorithm()
        if algorithm is None:
            continue  # Go back to instance selection
        
        # Step 3: Run algorithm
        try:
            solution = run_algorithm(algorithm, cargo_items, container)
            
            # Step 4: Display results
            display_results(solution, instance_name, algorithm)
            
        except Exception as e:
            print(f"\nError running algorithm: {e}")
            import traceback
            traceback.print_exc()
        
        # Continue or exit
        print("\n" + "="*70)
        continue_choice = input("\nSolve another instance? (y/n): ").strip().lower()
        if continue_choice != 'y':
            print("\nExiting program. Goodbye!")
            break
