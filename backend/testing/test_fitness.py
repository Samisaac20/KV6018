# test_fitness.py
"""Test fitness calculation"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from main import Cargo, Container, Solution
from fitness import calculate_fitness, update_solution_fitness


def test_perfect_solution():
    """Test a perfect solution: all placed, weight OK, COM in safe zone"""
    print("Test 1: Perfect Solution")
    
    # Create cargo centered in container
    cargo_items = [
        Cargo(id=0, diameter=2.0, weight=10.0, x=5.0, y=5.0, placed=True),
        Cargo(id=1, diameter=2.0, weight=10.0, x=7.0, y=5.0, placed=True),
    ]
    
    container = Container(width=10.0, depth=10.0, max_weight=100.0)
    
    solution = Solution(
        order=[0, 1],
        cargo_items=cargo_items,
        complete=True,
        fitness=0.0,
        violations={},
        container=container
    )
    
    fitness, violations = calculate_fitness(solution)
    
    print(f"  Fitness: {fitness}")
    print(f"  Violations: {violations}")
    print(f"  COM: {solution.get_center_of_mass()}")
    assert fitness == 0.0, "Perfect solution should have fitness 0.0"
    print("  PASS\n")


def test_unplaced_cargo():
    """Test incomplete solution"""
    print("Test 2: Unplaced Cargo")
    
    cargo_items = [
        Cargo(id=0, diameter=2.0, weight=10.0, x=5.0, y=5.0, placed=True),
        Cargo(id=1, diameter=2.0, weight=10.0, placed=False),  # Not placed
    ]
    
    container = Container(width=10.0, depth=10.0, max_weight=100.0)
    
    solution = Solution(
        order=[0, 1],
        cargo_items=cargo_items,
        complete=False,
        fitness=0.0,
        violations={},
        container=container
    )
    
    fitness, violations = calculate_fitness(solution)
    
    print(f"  Fitness: {fitness}")
    print(f"  Violations: {violations}")
    assert fitness == 1000.0, "Should have 1000.0 penalty for 1 unplaced"
    assert 'unplaced' in violations
    print("  PASS\n")


def test_weight_exceeded():
    """Test weight limit violation"""
    print("Test 3: Weight Exceeded")
    
    cargo_items = [
        Cargo(id=0, diameter=2.0, weight=60.0, x=5.0, y=5.0, placed=True),
        Cargo(id=1, diameter=2.0, weight=60.0, x=7.0, y=5.0, placed=True),
    ]
    
    container = Container(width=10.0, depth=10.0, max_weight=100.0)
    
    solution = Solution(
        order=[0, 1],
        cargo_items=cargo_items,
        complete=True,
        fitness=0.0,
        violations={},
        container=container
    )
    
    fitness, violations = calculate_fitness(solution)
    
    print(f"  Fitness: {fitness}")
    print(f"  Violations: {violations}")
    assert fitness > 0, "Should have penalty for weight excess"
    assert 'weight_excess' in violations
    print("  PASS\n")


def test_com_violation():
    """Test center of mass outside safe zone"""
    print("Test 4: COM Outside Safe Zone")
    
    # Place all cargo at corner (0,0) - COM will be outside safe zone
    cargo_items = [
        Cargo(id=0, diameter=2.0, weight=10.0, x=1.0, y=1.0, placed=True),
        Cargo(id=1, diameter=2.0, weight=10.0, x=3.0, y=1.0, placed=True),
    ]
    
    container = Container(width=10.0, depth=10.0, max_weight=100.0)
    
    solution = Solution(
        order=[0, 1],
        cargo_items=cargo_items,
        complete=True,
        fitness=0.0,
        violations={},
        container=container
    )
    
    fitness, violations = calculate_fitness(solution)
    
    print(f"  Fitness: {fitness}")
    print(f"  Violations: {violations}")
    print(f"  COM: {solution.get_center_of_mass()}")
    print(f"  Safe zone: X:[2.0, 8.0] Y:[2.0, 8.0]")
    assert fitness > 0, "Should have penalty for COM violation"
    assert 'com_violation' in violations
    print("  PASS\n")


if __name__ == "__main__":
    test_perfect_solution()
    test_unplaced_cargo()
    test_weight_exceeded()
    test_com_violation()
    print("All tests passed!")