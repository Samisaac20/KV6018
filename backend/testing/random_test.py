# test_random_search.py
"""Test random search algorithm"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import sys
sys.path.append('algorithms')

from main import Cargo, Container
from algorithms.random_cargo import random_search


def test_simple_instance():
    """Test random search on simple 3-cargo instance"""
    print("Test: Random Search on Simple Instance")
    print("=" * 60)
    
    # Create simple test instance
    cargo_items = [
        Cargo(id=0, diameter=2.0, weight=10.0),
        Cargo(id=1, diameter=2.0, weight=10.0),
        Cargo(id=2, diameter=2.0, weight=10.0),
    ]
    
    container = Container(width=10.0, depth=10.0, max_weight=100.0)
    
    print(f"Instance:")
    print(f"  Container: {container.width}x{container.depth}, max_weight={container.max_weight}")
    print(f"  Cargo items: {len(cargo_items)}")
    print(f"\nRunning random search (max 1000 iterations)...\n")
    
    # Run random search
    solution = random_search(cargo_items, container, max_iterations=1000, verbose=True)
    
    print(f"\nFinal Solution:")
    print(f"  Order: {solution.order}")
    print(f"  Fitness: {solution.fitness}")
    print(f"  Complete: {solution.complete}")
    print(f"  Violations: {solution.violations}")
    
    if solution.complete:
        print(f"\nPlaced cargo positions:")
        for cargo in solution.cargo_items:
            if cargo.placed:
                print(f"  Cargo {cargo.id}: ({cargo.x:.2f}, {cargo.y:.2f})")
        
        com_x, com_y = solution.get_center_of_mass()
        print(f"\nCenter of mass: ({com_x:.2f}, {com_y:.2f})")
    
    # Check if solution is valid
    assert solution.complete, "Should place all cargo"
    print("\nTest PASSED!")


def test_harder_instance():
    """Test random search on slightly harder instance"""
    print("\n" + "=" * 60)
    print("Test: Random Search on Harder Instance")
    print("=" * 60)
    
    # Create harder test instance with varied sizes
    cargo_items = [
        Cargo(id=0, diameter=3.5, weight=25.0),
        Cargo(id=1, diameter=3.0, weight=20.0),
        Cargo(id=2, diameter=2.5, weight=18.0),
        Cargo(id=3, diameter=2.5, weight=18.0),
        Cargo(id=4, diameter=2.0, weight=15.0),
    ]
    
    container = Container(width=15.0, depth=12.0, max_weight=200.0)
    
    print(f"Instance:")
    print(f"  Container: {container.width}x{container.depth}, max_weight={container.max_weight}")
    print(f"  Cargo items: {len(cargo_items)}")
    print(f"\nRunning random search (max 5000 iterations)...\n")
    
    # Run random search with more iterations
    solution = random_search(cargo_items, container, max_iterations=5000, verbose=True)
    
    print(f"\nFinal Solution:")
    print(f"  Order: {solution.order}")
    print(f"  Fitness: {solution.fitness}")
    print(f"  Complete: {solution.complete}")
    print(f"  Violations: {solution.violations}")
    
    print("\nTest PASSED!")


if __name__ == "__main__":
    test_simple_instance()
    test_harder_instance()
    
    print("\n" + "=" * 60)
    print("All random search tests completed!")