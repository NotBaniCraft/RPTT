import sys
import os

def get_registry_path(filename="RPTTRoot/registry.txt"):
    if hasattr(sys, '_MEIPASS'):
        # If running as a bundled exe, look for the file in the temp extracted folder
        return os.path.join(sys._MEIPASS, filename)
    else:
        # If running in dev mode, use the relative path
        return filename

def read_registry(filename="RPTTRoot/registry.txt"):
    registry = {}
    try:
        registry_path = get_registry_path(filename)
        with open(registry_path, "r") as file:
            for line in file:
                line = line.strip()  # Remove any extra spaces or newlines
                if line and "=" in line:  # Only process lines that contain "="
                    key, value = line.split("=")
                    registry[key.strip()] = value.strip()  # Store the key and value
    except FileNotFoundError:
        os.makedirs(os.path.dirname(registry_path), exist_ok=True)
        with open(registry_path, "w") as file:
            file.write("TempKey=TempVal\n")  # safe dummy key 💀
        return {"TempKey": "TempVal"}
    return registry

def write_registry(registry, filename="RPTTRoot/registry.txt"):
    registry_path = get_registry_path(filename)
    with open(registry_path, "w") as file:
        for key, value in registry.items():
            file.write(f"{key}={value}\n")

def set_registry(key, value, filename="RPTTRoot/registry.txt"):
    # read existing registry
    registry = read_registry(filename)
    
    # update or add the key-value pair
    registry[key] = value
    
    # write updated registry back to file
    write_registry(registry, filename)

def get_registry(key, filename="RPTTRoot/registry.txt"):
    registry = read_registry(filename)
    
    if key in registry:
        return registry[key]
    else:
        return None
    
def delete_registry(key, filename="RPTTRoot/registry.txt"):
    registry = read_registry(filename)
    
    if key in registry:
        del registry[key]  # Delete the key from the dictionary
        write_registry(registry, filename)  # Write the updated registry back to the file
        print(f"✔️ Key '{key}' deleted from the registry.")
    else:
        print(f"❌ Error: '{key}' not found in registry!")
