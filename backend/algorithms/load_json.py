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