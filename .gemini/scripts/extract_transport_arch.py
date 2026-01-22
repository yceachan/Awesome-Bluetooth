import pdfplumber
import os

PART_A_PDF = "Bluetooth_Knowledge_Base/Vol 1 Architecture, Change History, and Conventions/Part A Architecture/source.pdf"
OUTPUT_FILE = "notebook/vol1_architecture/transport_hierarchy.md"

# Range in Part A PDF (based on original pages 253-267)
# 253 - 222 = 31 (0-indexed roughly 30)
PAGES_TO_EXTRACT = range(30, 45) 

def extract():
    if not os.path.exists(os.path.dirname(OUTPUT_FILE)):
        os.makedirs(os.path.dirname(OUTPUT_FILE))

    print(f"Extracting transport architecture from {PART_A_PDF}...")
    
    with pdfplumber.open(PART_A_PDF) as pdf:
        extracted_text = []
        for p_num in PAGES_TO_EXTRACT:
            if p_num < len(pdf.pages):
                page = pdf.pages[p_num]
                text = page.extract_text()
                if text:
                    extracted_text.append(f"### Page {p_num + 222} (Original)\n\n{text}\n")
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write("# 蓝牙传输架构层级 (Transport Architecture Hierarchy)\n\n")
            f.write("> 本文档提取自 Vol 1, Part A, Section 3。介绍了蓝牙从物理信道到逻辑链路的层级结构。\n\n")
            f.write("\n".join(extracted_text))

    print(f"Done. Content saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    extract()

