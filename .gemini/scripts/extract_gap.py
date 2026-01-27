import pdfplumber
import os

PART_C_PDF = "Bluetooth_Knowledge_Base/Vol 3 Host/Part C Generic Access Profile/source.pdf"
DIR_OUT = "notebook/vol3_host/gap_raw"

# Base Page: 1315
# Section 9: Operational Modes (LE) - Page 1389 to 1422
RANGE_MODES = range(74, 108) 

# Section 10: Security Aspects (LE) - Page 1423 to 1444
RANGE_SECURITY = range(108, 130)

# Section 11: Advertising Data Format - Page 1445 to 1446
RANGE_ADV_DATA = range(130, 132)

def extract_section(pdf, page_range, output_filename, title):
    print(f"Extracting {title} to {output_filename}...")
    full_text = []
    
    for p_num in page_range:
        if p_num < len(pdf.pages):
            page = pdf.pages[p_num]
            text = page.extract_text()
            # Add header with original page number for reference
            full_text.append(f"### Page {p_num + 1315} (Original)\n\n{text}\n")
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n\n")
        f.write("> 本文档提取自 Vol 3, Part C Generic Access Profile (GAP)。\n\n")
        f.write("\n".join(full_text))
    print(f"Saved: {output_filename}")

def main():
    if not os.path.exists(DIR_OUT):
        os.makedirs(DIR_OUT)

    if not os.path.exists(PART_C_PDF):
        print(f"Error: Source PDF not found at {PART_C_PDF}")
        return

    with pdfplumber.open(PART_C_PDF) as pdf:
        extract_section(pdf, RANGE_MODES, 
                       os.path.join(DIR_OUT, "gap_modes_procedures_raw.md"), 
                       "GAP Modes & Procedures (LE 发现与连接模式)")
        
        extract_section(pdf, RANGE_SECURITY, 
                       os.path.join(DIR_OUT, "gap_security_raw.md"), 
                       "GAP Security Aspects (LE 安全模式)")

        extract_section(pdf, RANGE_ADV_DATA, 
                       os.path.join(DIR_OUT, "gap_advertising_data_raw.md"), 
                       "GAP Advertising Data Format (广播数据结构)")

if __name__ == "__main__":
    main()
