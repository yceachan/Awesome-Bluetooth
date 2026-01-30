import pdfplumber
import re

PDF_PATH = r"D:\Workspace\Extlibs\蓝牙协议栈\Docs\USB-HID\hid1_11.pdf"
OUTPUT_PATH = r"D:\Workspace\Extlibs\蓝牙协议栈\.gemini\hid_core_extract.txt"

# Target Sections based on TOC:
# 5. Operational Model: Page 12 (Logical)
# 6.2.2 Report Descriptor: Page 23 (Logical)
# Appendix B: Boot Interface: Page 59 (Logical)

def extract_core_knowledge():
    text_buffer = []
    
    with pdfplumber.open(PDF_PATH) as pdf:
        # Heuristic: Find the offset. Usually 'Introduction' is page 1.
        # Let's search for "5. Operational Model" to find the start.
        start_page_index = -1
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if "5. Operational Model" in text:
                start_page_index = i
                break
        
        if start_page_index == -1:
            print("Could not find start page.")
            return

        print(f"Found '5. Operational Model' at physical page {start_page_index}")

        # Extract Section 5 and 6 (approx 35 pages from start of Sec 5)
        # Section 5 starts at 12. Section 7 starts at 48.
        # So we want roughly 12 -> 48.
        # Logical 12 is at index `start_page_index`.
        # We want to extract until Logical Page 48.
        
        pages_to_extract = 40 # Covers Sec 5 and 6
        
        text_buffer.append("=== SECTION 5 & 6: OPERATIONAL MODEL & DESCRIPTORS ===\n")
        for i in range(start_page_index, start_page_index + pages_to_extract):
            if i < len(pdf.pages):
                page = pdf.pages[i]
                text_buffer.append(f"--- Page {i} ---\n")
                text_buffer.append(page.extract_text())

        # Extract Appendix B (Boot Interface)
        # Logical Page 59. 
        # If Logical 12 is at `start_page_index`, then Logical 59 is at `start_page_index + (59-12) = start_page_index + 47`.
        boot_page_index = start_page_index + 47
        text_buffer.append("\n=== APPENDIX B: BOOT INTERFACE ===\n")
        for i in range(boot_page_index, boot_page_index + 5): # 5 pages for Appx B
            if i < len(pdf.pages):
                page = pdf.pages[i]
                text_buffer.append(f"--- Page {i} ---\n")
                text_buffer.append(page.extract_text())

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(text_buffer))
    
    print(f"Extraction complete. Saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    extract_core_knowledge()
