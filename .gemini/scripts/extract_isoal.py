import pdfplumber
import os

PART_G_PDF = "Docs/Bt-core/chunk/Vol 6 Low Energy Controller/Part G Isochronous Adaptation Layer/source.pdf"
DIR_OUT = "notebook/vol6_controller/iso_raw"

# Base Page: 3760

# Section 2: ISOAL Features (Fragmentation & Segmentation)
# Page 3763 - 3769
RANGE_FEATURES = range(3, 10)

# Section 3: Time Stamp and Offset (Timing)
# Page 3770 - 3778
RANGE_TIMING = range(10, 19)

def extract_section(pdf, page_range, output_filename, title):
    print(f"Extracting {title} to {output_filename}...")
    full_text = []
    
    for p_num in page_range:
        if p_num < len(pdf.pages):
            page = pdf.pages[p_num]
            text = page.extract_text()
            full_text.append(f"### Page {p_num + 3760} (Original)\n\n{text}\n")
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n\n")
        f.write("> 本文档提取自 Vol 6, Part G Isochronous Adaptation Layer (ISOAL)。\n\n")
        f.write("\n".join(full_text))
    print(f"Saved: {output_filename}")

def main():
    if not os.path.exists(DIR_OUT):
        os.makedirs(DIR_OUT)

    if not os.path.exists(PART_G_PDF):
        print(f"Error: Source PDF not found at {PART_G_PDF}")
        return

    with pdfplumber.open(PART_G_PDF) as pdf:
        extract_section(pdf, RANGE_FEATURES, 
                       os.path.join(DIR_OUT, "isoal_features_raw.md"), 
                       "ISOAL Features (Framed vs Unframed PDU)")
        
        extract_section(pdf, RANGE_TIMING, 
                       os.path.join(DIR_OUT, "isoal_timing_raw.md"), 
                       "ISOAL Timing (Time Stamp & Offset)")

if __name__ == "__main__":
    main()
