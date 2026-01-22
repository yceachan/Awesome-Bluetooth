import xml.etree.ElementTree as ET
import os
import re
import sys
from pypdf import PdfReader, PdfWriter

# Configuration
XML_FILE = '【书签】蓝牙规格书-Core_v6.2.xml'
SOURCE_PDF = '蓝牙规格书-Core_v6.2.pdf'
BASE_DIR = 'Bluetooth_Knowledge_Base'
BATCH_LIMIT = 5  # Process only 5 parts per run to avoid timeout

def sanitize_name(name):
    """Sanitizes a string to be safe for directory names."""
    clean_name = re.sub(r'[\\/*?:":<>|]', '', name)
    clean_name = clean_name.replace(':', ' -')
    clean_name = " ".join(clean_name.split())
    return clean_name

def get_structure_with_pages(element):
    """
    Parses XML to get a flat list of Parts with their page numbers and output paths.
    """
    structure = []
    
    # Process Volumes (Level 1)
    for vol in element.findall('ITEM'):
        vol_name = vol.get('NAME', 'Unknown')
        vol_dir = sanitize_name(vol_name)
        
        # Process Parts (Level 2)
        parts = vol.findall('ITEM')
        if not parts:
            continue
            
        for part in parts:
            part_name = part.get('NAME', 'Unknown')
            part_page = int(part.get('PAGE', '0'))
            part_dir = sanitize_name(part_name)
            
            output_path = os.path.join(BASE_DIR, vol_dir, part_dir)
            
            structure.append({
                'name': f"{vol_name} - {part_name}",
                'page': part_page,
                'path': output_path
            })
            
    return structure

def split_pdf(structure):
    """
    Splits the source PDF based on the structure page ranges.
    """
    try:
        reader = PdfReader(SOURCE_PDF)
        total_pages = len(reader.pages)
        print(f"Opened Source PDF. Total Pages: {total_pages}")
        
        processed_count = 0
        
        for i, item in enumerate(structure):
            if processed_count >= BATCH_LIMIT:
                print(f"Batch limit of {BATCH_LIMIT} reached. Exiting for now.")
                break

            start_page = item['page']
            
            # Determine end page
            if i < len(structure) - 1:
                end_page = structure[i+1]['page']
            else:
                end_page = total_pages
                
            # Validation
            if start_page >= total_pages:
                continue
            
            if end_page <= start_page:
                continue

            # Ensure directory exists
            if not os.path.exists(item['path']):
                os.makedirs(item['path'])
                
            output_filename = os.path.join(item['path'], "source.pdf")
            
            # Check if already exists
            if os.path.exists(output_filename):
                # print(f"Skipping {item['name']}: Already exists.")
                continue

            print(f"Extracting: {item['name']} (Pages {start_page}-{end_page})...")
            sys.stdout.flush() # Force print
            
            writer = PdfWriter()
            
            try:
                for p in range(start_page, end_page):
                    if p < total_pages:
                        writer.add_page(reader.pages[p])
                
                with open(output_filename, 'wb') as f:
                    writer.write(f)
                
                print(f"Done: {output_filename}")
                processed_count += 1
                
            except Exception as e:
                print(f"Error extracting {item['name']}: {e}")

    except Exception as e:
        print(f"Critical Error: {e}")

def main():
    print(f"Parsing structure from {XML_FILE}...")
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    main_book = root.find('ITEM') 
    
    if main_book:
        structure = get_structure_with_pages(main_book)
        structure.sort(key=lambda x: x['page'])
        split_pdf(structure)
    else:
        print("Invalid XML Structure.")

if __name__ == "__main__":
    main()