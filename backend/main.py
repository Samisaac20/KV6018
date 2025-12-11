# load json
# allow user to pick algorithm
# greedy/ GA ect
# placement algorithm
# run selected algorithm
# output results
def load_instances_from_json(filename: str) -> Dict:
    """
    Load problem instances from JSON file.
    
    Expected JSON format:
    {
        "basic_instances": [
            {
                "name": "instance_name",
                "container": {"width": 10.0, "depth": 10.0, "max_weight": 100.0},
                "cylinders": [
                    {"id": 1, "diameter": 2.0, "weight": 10.0},
                    ...
                ]
            },
            ...
        ],
        "challenging_instances": [...]
    }
    
    Args:
        filename: Path to JSON file
        
    Returns:
        Dictionary of instances or None if error
    """
    try:
        print(f"Loading instances from: {filename}")
        
        with open(filename, 'r') as f:
            data = json.load(f)
        
        instances = {}
        
        # Load basic instances
        if "basic_instances" in data:
            for inst_data in data["basic_instances"]:
                name = inst_data["name"]
                container = Container(
                    inst_data["container"]["width"],
                    inst_data["container"]["depth"],
                    inst_data["container"]["max_weight"]
                )
                cylinders = [
                    Cylinder(c["id"], c["diameter"], c["weight"])
                    for c in inst_data["cylinders"]
                ]
                instances[name] = {
                    'container': container,
                    'cylinders': cylinders,
                    'category': 'basic'
                }
        
        # Load challenging instances
        if "challenging_instances" in data:
            for inst_data in data["challenging_instances"]:
                name = inst_data["name"]
                container = Container(
                    inst_data["container"]["width"],
                    inst_data["container"]["depth"],
                    inst_data["container"]["max_weight"]
                )
                cylinders = [
                    Cylinder(c["id"], c["diameter"], c["weight"])
                    for c in inst_data["cylinders"]
                ]
                instances[name] = {
                    'container': container,
                    'cylinders': cylinders,
                    'category': 'challenging'
                }
        
        if not instances:
            print("Warning: No instances found in JSON file")
            return None
        
        print(f"✓ Successfully loaded {len(instances)} instances")
        return instances
    
    except FileNotFoundError:
        print(f"\nError: Could not find file '{filename}'")
        print("\nPlease ensure:")
        print(f"  1. The file '{filename}' exists in the current directory")
        print(f"  2. You have permission to read the file")
        print(f"\nCurrent directory: {os.getcwd() if 'os' in dir() else 'unknown'}")
        return None
    
    except json.JSONDecodeError as e:
        print(f"\nError: Invalid JSON in file '{filename}'")
        print(f"  {str(e)}")
        print("\nPlease check:")
        print(f"  1. The file is valid JSON format")
        print(f"  2. No trailing commas or syntax errors")
        return None
    
    except KeyError as e:
        print(f"\nError: Missing required field in JSON: {str(e)}")
        print("\nExpected structure:")
        print("  {")
        print('    "basic_instances": [')
        print('      {"name": "...", "container": {...}, "cylinders": [...]}')
        print('    ],')
        print('    "challenging_instances": [...]')
        print("  }")
        return None
    
    except Exception as e:
        print(f"\nUnexpected error loading instances: {str(e)}")
        return None