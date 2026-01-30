import os
import sys

# Configuration
# On Windows, we access network shares via UNC paths
NETWORK_PATH = r"\\192.168.2.16\public"

def get_indent(level):
    return "    " * level

def traverse_path(root_path):
    print(f"Scanning: {root_path}\n")
    
    if not os.path.exists(root_path):
        print(f"Error: The path '{root_path}' does not exist or is not accessible.")
        print("Make sure you can access this path in File Explorer first.")
        return

    # Calculate root depth to normalize indentation
    root_depth = len(root_path.rstrip(os.sep).split(os.sep))

    for root, dirs, files in os.walk(root_path):
        # Calculate current depth relative to the starting path
        path_parts = root.rstrip(os.sep).split(os.sep)
        depth = len(path_parts) - root_depth
        
        # Print current directory
        dir_name = path_parts[-1]
        print(f"{get_indent(depth)}[{dir_name}]")
        
        # Print files in this directory
        for f in files:
            print(f"{get_indent(depth + 1)}{f}")

if __name__ == "__main__":
    traverse_path(NETWORK_PATH)
