import pdfplumber
import os

PART_B_PDF = "Docs/Bt-core/chunk/Vol 6 Low Energy Controller/Part B Link Layer Specification/source.pdf"
DIR_OUT = "notebook/vol6_controller"

# 相对页码 = 原始页码 - 2944
# 1.1 Link Layer States: 2955-2958 -> 11-14
RANGE_STATES = range(11, 16) 

# 2 Air Interface Packets: 2965-2990 -> 21-46
# 覆盖 Packet Format, Advertising PDUs 核心定义
RANGE_PACKETS = range(21, 47)

def extract_section(pdf, page_range, output_filename, title):
    print(f"Extracting {title} to {output_filename}...")
    full_text = []
    
    for p_num in page_range:
        if p_num < len(pdf.pages):
            page = pdf.pages[p_num]
            text = page.extract_text()
            if text:
                full_text.append(f"### Page {p_num + 2944} (Original)\n\n{text}\n")
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n\n")
        f.write("> 本文档提取自 Vol 6, Part B Link Layer Specification。\n\n")
        f.write("\n".join(full_text))
    print(f"Saved: {output_filename}")

def main():
    if not os.path.exists(DIR_OUT):
        os.makedirs(DIR_OUT)

    if not os.path.exists(PART_B_PDF):
        print(f"Error: Source PDF not found at {PART_B_PDF}")
        return

    with pdfplumber.open(PART_B_PDF) as pdf:
        # Extract States
        extract_section(pdf, RANGE_STATES, 
                       os.path.join(DIR_OUT, "link_layer_states.md"), 
                       "BLE Link Layer States (链路层状态)")
        
        # Extract Packets
        extract_section(pdf, RANGE_PACKETS, 
                       os.path.join(DIR_OUT, "air_interface_packets.md"), 
                       "BLE Air Interface Packets (空口包格式)")

if __name__ == "__main__":
    main()
