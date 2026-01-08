from __future__ import annotations

import json
from pathlib import Path

from container_instances import (
    create_basic_instances,
    create_challenging_instances,
)


def _print_summary(instances, heading):
    """Print a short summary for a list of Instance objects."""
    print(f"\n{heading.upper()} INSTANCES:")
    for inst in instances:
        container = inst.container
        print(
            f"  {inst.name:<30} {len(inst.cylinders)} cylinders, "
            f"{container.width}m x {container.depth}m"
        )


def generate_instances_json():
    """Generate JSON file from the reference instances."""
    basic_instances = create_basic_instances()
    challenging_instances = create_challenging_instances()

    instances_data = {
        "basic_instances": [inst.to_dict() for inst in basic_instances],
        "challenging_instances": [inst.to_dict() for inst in challenging_instances],
    }

    output_path = Path(__file__).resolve().parent / "container_instances.json"
    with output_path.open("w", encoding="utf-8") as json_file:
        json.dump(instances_data, json_file, indent=2)

    print(f"Successfully created {output_path}")
    print("\nFile contains:")
    print(f"  - {len(basic_instances)} basic instances")
    print(f"  - {len(challenging_instances)} challenging instances")
    print(f"\nTotal: {len(basic_instances) + len(challenging_instances)} instances")

    print("\n" + "=" * 70)
    print("INSTANCE SUMMARY")
    print("=" * 70)

    _print_summary(basic_instances, "basic")
    _print_summary(challenging_instances, "challenging")

    print("\n" + "=" * 70)
    print("\nYou can now run the main program:")
    print("  python cargo_container_loading.py")
    print("=" * 70 + "\n")

    return output_path


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("GENERATING container_instances.json")
    print("=" * 70 + "\n")

    generate_instances_json()
