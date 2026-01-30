import pdfplumber
import os

PART_D_PDF = "Docs/Bt-core/chunk/Vol 6 Low Energy Controller/Part D Message Sequence Charts/source.pdf"
DIR_OUT = "notebook/vol6_controller"

# Relative pages (Original - 3559)
# Adv: 3571-3574 -> 12-15
# Scan: 3585-3587 -> 26-28
# Init: 3598-3600 -> 39-41

RANGES = [
    range(12, 16), # Advertising
    range(26, 29), # Scanning
    range(39, 42)  # Initiating
]

def extract_msc_text():
    output_file = os.path.join(DIR_OUT, "msc_raw_text.md")
    print(f"Extracting MSC text to {output_file}...")
    
    if not os.path.exists(DIR_OUT):
        os.makedirs(DIR_OUT)

    with pdfplumber.open(PART_D_PDF) as pdf:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# MSC Raw Text Extraction\n\n")
            
            for r in RANGES:
                for p_num in r:
                    if p_num < len(pdf.pages):
                        page = pdf.pages[p_num]
                        text = page.extract_text()
                        f.write(f"### Page {p_num + 3559} (Original)\n\n{text}\n\n")
    
    print("Done.")

if __name__ == "__main__":
    extract_msc_text()
