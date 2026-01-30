import pdfplumber
import os

PART_F_PDF = "Docs/Bt-core/chunk/Vol 3 Host/Part F Attribute Protocol (ATT)/source.pdf"
DIR_OUT = "notebook/vol3_host/raw/att_raw"

# Base Page: 1488

# Section 2 & 3.2: Overview & Concepts (Page 1492 - 1500)
RANGE_CONCEPTS = range(4, 13)

# Section 3.3 & 3.4: PDU Formats & Details (Page 1500 - 1541)
RANGE_PDUS = range(12, 54)

def extract_section(pdf, page_range, output_filename, title):
    print(f"Extracting {title} to {output_filename}...")
    full_text = []
    
    for p_num in page_range:
        if p_num < len(pdf.pages):
            page = pdf.pages[p_num]
            text = page.extract_text()
            full_text.append(f"### Page {p_num + 1488} (Original)\n\n{text}\n")
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n\n")
        f.write("> 本文档提取自 Vol 3, Part F Attribute Protocol (ATT)。\n\n")
        f.write("\n".join(full_text))
    print(f"Saved: {output_filename}")

def main():
    if not os.path.exists(DIR_OUT):
        os.makedirs(DIR_OUT)

    if not os.path.exists(PART_F_PDF):
        print(f"Error: Source PDF not found at {PART_F_PDF}")
        return

    with pdfplumber.open(PART_F_PDF) as pdf:
        extract_section(pdf, RANGE_CONCEPTS, 
                       os.path.join(DIR_OUT, "att_concepts_raw.md"), 
                       "ATT Concepts (属性类型, Handle, 权限)")
        
        extract_section(pdf, RANGE_PDUS, 
                       os.path.join(DIR_OUT, "att_pdus_raw.md"), 
                       "ATT PDUs (Opcode与包结构)")

if __name__ == "__main__":
    main()
