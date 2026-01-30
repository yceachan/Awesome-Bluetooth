import xml.etree.ElementTree as ET
import os
import re
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pypdf import PdfReader, PdfWriter
from tqdm import tqdm

# Configuration
XML_FILE = '【书签】蓝牙规格书-Core_v6.2.xml'
SOURCE_PDF = '蓝牙规格书-Core_v6.2.pdf'
BASE_DIR = 'Docs/Bt-core/chunk'

# 调整并发数：
# 多进程模式下，每个进程都会独立加载 PDF 索引，消耗较多内存。
# 建议设置为物理 CPU 核心数，或者根据内存情况调整。
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
    Executed in a separate process.
    """
    try:
        start_page = task['start_page']
        end_page = task['end_page']
        output_filename = os.path.join(task['path'], "source.pdf")
        
        # Double check existence
        if os.path.exists(output_filename):
            return f"Skipped (Exists): {task['name']}"

        # Ensure directory exists
        os.makedirs(task['path'], exist_ok=True)

        # Performance Timer
        t0 = time.time()

        # In Multiprocessing, we MUST open the file inside the process.
        # Passing PdfReader objects between processes is not pickle-able/efficient.
        # This uses more RAM but bypasses the GIL.
        reader = PdfReader(SOURCE_PDF)
        
        # Validation
        total_pages = len(reader.pages)
        if start_page >= total_pages:
            return f"Skipped (OOR): {task['name']}"
            
        writer = PdfWriter()
        
        # Add pages
        # Iterate carefully to avoid index errors
        page_count = 0
        for p in range(start_page, min(end_page, total_pages)):
            writer.add_page(reader.pages[p])
            page_count += 1
        
        # Write to file
        with open(output_filename, 'wb') as f:
            writer.write(f)
            
        duration = time.time() - t0
        return f"Completed: {task['name']} ({page_count} pages) in {duration:.2f}s"

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
        
        # 1. Quick pass to get total pages (lightweight)
        try:
            reader = PdfReader(SOURCE_PDF)
            total_pdf_pages = len(reader.pages)
            print(f"Source PDF loaded. Total pages: {total_pdf_pages}")
        except Exception as e:
            print(f"Error checking source PDF: {e}")
            return

        # 2. Prepare tasks
        tasks = []
        for i, item in enumerate(raw_structure):
            start_page = item['page']
            
            if i < len(raw_structure) - 1:
                end_page = raw_structure[i+1]['page']
            else:
                end_page = total_pdf_pages
            
            output_filename = os.path.join(item['path'], "source.pdf")
            
            # Pre-filter existing files to avoid spawning processes for nothing
            if os.path.exists(output_filename):
                continue 
                
            tasks.append({
                'name': item['name'],
                'start_page': start_page,
                'end_page': end_page,
                'path': item['path']
            })
            
        print(f"Found {len(tasks)} parts pending processing.")
        
        if not tasks:
            print("All tasks completed.")
            return

        print(f"Starting execution with {MAX_WORKERS} PROCESSES (High CPU Mode)...")
        print("Note: Memory usage may increase. Watch your system resources.")
        
        # Change to ProcessPoolExecutor for CPU-bound tasks
        with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_task = {executor.submit(process_single_part, task): task for task in tasks}
            
            with tqdm(total=len(tasks), unit="part") as pbar:
                for future in as_completed(future_to_task):
                    result = future.result()
                    if "Error" in result:
                        pbar.write(result)
                    # pbar.write(result) # Uncomment to see details log
                    pbar.update(1)
                    
        print("\nAll tasks completed.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
