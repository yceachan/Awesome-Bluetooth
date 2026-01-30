import pdfplumber
import pandas as pd
import json
import os
import re

# 配置路径
PDF_PATH = r"Docs/HUT/hut1_7.pdf"
OUTPUT_DIR = r"notebook/profiles/hid/data"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_text(text):
    if not text: return ""
    return text.replace('\n', ' ').strip()

def extract_tables_smart(pdf_path, start_page, end_page, table_type="keyboard"):
    extracted_data = []
    print(f"Processing {table_type} from page {start_page} to {end_page}...")
    
    with pdfplumber.open(pdf_path) as pdf:
        for i in range(start_page - 1, end_page):
            page = pdf.pages[i]
            
            # 策略 A: 默认提取 (适用于 Keyboard Page)
            # 策略 B: 基于文本间隙提取 (适用于 Consumer Page)
            settings = {}
            if "consumer" in table_type.lower():
                settings = {
                    "vertical_strategy": "text",
                    "horizontal_strategy": "text",
                    "snap_tolerance": 3,
                }
            
            tables = page.extract_tables(settings)
            
            for table in tables:
                if not table or len(table) < 2: continue
                
                # 尝试定位 Usage ID 和 Usage Name 列
                # Keyboard Page: [ID, Name, Type]
                # Consumer Page: [Name, Type, Description] OR [ID, Name, Type] (有些页可能有 ID)
                
                # 简单启发式: 寻找 ID 列 (十六进制) 和 Name 列
                for row in table:
                    # 跳过表头 (简单的非数据行过滤)
                    if "Usage Name" in str(row) or "Usage ID" in str(row):
                        continue
                        
                    clean_row = [clean_text(c) for c in row]
                    
                    # 判别逻辑
                    item = {}
                    
                    if table_type == "keyboard":
                        # Keyboard 格式通常很好: Col 0 = ID, Col 1 = Name
                        if len(clean_row) >= 2 and re.match(r'^[0-9A-F]{2}$', clean_row[0], re.I):
                            item = {
                                "usage_id": clean_row[0],
                                "usage_name": clean_row[1],
                                "usage_type": clean_row[2] if len(clean_row) > 2 else "",
                                "source_page": i + 1
                            }
                    
                    elif "consumer" in table_type.lower():
                        # Consumer Page 比较乱。有些表没有 ID，只有 Name | Type | Desc
                        # 我们需要根据 Name 去反查 ID (如果 PDF 里没有显示 ID)
                        # 等等，HUT 文档里 Consumer Page 表格只有 Name, Type, Description。ID 是隐含的顺序吗？
                        # 不，通常开头会有 Usage ID 段，或者表里有 ID。
                        # 重新看 Page 145 snippet: "Usage Name Usage Type Description"
                        # 确实没有 Usage ID 列！这意味着 Usage ID 可能在段落标题里，或者是顺序递增？
                        # 不，HUT 里 ID 是显式的。让我们再仔细看一眼 Page 137 (Consumer Page start)
                        
                        # 临时策略: 先提取 Name 和 Description，ID 后续人工或通过其他方式补全
                        # 如果第一列是 Name (字母开头), 第二列是 Type (大写缩写)
                        name = clean_row[0]
                        
                        # 尝试识别 Type (通常是 OOC, MC, OSC, RTC, LC)
                        # 如果 clean_row[1] 是 Type
                        type_cand = clean_row[1] if len(clean_row) > 1 else ""
                        
                        if name and re.match(r'^[A-Z]{2,4}$', type_cand):
                             item = {
                                "usage_id": "TBD", # ID 缺失
                                "usage_name": name,
                                "usage_type": type_cand,
                                "description": clean_row[2] if len(clean_row) > 2 else "",
                                "source_page": i + 1
                            }
                    
                    if item:
                        extracted_data.append(item)

    return extracted_data

def save_to_markdown(data, filename, title):
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        if data and "description" in data[0]:
             f.write("| Usage Name | Type | Description | Source Page |\n")
             f.write("| :--- | :--- | :--- | :--- |\n")
             for item in data:
                f.write(f"| {item['usage_name']} | {item['usage_type']} | {item.get('description', '')} | {item['source_page']} |\n")
        else:
            f.write("| Usage ID | Usage Name | Type | Source Page |\n")
            f.write("| :--- | :--- | :--- | :--- |\n")
            for item in data:
                f.write(f"| {item['usage_id']} | {item['usage_name']} | {item['usage_type']} | {item['source_page']} |\n")
    
    print(f"Saved {len(data)} items to {filepath}")

def main():
    # 1. Keyboard (Page 89-96)
    kb_data = extract_tables_smart(PDF_PATH, 89, 96, "keyboard")
    save_to_markdown(kb_data, "keyboard_usage_table_raw.md", "Keyboard/Keypad Page (0x07)")

    # 2. Consumer Media (Page 145-148)
    # 重点关注 Transport (Play, Pause) 和 Audio (Vol+, Vol-)
    media_data = extract_tables_smart(PDF_PATH, 145, 148, "consumer")
    save_to_markdown(media_data, "consumer_media_usage_table_raw.md", "Consumer Page (0x0C) Media")

if __name__ == "__main__":
    main()
