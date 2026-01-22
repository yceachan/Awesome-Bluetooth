import xml.etree.ElementTree as ET
import os
import re

# Configuration
XML_FILE = '【书签】蓝牙规格书-Core_v6.2.xml'
BASE_DIR = 'Bluetooth_Knowledge_Base'

def sanitize_name(name):
    """Sanitizes a string to be safe for directory names."""
    # Extract "Vol X" or "Part Y" prefix if present for sorting
    match = re.match(r'^(Vol \d+|Part [A-Z0-9]+)', name)
    prefix = match.group(1).replace(' ', '_') if match else ""
    
    # Clean the rest of the name
    clean_name = re.sub(r'[\\/*?:":<>|]', '', name) # Remove invalid chars
    clean_name = clean_name.replace(':', ' -') # Replace colons
    clean_name = " ".join(clean_name.split()) # Remove extra spaces
    
    if prefix and prefix not in clean_name.replace(' ', '_'):
         # If the simple sanitization messed up the clear prefix, ensure it's there? 
         # Actually, better strategy: Use the full name but sanitized.
         pass
         
    return clean_name

def parse_and_build(element, current_path, level=0):
    """
    Recursively parses XML elements and builds directory structure.
    level 0: Root (Core Spec)
    level 1: Volume (Create Dir)
    level 2: Part (Create Dir)
    level 3+: Sections (Add to README)
    """
    
    # Get current item details
    name = element.get('NAME', 'Unknown')
    page = element.get('PAGE', '0')
    
    # Prepare content for the current level's README/Index
    # Only meaningful for Parts (level 2) to list their sections (level 3+)
    
    children = element.findall('ITEM')
    
    if level == 1: # Volume Level
        dir_name = sanitize_name(name)
        new_path = os.path.join(current_path, dir_name)
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        
        # Create a Vol level README
        with open(os.path.join(new_path, 'README.md'), 'w', encoding='utf-8') as f:
            f.write(f"# {name}\n\nStart Page: {page}\n\n## Parts\n")
            
        for child in children:
            parse_and_build(child, new_path, level + 1)
            
    elif level == 2: # Part Level
        dir_name = sanitize_name(name)
        new_path = os.path.join(current_path, dir_name)
        if not os.path.exists(new_path):
            os.makedirs(new_path)
            
        # Create Part level README with detailed TOC
        with open(os.path.join(new_path, 'README.md'), 'w', encoding='utf-8') as f:
            f.write(f"# {name}\n\n**Start Page:** {page}\n\n## Table of Contents\n\n")
            write_toc(f, children, depth=0)
            
        # Update parent (Volume) README to link to this Part
        parent_readme = os.path.join(current_path, 'README.md')
        if os.path.exists(parent_readme):
            with open(parent_readme, 'a', encoding='utf-8') as f:
                f.write(f"- [{name}](./{dir_name}/README.md) (Page {page})\n")

    elif level == 0: # Root Level
        # Just iterate children (Volumes)
        if not os.path.exists(current_path):
            os.makedirs(current_path)
        for child in children:
            parse_and_build(child, current_path, level + 1)

def write_toc(file_handle, items, depth):
    """Recursive function to write TOC into Markdown."""
    for item in items:
        name = item.get('NAME', 'Unknown')
        page = item.get('PAGE', '0')
        indent = '  ' * depth
        file_handle.write(f"{indent}- {name} (Page {page})\n")
        
        children = item.findall('ITEM')
        if children:
            write_toc(file_handle, children, depth + 1)

def main():
    try:
        print(f"Parsing {XML_FILE}...")
        tree = ET.parse(XML_FILE)
        root = tree.getroot()
        
        # The first ITEM is usually the Book Title "Bluetooth Core Specification"
        # We want to start processing its children (Volumes)
        main_book = root.find('ITEM')
        if main_book:
            print("Found Root Item. Building Framework...")
            parse_and_build(main_book, BASE_DIR, level=0)
            print(f"Success! Knowledge Base framework created in '{BASE_DIR}/'")
        else:
            print("Error: Could not find root ITEM in XML.")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
