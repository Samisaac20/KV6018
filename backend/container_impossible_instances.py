"""
KV6018 Cargo Container Loading - IMPOSSIBLE INSTANCES
These instances CANNOT be solved due to constraint violations
Use these to test algorithm robustness and understand constraint satisfaction
"""

import json
import math
from typing import List, Dict

class Cylinder:
    """Represents a cylindrical container"""
    def __init__(self, id: int, diameter: float, weight: float):
        self.id = id
        self.diameter = diameter
        self.weight = weight
        self.radius = diameter / 2.0
    
    def to_dict(self):
        return {
            "id": self.id,
            "diameter": self.diameter,
            "weight": self.weight
        }

class Container:
    """Represents the cargo container"""
    def __init__(self, width: float, depth: float, max_weight: float):
        self.width = width
        self.depth = depth
        self.max_weight = max_weight
    
    def to_dict(self):
        return {
            "width": self.width,
            "depth": self.depth,
            "max_weight": self.max_weight
        }

class Placement:
    """Represents a cylinder placement with position"""
    def __init__(self, cylinder_id: int, x: float, y: float):
        self.cylinder_id = cylinder_id
        self.x = x
        self.y = y
    
    def to_dict(self):
        return {
            "cylinder_id": self.cylinder_id,
            "x": self.x,
            "y": self.y
        }

class Solution:
    """A verified solution to an instance"""
    def __init__(self, placements: List[Placement], is_valid: bool, 
                 fitness: float, violations: Dict):
        self.placements = placements
        self.is_valid = is_valid
        self.fitness = fitness
        self.violations = violations
    
    def to_dict(self):
        return {
            "placements": [p.to_dict() for p in self.placements],
            "is_valid": self.is_valid,
            "fitness": self.fitness,
            "violations": self.violations
        }

class Instance:
    """A complete problem instance with best attempt solution"""
    def __init__(self, name: str, container: Container, 
                 cylinders: List[Cylinder], solution: Solution = None):
        self.name = name
        self.container = container
        self.cylinders = cylinders
        self.solution = solution
    
    def to_dict(self):
        result = {
            "name": self.name,
            "container": self.container.to_dict(),
            "cylinders": [c.to_dict() for c in self.cylinders]
        }
        if self.solution:
            result["best_attempt_solution"] = self.solution.to_dict()
        return result

# ============================================================================
# SOLUTION VERIFICATION
# ============================================================================

def verify_solution(container: Container, cylinders: List[Cylinder], 
                    placements: List[Placement]) -> Solution:
    """Verify if a solution satisfies all constraints"""
    
    violations = {
        "boundary_violations": [],
        "overlap_violations": [],
        "weight_limit_violation": False,
        "weight_distribution_violation": False
    }
    
    # Create cylinder lookup
    cyl_dict = {c.id: c for c in cylinders}
    
    # Check boundary constraints
    for p in placements:
        cyl = cyl_dict[p.cylinder_id]
        if p.x - cyl.radius < 0 or p.x + cyl.radius > container.width:
            violations["boundary_violations"].append(p.cylinder_id)
        if p.y - cyl.radius < 0 or p.y + cyl.radius > container.depth:
            violations["boundary_violations"].append(p.cylinder_id)
    
    # Check overlaps
    for i, p1 in enumerate(placements):
        for p2 in placements[i+1:]:
            cyl1 = cyl_dict[p1.cylinder_id]
            cyl2 = cyl_dict[p2.cylinder_id]
            dist = math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
            min_dist = cyl1.radius + cyl2.radius
            if dist < min_dist - 0.001:  # Small tolerance
                violations["overlap_violations"].append(
                    (p1.cylinder_id, p2.cylinder_id)
                )
    
    # Check total weight
    total_weight = sum(cyl_dict[p.cylinder_id].weight for p in placements)
    if total_weight > container.max_weight:
        violations["weight_limit_violation"] = True
    
    # Check center of mass (must be within central 60%)
    total_mass = 0
    com_x = 0
    com_y = 0
    for p in placements:
        cyl = cyl_dict[p.cylinder_id]
        com_x += p.x * cyl.weight
        com_y += p.y * cyl.weight
        total_mass += cyl.weight
    
    com_x /= total_mass
    com_y /= total_mass
    
    # Central 60% boundaries (20% margin on each side)
    x_min = container.width * 0.2
    x_max = container.width * 0.8
    y_min = container.depth * 0.2
    y_max = container.depth * 0.8
    
    if not (x_min <= com_x <= x_max and y_min <= com_y <= y_max):
        violations["weight_distribution_violation"] = True
    
    # Calculate fitness (sum of all violations)
    fitness = (
        len(violations["boundary_violations"]) +
        len(violations["overlap_violations"]) +
        (10 if violations["weight_limit_violation"] else 0) +
        (10 if violations["weight_distribution_violation"] else 0)
    )
    
    is_valid = fitness == 0
    
    return Solution(placements, is_valid, fitness, violations)

# ============================================================================
# IMPOSSIBLE INSTANCES (Cannot be solved)
# ============================================================================

def create_impossible_instances():
    """Instances that cannot achieve fitness of 0 due to constraints"""
    instances = []
    
    # Instance 1: Total weight exceeds container limit
    container1 = Container(15.0, 15.0, 150.0)  # Max weight: 150kg
    cylinders1 = [
        Cylinder(1, 3.0, 60.0),
        Cylinder(2, 3.0, 60.0),
        Cylinder(3, 2.5, 50.0),  # Total: 170kg > 150kg limit
    ]
    # Best attempt placement (still violates weight)
    placements1 = [
        Placement(1, 5.0, 5.0),
        Placement(2, 10.0, 5.0),
        Placement(3, 7.5, 10.0)
    ]
    solution1 = verify_solution(container1, cylinders1, placements1)
    inst1 = Instance("impossible_01_weight_limit", container1, cylinders1, solution1)
    instances.append(inst1)
    
    # Instance 2: Geometric impossibility - cylinders too large
    container2 = Container(10.0, 10.0, 500.0)
    cylinders2 = [
        Cylinder(1, 6.0, 30.0),  # Diameter 6m
        Cylinder(2, 6.0, 30.0),  # Diameter 6m
        Cylinder(3, 6.0, 30.0),  # Three 6m cylinders can't fit in 10m×10m
    ]
    # Best attempt - overlaps inevitable
    placements2 = [
        Placement(1, 5.0, 3.5),
        Placement(2, 5.0, 6.5),
        Placement(3, 5.0, 9.5)
    ]
    solution2 = verify_solution(container2, cylinders2, placements2)
    inst2 = Instance("impossible_02_geometric_constraint", container2, cylinders2, solution2)
    instances.append(inst2)
    
    # Instance 3: Weight distribution impossible
    container3 = Container(20.0, 10.0, 500.0)
    cylinders3 = [
        Cylinder(1, 3.0, 200.0),  # Very heavy
        Cylinder(2, 2.0, 5.0),    # Very light
        Cylinder(3, 2.0, 5.0),    # Very light
        Cylinder(4, 2.0, 5.0),    # Very light
        # Heavy cylinder pulls COM too far, can't balance with light ones
    ]
    # Best attempt - COM will be outside central 60%
    placements3 = [
        Placement(1, 3.0, 5.0),   # Heavy on left
        Placement(2, 15.0, 3.0),  # Light on right
        Placement(3, 15.0, 5.0),  # Light on right
        Placement(4, 15.0, 7.0)   # Light on right
    ]
    solution3 = verify_solution(container3, cylinders3, placements3)
    inst3 = Instance("impossible_03_weight_distribution", container3, cylinders3, solution3)
    instances.append(inst3)
    
    # Instance 4: Combined impossibility - tight space + weight issues
    container4 = Container(12.0, 12.0, 200.0)
    cylinders4 = [
        Cylinder(1, 5.0, 70.0),
        Cylinder(2, 5.0, 70.0),
        Cylinder(3, 4.0, 50.0),  # Total weight: 190kg (OK)
        Cylinder(4, 4.0, 10.0),  # But geometric packing impossible
    ]
    # Best attempt - some overlap or boundary violation inevitable
    placements4 = [
        Placement(1, 3.5, 6.0),
        Placement(2, 8.5, 6.0),
        Placement(3, 6.0, 3.0),
        Placement(4, 6.0, 9.5)
    ]
    solution4 = verify_solution(container4, cylinders4, placements4)
    inst4 = Instance("impossible_04_combined_constraints", container4, cylinders4, solution4)
    instances.append(inst4)
    
    # Instance 5: Area constraint - total circle area exceeds container area
    container5 = Container(10.0, 8.0, 300.0)  # Area: 80 m²
    cylinders5 = [
        Cylinder(1, 4.0, 25.0),  # Area: π×4 ≈ 12.57 m²
        Cylinder(2, 4.0, 25.0),  # Area: π×4 ≈ 12.57 m²
        Cylinder(3, 4.0, 25.0),  # Area: π×4 ≈ 12.57 m²
        Cylinder(4, 3.5, 20.0),  # Area: π×3.06 ≈ 9.62 m²
        Cylinder(5, 3.5, 20.0),  # Area: π×3.06 ≈ 9.62 m²
        Cylinder(6, 3.0, 15.0),  # Area: π×2.25 ≈ 7.07 m²
        # Total circle area ≈ 63.6 m², but packing efficiency means needs more space
    ]
    placements5 = [
        Placement(1, 2.5, 2.5),
        Placement(2, 7.5, 2.5),
        Placement(3, 2.5, 6.0),
        Placement(4, 7.0, 6.0),
        Placement(5, 5.0, 4.0),
        Placement(6, 5.0, 7.0)
    ]
    solution5 = verify_solution(container5, cylinders5, placements5)
    inst5 = Instance("impossible_05_packing_density", container5, cylinders5, solution5)
    instances.append(inst5)
    
    return instances

# ============================================================================
# GENERATE IMPOSSIBLE INSTANCES
# ============================================================================

def generate_impossible_instances():
    """Generate and save all impossible (unsolvable) instances"""
    instances = create_impossible_instances()
    
    # Print summary
    print("=" * 70)
    print("KV6018 IMPOSSIBLE INSTANCES - CANNOT BE SOLVED")
    print("=" * 70)
    print("\nThese instances demonstrate constraint satisfaction vs optimization.")
    print("Use them to test algorithm robustness and fitness function design.\n")
    print("-" * 70)
    
    for inst in instances:
        print(f"\n{inst.name}:")
        print(f"  Container: {inst.container.width}m × {inst.container.depth}m, "
              f"max weight: {inst.container.max_weight}kg")
        print(f"  Cylinders: {len(inst.cylinders)}")
        total_weight = sum(c.weight for c in inst.cylinders)
        print(f"  Total weight: {total_weight}kg")
        
        if inst.solution:
            print(f"  Best attempt fitness: {inst.solution.fitness} (> 0, impossible to solve)")
            print(f"  Violations:")
            if inst.solution.violations["weight_limit_violation"]:
                print(f"    ✗ Weight limit exceeded ({total_weight}kg > {inst.container.max_weight}kg)")
            if inst.solution.violations["weight_distribution_violation"]:
                print(f"    ✗ Weight distribution constraint violated (COM outside central 60%)")
            if inst.solution.violations["boundary_violations"]:
                print(f"    ✗ Boundary violations: {len(inst.solution.violations['boundary_violations'])} cylinders")
            if inst.solution.violations["overlap_violations"]:
                print(f"    ✗ Overlaps: {len(inst.solution.violations['overlap_violations'])} pairs")
    
    print("\n" + "=" * 70)
    print("\nJSON OUTPUT:")
    print("=" * 70)
    
    # Output as JSON
    output = {
        "impossible_instances": [inst.to_dict() for inst in instances]
    }
    
    print(json.dumps(output, indent=2))
    
    # Save to file
    with open("impossible_instances.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\n✓ Saved to impossible_instances.json")
    
    return output

if __name__ == "__main__":
    generate_impossible_instances()