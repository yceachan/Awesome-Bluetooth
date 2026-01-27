import pdfplumber
import os

PART_E_PDF = "Bluetooth_Knowledge_Base/Vol 4 Host Controller Interface/Part E Host Controller Interface Functional Specification/source.pdf"
DIR_OUT = "notebook/vol4_hci/hci_raw"

# Base Page: 1802

# Section 5.4: HCI Specific Information (Packet Formats) - Page 1885 - 1893
RANGE_PACKET_FORMATS = range(83, 92)

# Selected Commands for Initialization Flow
# Reset (Page 2053)
RANGE_CMD_RESET = range(251, 252)
# Read Local Version (Page 2205)
RANGE_CMD_READ_VER = range(403, 404)
# LE Set Advertising Parameters (Page 2510 - 2513)
RANGE_CMD_SET_ADV_PARAM = range(708, 712)

def extract_section(pdf, page_range, output_filename, title):
    print(f"Extracting {title} to {output_filename}...")
    full_text = []
    
    for p_num in page_range:
        if p_num < len(pdf.pages):
            page = pdf.pages[p_num]
            text = page.extract_text()
            full_text.append(f"### Page {p_num + 1802} (Original)\n\n{text}\n")
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n\n")
        f.write("> 本文档提取自 Vol 4, Part E HCI Functional Specification。\n\n")
        f.write("\n".join(full_text))
    print(f"Saved: {output_filename}")

def main():
    if not os.path.exists(DIR_OUT):
        os.makedirs(DIR_OUT)

    if not os.path.exists(PART_E_PDF):
        print(f"Error: Source PDF not found at {PART_E_PDF}")
        return

    with pdfplumber.open(PART_E_PDF) as pdf:
        extract_section(pdf, RANGE_PACKET_FORMATS, 
                       os.path.join(DIR_OUT, "hci_packet_formats_raw.md"), 
                       "HCI Packet Formats (Command, Event, ACL)")
        
        extract_section(pdf, RANGE_CMD_RESET, 
                       os.path.join(DIR_OUT, "hci_cmd_reset_raw.md"), 
                       "HCI Command: Reset")
        
        extract_section(pdf, RANGE_CMD_READ_VER, 
                       os.path.join(DIR_OUT, "hci_cmd_read_ver_raw.md"), 
                       "HCI Command: Read Local Version")

        extract_section(pdf, RANGE_CMD_SET_ADV_PARAM, 
                       os.path.join(DIR_OUT, "hci_cmd_set_adv_param_raw.md"), 
                       "HCI Command: LE Set Adv Params")

if __name__ == "__main__":
    main()
