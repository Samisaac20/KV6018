"""
Load problem instances from JSON file.
"""

import json
from typing import List, Tuple
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))


def load_instance(instance_name: str):

    # Import here to avoid circular dependency
    from main import Cargo, Container
    
    with open('data/container_instances.json', 'r') as f:
        data = json.load(f)
    
    # Search in both basic and challenging instances
    all_instances = data.get('basic_instances', []) + data.get('challenging_instances', [])
    
    for instance in all_instances:
        if instance['name'] == instance_name:
            # Create container
            container_data = instance['container']
            container = Container(
                width=container_data['width'],
                depth=container_data['depth'],
                max_weight=container_data['max_weight']
            )
            
            # Create cargo items (re-index from 0)
            cargo_items = []
            for idx, cylinder in enumerate(instance['cylinders']):
                cargo = Cargo(
                    id=idx,  # Re-index from 0
                    diameter=cylinder['diameter'],
                    weight=cylinder['weight']
                )
                cargo_items.append(cargo)
            
            return cargo_items, container
    
    raise ValueError(f"Instance '{instance_name}' not found in data/container_instances.json")


def list_all_instances() -> List[str]:

    with open('data/container_instances.json', 'r') as f:
        data = json.load(f)
    
    names = []
    for instance in data.get('basic_instances', []):
        names.append(instance['name'])
    for instance in data.get('challenging_instances', []):
        names.append(instance['name'])
    
    return names


def print_instance_info(instance_name: str):

    cargo_items, container = load_instance(instance_name)
    
    print(f"\nInstance: {instance_name}")
    print(f"Container: {container.width}m × {container.depth}m, max weight: {container.max_weight}kg")
    print(f"Cargo items: {len(cargo_items)}")
    
    total_weight = sum(c.weight for c in cargo_items)
    print(f"Total cargo weight: {total_weight}kg")
    
    print(f"\nCargo details:")
    for cargo in cargo_items:
        print(f"  Cargo {cargo.id}: diameter={cargo.diameter}m, weight={cargo.weight}kg")


# Test if this file works when run directly
if __name__ == "__main__":
    print("Testing load_json.py...")
    
    # Test list_all_instances
    instances = list_all_instances()
    print(f"\nFound {len(instances)} instances:")
    for name in instances:
        print(f"  - {name}")
    
    # Test load_instance
    print("\nTesting load_instance on first instance...")
    cargo, container = load_instance(instances[0])
    print(f"Loaded {len(cargo)} cargo items")
    print(f"Container: {container.width} x {container.depth}")
    
    print("\n✅ All tests passed!")