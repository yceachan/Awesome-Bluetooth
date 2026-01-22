import xml.etree.ElementTree as ET
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pypdf import PdfReader, PdfWriter
from tqdm import tqdm

# Configuration
XML_FILE = '【书签】蓝牙规格书-Core_v6.2.xml'
SOURCE_PDF = '蓝牙规格书-Core_v6.2.pdf'
BASE_DIR = 'Bluetooth_Knowledge_Base'
MAX_WORKERS = 12

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

def process_single_part(task):
    """
    Worker function to process a single split task.
    task: dict containing 'name', 'start_page', 'end_page', 'path'
    """
    try:
        start_page = task['start_page']
        end_page = task['end_page']
        output_filename = os.path.join(task['path'], "source.pdf")
        
        # Double check existence (in case of race conditions or restart)
        if os.path.exists(output_filename):
            return f"Skipped (Exists): {task['name']}"

        # Ensure directory exists
        os.makedirs(task['path'], exist_ok=True)

        # Open a fresh reader for each thread to avoid race conditions/locks
        reader = PdfReader(SOURCE_PDF)
        total_pages = len(reader.pages)
        
        writer = PdfWriter()
        
        # Add pages
        for p in range(start_page, end_page):
            if p < total_pages:
                writer.add_page(reader.pages[p])
        
        # Write to file
        with open(output_filename, 'wb') as f:
            writer.write(f)
            
        return f"Completed: {task['name']} ({end_page - start_page} pages)"

    except Exception as e:
        return f"Error processing {task['name']}: {str(e)}"

def main():
    print(f"Parsing structure from {XML_FILE}...")
    try:
        tree = ET.parse(XML_FILE)
        root = tree.getroot()
        main_book = root.find('ITEM')
        
        if not main_book:
            print("Error: Invalid XML Structure (Root ITEM not found).")
            return

        raw_structure = get_structure_with_pages(main_book)
        raw_structure.sort(key=lambda x: x['page'])
        
        # Calculate ranges and prepare tasks
        tasks = []
        
        # Get total pages once to calculate limits
        try:
            temp_reader = PdfReader(SOURCE_PDF)
            total_pdf_pages = len(temp_reader.pages)
        except Exception as e:
            print(f"Error reading source PDF: {e}")
            return

        for i, item in enumerate(raw_structure):
            start_page = item['page']
            
            if i < len(raw_structure) - 1:
                end_page = raw_structure[i+1]['page']
            else:
                end_page = total_pdf_pages
            
            # Validation
            if start_page >= total_pdf_pages:
                continue
            if end_page <= start_page:
                continue
                
            output_filename = os.path.join(item['path'], "source.pdf")
            if os.path.exists(output_filename):
                continue # Skip already processed
                
            tasks.append({
                'name': item['name'],
                'start_page': start_page,
                'end_page': end_page,
                'path': item['path']
            })
            
        print(f"Found {len(tasks)} parts to process.")
        
        if not tasks:
            print("All parts are already processed.")
            return

        print(f"Starting execution with {MAX_WORKERS} threads...")
        
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # Submit all tasks
            future_to_task = {executor.submit(process_single_part, task): task for task in tasks}
            
            # Use tqdm for progress bar
            with tqdm(total=len(tasks), unit="part") as pbar:
                for future in as_completed(future_to_task):
                    result = future.result()
                    # Optional: Print result if it's an error
                    if "Error" in result:
                        pbar.write(result)
                    pbar.update(1)
                    
        print("\nAll tasks completed.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
