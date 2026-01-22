import os
import sys
from pypdf import PdfReader

BASE_DIR = 'Bluetooth_Knowledge_Base'

def validate_and_clean():
    print(f"Scanning '{BASE_DIR}' for corrupt PDFs...")
    
    corrupt_count = 0
    valid_count = 0
    
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.lower().endswith('.pdf'):
                path = os.path.join(root, file)
                
                try:
                    # 1. Basic size check
                    if os.path.getsize(path) == 0:
                        raise Exception("File is empty (0 bytes)")
                    
                    # 2. Structure check using pypdf
                    # Just creating the object parses the header/trailer/xref
                    PdfReader(path)
                    
                    valid_count += 1
                    # Optional: Print progress for every 100 valid files
                    if valid_count % 100 == 0:
                        print(f"Verified {valid_count} files...")
                        
                except Exception as e:
                    print(f"[CORRUPT] Deleting: {path} | Reason: {e}")
                    try:
                        os.remove(path)
                        corrupt_count += 1
                    except OSError as del_err:
                        print(f"Error deleting file: {del_err}")

    print("-" * 30)
    print(f"Scan Complete.")
    print(f"Valid Files:   {valid_count}")
    print(f"Corrupt Files: {corrupt_count} (Deleted)")
    print("-" * 30)
    
    if corrupt_count > 0:
        print("Recommendation: Please re-run 'optimized_split_pdf.py' to regenerate the deleted files.")
    else:
        print("All existing files are healthy. You can resume processing.")

if __name__ == "__main__":
    validate_and_clean()
