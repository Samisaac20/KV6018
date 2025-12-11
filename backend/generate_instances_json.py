"""
Generate container_instances.json from container_instances.py
Run this once to create the JSON file that the main program will load
"""

import json

def generate_instances_json():
    """Generate JSON file from the reference instances"""
    
    # Define all instances matching container_instances.py
    instances_data = {
        "basic_instances": [
            {
                "name": "basic_01_three_identical",
                "container": {
                    "width": 10.0,
                    "depth": 10.0,
                    "max_weight": 100.0
                },
                "cylinders": [
                    {"id": 1, "diameter": 2.0, "weight": 10.0},
                    {"id": 2, "diameter": 2.0, "weight": 10.0},
                    {"id": 3, "diameter": 2.0, "weight": 10.0}
                ]
            },
            {
                "name": "basic_02_two_sizes",
                "container": {
                    "width": 12.0,
                    "depth": 10.0,
                    "max_weight": 150.0
                },
                "cylinders": [
                    {"id": 1, "diameter": 3.0, "weight": 20.0},
                    {"id": 2, "diameter": 3.0, "weight": 20.0},
                    {"id": 3, "diameter": 2.0, "weight": 15.0},
                    {"id": 4, "diameter": 2.0, "weight": 15.0}
                ]
            },
            {
                "name": "basic_03_varied_sizes",
                "container": {
                    "width": 15.0,
                    "depth": 12.0,
                    "max_weight": 200.0
                },
                "cylinders": [
                    {"id": 1, "diameter": 3.5, "weight": 25.0},
                    {"id": 2, "diameter": 3.0, "weight": 20.0},
                    {"id": 3, "diameter": 2.5, "weight": 18.0},
                    {"id": 4, "diameter": 2.5, "weight": 18.0},
                    {"id": 5, "diameter": 2.0, "weight": 15.0}
                ]
            }
        ],
        "challenging_instances": [
            {
                "name": "challenge_01_tight_packing",
                "container": {
                    "width": 15.0,
                    "depth": 15.0,
                    "max_weight": 300.0
                },
                "cylinders": [
                    {"id": 1, "diameter": 4.0, "weight": 35.0},
                    {"id": 2, "diameter": 3.5, "weight": 30.0},
                    {"id": 3, "diameter": 3.5, "weight": 30.0},
                    {"id": 4, "diameter": 3.0, "weight": 25.0},
                    {"id": 5, "diameter": 3.0, "weight": 25.0},
                    {"id": 6, "diameter": 2.5, "weight": 20.0},
                    {"id": 7, "diameter": 2.5, "weight": 20.0},
                    {"id": 8, "diameter": 2.0, "weight": 15.0}
                ]
            },
            {
                "name": "challenge_02_weight_balance",
                "container": {
                    "width": 18.0,
                    "depth": 14.0,
                    "max_weight": 400.0
                },
                "cylinders": [
                    {"id": 1, "diameter": 3.0, "weight": 80.0},
                    {"id": 2, "diameter": 3.0, "weight": 80.0},
                    {"id": 3, "diameter": 2.5, "weight": 10.0},
                    {"id": 4, "diameter": 2.5, "weight": 10.0},
                    {"id": 5, "diameter": 2.5, "weight": 10.0},
                    {"id": 6, "diameter": 2.5, "weight": 10.0},
                    {"id": 7, "diameter": 3.5, "weight": 60.0},
                    {"id": 8, "diameter": 3.5, "weight": 60.0}
                ]
            },
            {
                "name": "challenge_03_many_small",
                "container": {
                    "width": 20.0,
                    "depth": 15.0,
                    "max_weight": 350.0
                },
                "cylinders": [
                    {"id": i, "diameter": 2.0, "weight": 15.0}
                    for i in range(1, 13)
                ]
            },
            {
                "name": "challenge_04_mixed_constraints",
                "container": {
                    "width": 20.0,
                    "depth": 20.0,
                    "max_weight": 500.0
                },
                "cylinders": [
                    {"id": 1, "diameter": 5.0, "weight": 50.0},
                    {"id": 2, "diameter": 4.5, "weight": 45.0},
                    {"id": 3, "diameter": 4.0, "weight": 40.0},
                    {"id": 4, "diameter": 3.5, "weight": 35.0},
                    {"id": 5, "diameter": 3.5, "weight": 35.0},
                    {"id": 6, "diameter": 3.0, "weight": 30.0},
                    {"id": 7, "diameter": 3.0, "weight": 30.0},
                    {"id": 8, "diameter": 2.5, "weight": 25.0},
                    {"id": 9, "diameter": 2.5, "weight": 25.0},
                    {"id": 10, "diameter": 2.0, "weight": 20.0}
                ]
            }
        ]
    }
    
    # Write to JSON file
    filename = "container_instances.json"
    with open(filename, 'w') as f:
        json.dump(instances_data, f, indent=2)
    
    print(f"✓ Successfully created {filename}")
    print(f"\nFile contains:")
    print(f"  - {len(instances_data['basic_instances'])} basic instances")
    print(f"  - {len(instances_data['challenging_instances'])} challenging instances")
    print(f"\nTotal: {len(instances_data['basic_instances']) + len(instances_data['challenging_instances'])} instances")
    
    # Display summary
    print("\n" + "="*70)
    print("INSTANCE SUMMARY")
    print("="*70)
    
    print("\nBASIC INSTANCES:")
    for inst in instances_data['basic_instances']:
        n_cyls = len(inst['cylinders'])
        container = inst['container']
        print(f"  {inst['name']:<30} {n_cyls} cylinders, "
              f"{container['width']}m × {container['depth']}m")
    
    print("\nCHALLENGING INSTANCES:")
    for inst in instances_data['challenging_instances']:
        n_cyls = len(inst['cylinders'])
        container = inst['container']
        print(f"  {inst['name']:<30} {n_cyls} cylinders, "
              f"{container['width']}m × {container['depth']}m")
    
    print("\n" + "="*70)
    print(f"\nYou can now run the main program:")
    print(f"  python cargo_container_loading.py")
    print("="*70 + "\n")
    
    return filename

if __name__ == "__main__":
    print("\n" + "="*70)
    print("GENERATING container_instances.json")
    print("="*70 + "\n")
    
    generate_instances_json()