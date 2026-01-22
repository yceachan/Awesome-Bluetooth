import pdfplumber
import os

PART_A_PDF = "Bluetooth_Knowledge_Base/Vol 3 Host/Part A Logical Link Control and Adaptation Protocol Specification/source.pdf"
DIR_OUT = "notebook/vol3_host"

# Relative pages (Original - 1084)
RANGE_OPS = range(14, 22)   # 1098-1105: General Operation
RANGE_PKT = range(22, 34)   # 1106-1117: Packet Formats
RANGE_LE  = range(160, 162) # 1244-1245: LE Credit Based Flow Control

def extract_section(pdf, page_range, output_filename, title, mode='w'):
    print(f"Extracting {title} to {output_filename}...")
    full_text = []
    
    for p_num in page_range:
        if p_num < len(pdf.pages):
            page = pdf.pages[p_num]
            text = page.extract_text()
            if text:
                full_text.append(f"### Page {p_num + 1084} (Original)\n\n{text}\n")
    
    with open(output_filename, mode, encoding='utf-8') as f:
        if mode == 'w':
            f.write(f"# {title}\n\n")
            f.write("> 本文档提取自 Vol 3, Part A L2CAP Specification。\n\n")
        f.write("\n".join(full_text))
    print(f"Saved: {output_filename}")

def main():
    if not os.path.exists(DIR_OUT):
        os.makedirs(DIR_OUT)

    if not os.path.exists(PART_A_PDF):
        print(f"Error: Source PDF not found at {PART_A_PDF}")
        return

    with pdfplumber.open(PART_A_PDF) as pdf:
        # 1. Channels & Operation
        extract_section(pdf, RANGE_OPS, 
                       os.path.join(DIR_OUT, "l2cap_general_operation.md"), 
                       "L2CAP General Operation (通道与模式)")
        
        # 2. Append LE Flow Control to General Operation
        extract_section(pdf, RANGE_LE, 
                       os.path.join(DIR_OUT, "l2cap_general_operation.md"), 
                       "LE Credit Based Flow Control", mode='a')

        # 3. Packet Formats
        extract_section(pdf, RANGE_PKT, 
                       os.path.join(DIR_OUT, "l2cap_packet_formats.md"), 
                       "L2CAP Packet Formats (数据包结构)")

if __name__ == "__main__":
    main()
