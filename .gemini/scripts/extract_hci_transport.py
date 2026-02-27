import pdfplumber
import os

BASE_DIR = "Docs/Bt-core/chunk/Vol 4 Host Controller Interface/"
OUT_DIR = "Knowledge_Base/vol4_hci/hci_raw/transport_raw/"

PARTS = [
    {
        "name": "h4_uart",
        "path": BASE_DIR + "Part A UART Transport Layer/source.pdf",
        "title": "Part A UART Transport Layer (H4)",
        "offset": 1736
    },
    {
        "name": "h2_usb",
        "path": BASE_DIR + "Part B USB Transport Layer/source.pdf",
        "title": "Part B USB Transport Layer (H2)",
        "offset": 1742
    },
    {
        "name": "sd",
        "path": BASE_DIR + "Part C Secure Digital (SD) Transport Layer/source.pdf",
        "title": "Part C Secure Digital (SD) Transport Layer",
        "offset": 1763
    },
    {
        "name": "h5_three_wire_uart",
        "path": BASE_DIR + "Part D Three-wire UART Transport Layer/source.pdf",
        "title": "Part D Three-wire UART Transport Layer (H5)",
        "offset": 1773
    }
]

def extract_pdf(info):
    if not os.path.exists(info["path"]):
        print(f"File not found: {info['path']}")
        return
        
    out_file = os.path.join(OUT_DIR, f"{info['name']}_raw.md")
    print(f"Extracting {info['title']} to {out_file}...")
    
    full_text = []
    with pdfplumber.open(info["path"]) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                offset = info['offset']
                full_text.append(f"### Page {i + 1 + offset} (Original)\n\n{text}\n")
                
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(f"# {info['title']}\n\n")
        f.write(f"> 本文档提取自 Vol 4, {info['title']}。\n\n")
        f.write("\n".join(full_text))
    print(f"Saved: {out_file}")

def main():
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)
        
    for part in PARTS:
        extract_pdf(part)

if __name__ == "__main__":
    main()
