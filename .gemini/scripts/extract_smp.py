import pdfplumber
import os

PART_H_PDF = "Bluetooth_Knowledge_Base/Vol 3 Host/Part H Security Manager Specification/source.pdf"
DIR_OUT = "notebook/vol3_host/raw/smp_raw"

# Base Page: 1630

# Section 2.3: Pairing Methods (Legacy & Secure Connections)
# Page 1649 - 1668
RANGE_PAIRING_METHODS = range(19, 39)

# Section 3: Security Manager Protocol (Packet Formats & Key Dist)
# Page 1679 - 1699
RANGE_PROTOCOL = range(49, 70)

def extract_section(pdf, page_range, output_filename, title):
    print(f"Extracting {title} to {output_filename}...")
    full_text = []
    
    for p_num in page_range:
        if p_num < len(pdf.pages):
            page = pdf.pages[p_num]
            text = page.extract_text()
            full_text.append(f"### Page {p_num + 1630} (Original)\n\n{text}\n")
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n\n")
        f.write("> 本文档提取自 Vol 3, Part H Security Manager Specification。\n\n")
        f.write("\n".join(full_text))
    print(f"Saved: {output_filename}")

def main():
    if not os.path.exists(DIR_OUT):
        os.makedirs(DIR_OUT)

    if not os.path.exists(PART_H_PDF):
        print(f"Error: Source PDF not found at {PART_H_PDF}")
        return

    with pdfplumber.open(PART_H_PDF) as pdf:
        extract_section(pdf, RANGE_PAIRING_METHODS, 
                       os.path.join(DIR_OUT, "smp_pairing_methods_raw.md"), 
                       "SMP Pairing Methods (配对方法与算法)")
        
        extract_section(pdf, RANGE_PROTOCOL, 
                       os.path.join(DIR_OUT, "smp_protocol_raw.md"), 
                       "SMP Protocol Commands (PDU 格式与密钥分发)")

if __name__ == "__main__":
    main()
