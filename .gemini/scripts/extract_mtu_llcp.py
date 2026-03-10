import pdfplumber
import os

def extract_section(pdf_path, start_page, end_page, offset, output_filename, title):
    print(f"Extracting {title} to {output_filename}...")
    if not os.path.exists(pdf_path):
        print(f"Error: PDF not found at {pdf_path}")
        return

    full_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for p_num in range(start_page - offset, end_page - offset + 1):
            if 0 <= p_num < len(pdf.pages):
                page = pdf.pages[p_num]
                text = page.extract_text()
                if text:
                    full_text.append(f"### Page {p_num + offset} (Original)\n\n{text}\n")
    
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n\n")
        f.write("\n".join(full_text))
    print(f"Saved: {output_filename}")

if __name__ == "__main__":
    # LLCP Chapter 5 (Pages 3189 to 3255)
    extract_section(
        "Docs/Bt-core/chunk/Vol 6 Low Energy Controller/Part B Link Layer Specification/source.pdf",
        3189, 3255, 2944,
        "Knowledge_Base/vol6_controller/llcp_raw.md",
        "LLCP Specification"
    )

    # L2CAP MTU Section 5.1 (Pages 1147 to 1149)
    extract_section(
        "Docs/Bt-core/chunk/Vol 3 Host/Part A Logical Link Control and Adaptation Protocol Specification/source.pdf",
        1147, 1149, 1084,
        "Knowledge_Base/vol3_host/l2cap/l2cap_mtu_raw.md",
        "L2CAP MTU Specification"
    )

    # GATT MTU Section 4.3.1 (Page 1579 to 1580)
    extract_section(
        "Docs/Bt-core/chunk/Vol 3 Host/Part G Generic Attribute Profile (GATT)/source.pdf",
        1579, 1580, 1547,
        "Knowledge_Base/vol3_host/gatt/gatt_mtu_raw.md",
        "GATT MTU Specification"
    )
