import json
from pathlib import Path
from typing import List, Tuple
from main import Cargo, Container

def load_json_instance(instance_name: str) -> Tuple[List[Cargo], Container, str]:
    json_path = Path(__file__).parent.parent / "data" / "container_instances.json"

    if not json_path.exists():
        raise FileNotFoundError(f"Could not find {json_path}")

    with open(json_path, 'r') as f:
        data = json.load(f)

    instance_data = None

    for instance in data.get("basic_instances", []):
        if instance["name"] == instance_name:
            instance_data = instance
            break

    if instance_data is None:
        for instance in data.get("challenging_instances", []):
            if instance["name"] == instance_name:
                instance_data = instance
                break

    if instance_data is None:
        available = list_all_instances()
        raise ValueError(
            f"Instance '{instance_name}' not found.\n"
            f"Available instances: {available}"
        )

    # Parse container
    container_data = instance_data["container"]
    container = Container(
        width=container_data["width"],
        depth=container_data["depth"],
        max_weight=container_data["max_weight"]
    )

    # Parse cargo items (re-index IDs from 0)
    cargo_items = []
    for idx, cylinder_data in enumerate(instance_data["cylinders"]):
        cargo = Cargo(
            id=idx,  # Re-index from 0
            diameter=cylinder_data["diameter"],
            weight=cylinder_data["weight"]
        )
        cargo_items.append(cargo)
    
    return cargo_items, container, instance_name