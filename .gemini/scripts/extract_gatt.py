import pdfplumber
import os

PART_G_PDF = "Bluetooth_Knowledge_Base/Vol 3 Host/Part G Generic Attribute Profile (GATT)/source.pdf"
# Updated output path to follow the raw paradigm
DIR_OUT = "notebook/vol3_host/raw/gatt_raw"

# Relative pages (Original - 1547)
RANGE_OVERVIEW = range(5, 18)  # 1552-1564
RANGE_HIERARCHY = range(18, 30) # 1565-1576
RANGE_PROCEDURE = range(30, 61) # 1577-1607

def extract_section(pdf, page_range, output_filename, title):
    print(f"Extracting {title} to {output_filename}...")
    full_text = []
    
    for p_num in page_range:
        if p_num < len(pdf.pages):
            page = pdf.pages[p_num]
            text = page.extract_text()
            if text:
                full_text.append(f"### Page {p_num + 1547} (Original)\n\n{text}\n")
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n\n")
        f.write("> 本文档提取自 Vol 3, Part G GATT Specification。\n\n")
        f.write("\n".join(full_text))
    print(f"Saved: {output_filename}")

def main():
    if not os.path.exists(DIR_OUT):
        os.makedirs(DIR_OUT)

    if not os.path.exists(PART_G_PDF):
        print(f"Error: Source PDF not found at {PART_G_PDF}")
        return

    with pdfplumber.open(PART_G_PDF) as pdf:
        extract_section(pdf, RANGE_OVERVIEW, 
                       os.path.join(DIR_OUT, "gatt_overview_raw.md"), 
                       "GATT Profile Overview (角色与基础)")
        
        extract_section(pdf, RANGE_HIERARCHY, 
                       os.path.join(DIR_OUT, "gatt_hierarchy_raw.md"), 
                       "GATT Hierarchy (服务与特征层级)")

        extract_section(pdf, RANGE_PROCEDURE, 
                       os.path.join(DIR_OUT, "gatt_procedures_raw.md"), 
                       "GATT Procedures (读/写/通知交互)")

if __name__ == "__main__":
    main()
