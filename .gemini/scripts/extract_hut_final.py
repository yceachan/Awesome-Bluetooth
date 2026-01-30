import pdfplumber
import os
import re

PDF_PATH = r"Docs/HUT/hut1_7.pdf"
OUTPUT_DIR = r"notebook/profiles/hid/data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_text(text):
    if not text:
        return ""
    return text.replace('\n', ' ').strip()

def extract_keyboard(pdf):
    data = []
    print("Processing Keyboard (Page 89-96)...")
    for i in range(88, 96): # Page 89-96
        page = pdf.pages[i]
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                if not row or len(row) < 2: continue
                c0 = clean_text(row[0])
                c1 = clean_text(row[1])
                
                # Keyboard Page: Col 0 is 2-digit Hex ID
                if re.match(r'^[0-9A-F]{2}$', c0, re.I):
                    data.append({
                        "usage_id": c0,
                        "usage_name": c1,
                        "usage_type": clean_text(row[2]) if len(row) > 2 else "",
                        "source_page": i + 1
                    })
    return data

def extract_consumer(pdf):
    data = []
    print("Processing Consumer (Page 145-148)...")
    for i in range(144, 148): # Page 145-148
        page = pdf.pages[i]
        settings = {"vertical_strategy": "text", "horizontal_strategy": "text"}
        tables = page.extract_tables(settings)
        
        for table in tables:
            for row in table:
                if not row or len(row) < 2: continue
                c0 = clean_text(row[0]) # Name
                c1 = clean_text(row[1]) # Type
                
                if "Usage Name" in c0: continue
                
                # Consumer Page: Col 1 is Type (OOC, OSC...)
                if re.match(r'^(OOC|OSC|LC|MC|RTC|Sel|SV|SF|DF|DV)$', c1):
                    data.append({
                        "usage_name": c0,
                        "usage_type": c1,
                        "description": clean_text(row[2]) if len(row) > 2 else "",
                        "source_page": i + 1
                    })
    return data

def save_md(data, filename, title, headers):
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write("| " + " | ".join(headers) + " |\n")
        f.write("| " + " | ".join([":---"] * len(headers)) + " |\n")
        
        for item in data:
            row = []
            for h in headers:
                key = h.lower().replace(" ", "_")
                row.append(str(item.get(key, "")))
            f.write("| " + " | ".join(row) + " |\n")
    print(f"Saved {len(data)} items to {filepath}")

def main():
    if not os.path.exists(PDF_PATH):
        print("PDF not found!")
        return
        
    with pdfplumber.open(PDF_PATH) as pdf:
        kb_data = extract_keyboard(pdf)
        save_md(kb_data, "ref_keyboard_usage_map.md", "Keyboard/Keypad Page (0x07)", ["Usage ID", "Usage Name", "Usage Type"])
        
        consumer_data = extract_consumer(pdf)
        save_md(consumer_data, "consumer_media_raw.md", "Consumer Page (0x0C) - Media", ["Usage Name", "Usage Type", "Description"])

if __name__ == "__main__":
    main()