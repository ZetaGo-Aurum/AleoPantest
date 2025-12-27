import json
import os
import re
import sys

def validate_requirements(file_path):
    print(f"Validating {file_path}...")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for UTF-8 (open with encoding='utf-8' will raise error if invalid, 
    # but we can also check for non-ascii if needed)
    
    lines = content.splitlines()
    if not lines[0].startswith("# Aleopantest"):
        print("Error: Missing header in requirements.txt")
        return False
        
    # Check PEP 440 versioning (simple regex check for ==version)
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
            
        # Match library==version # comment
        match = re.match(r'^([a-zA-Z0-9\-_]+)==([0-9\.]+)\s*#.*$', line)
        if not match:
            print(f"Error at line {i}: Invalid format. Expected 'library==version # comment'")
            return False
            
    print("requirements.txt is valid.")
    return True

def validate_library_json(file_path):
    print(f"Validating {file_path}...")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found")
        return False
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        required_keys = ["name", "supported_version", "function", "usage_example", "compatibility"]
        
        if "_metadata" not in data:
            print("Error: Missing _metadata in library.json")
            return False
            
        if "libraries" not in data or not isinstance(data["libraries"], list):
            print("Error: Missing libraries list in library.json")
            return False
            
        for i, lib in enumerate(data["libraries"]):
            for key in required_keys:
                if key not in lib:
                    print(f"Error in library entry {i}: Missing key '{key}'")
                    return False
                    
        print("library.json is valid.")
        return True
    except json.JSONDecodeError as e:
        print(f"Error: library.json is not a valid JSON: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    req_valid = validate_requirements("requirements.txt")
    json_valid = validate_library_json("library.json")
    
    if req_valid and json_valid:
        print("\nAll files validated successfully!")
        sys.exit(0)
    else:
        print("\nValidation failed!")
        sys.exit(1)
