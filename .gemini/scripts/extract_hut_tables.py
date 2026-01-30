import pdfplumber
import pandas as pd
import json
import os
import re

# 配置路径
PDF_PATH = r"Docs/HUT/hut1_7.pdf"
OUTPUT_DIR = r"notebook/profiles/hid/data"

# 确保输出目录存在
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_table_from_range(pdf_path, start_page, end_page, table_type="keyboard"):
    """
    从指定页码范围提取表格数据。
    注意：pdfplumber 的 page_number 是从 1 开始的，但 pages 索引是从 0 开始的。
    PDF 页码通常对应 pages[page_num - 1]。
    """
    extracted_data = []
    
    print(f"Processing {table_type} from page {start_page} to {end_page}...")
    
    with pdfplumber.open(pdf_path) as pdf:
        # 遍历每一页
        for i in range(start_page - 1, end_page):
            page = pdf.pages[i]
            tables = page.extract_tables()
            
            for table in tables:
                # 简单的表头过滤，确保是 Usage 表
                # HUT 表格通常有: Usage ID, Usage Name, Usage Type
                if not table or len(table) < 2:
                    continue
                
                header = table[0]
                # 清洗表头: 去除换行符，转小写
                clean_header = [h.replace('\n', ' ').lower() if h else '' for h in header]
                
                # 识别有效表格
                if "usage id" in clean_header or "usage name" in clean_header:
                    # 跳过表头，处理每一行
                    for row in table[1:]:
                        # 过滤空行或无效行
                        if not row or all(c is None or c.strip() == "" for c in row):
                            continue
                            
                        # 尝试解析
                        try:
                            # 不同的表结构可能略有不同，这里做适配
                            # Keyboard Page 通常是: Usage ID | Usage Name | Usage Type
                            usage_id_raw = row[0]
                            usage_name_raw = row[1]
                            usage_type = row[2] if len(row) > 2 else ""
                            
                            # 清洗 Usage ID (去除换行，提取十六进制)
                            if usage_id_raw:
                                usage_id_clean = usage_id_raw.replace('\n', '').strip()
                            else:
                                continue

                            # 清洗 Usage Name
                            if usage_name_raw:
                                usage_name_clean = usage_name_raw.replace('\n', ' ').strip()
                            else:
                                continue
                                
                            extracted_data.append({
                                "usage_id": usage_id_clean,
                                "usage_name": usage_name_clean,
                                "usage_type": usage_type.replace('\n', ' ').strip() if usage_type else "",
                                "source_page": i + 1
                            })
                        except Exception as e:
                            print(f"Error parsing row on page {i+1}: {row} -> {e}")

    return extracted_data

def save_to_markdown(data, filename, title):
    """生成 Markdown 表格"""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write("| Usage ID | Usage Name | Type | Source Page |\n")
        f.write("| :--- | :--- | :--- | :--- |\n")
        
        for item in data:
            f.write(f"| {item['usage_id']} | {item['usage_name']} | {item['usage_type']} | {item['source_page']} |\n")
    
    print(f"Saved {len(data)} items to {filepath}")

def main():
    if not os.path.exists(PDF_PATH):
        print(f"Error: PDF not found at {PDF_PATH}")
        return

    # 1. 提取 Keyboard/Keypad Page (0x07)
    # 范围: Page 89 - 96 (根据书签)
    kb_data = extract_table_from_range(PDF_PATH, 89, 96, "Keyboard")
    save_to_markdown(kb_data, "keyboard_usage_table_raw.md", "Keyboard/Keypad Page (0x07) Usage Table")

    # 2. 提取 Consumer Page (0x0C) - Audio & Transport
    # 范围: Page 144 - 147 (Transport & Audio)
    # 为了更全，我们可以提取整个 Consumer Page 的核心部分 Page 125 - 150
    # 但为了精准，我们先聚焦多媒体键
    consumer_data = extract_table_from_range(PDF_PATH, 144, 147, "Consumer_Media")
    save_to_markdown(consumer_data, "consumer_media_usage_table_raw.md", "Consumer Page (0x0C) - Media & Transport")

if __name__ == "__main__":
    main()
