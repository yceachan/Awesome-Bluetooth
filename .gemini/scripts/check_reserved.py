import pdfplumber
import re

PDF_PATH = r"Docs/HUT/hut1_7.pdf"

def check_reserved_range():
    with pdfplumber.open(PDF_PATH) as pdf:
        # Keyboard Page 跨越 Page 90 - 97 (Index 89 - 96)
        # 我们搜索包含 "A4" 或 "A5" 的行
        print("Scanning for Usage ID A4, A5, or Reserved range...")
        for i in range(89, 97):
            page = pdf.pages[i]
            text = page.extract_text()
            # 简单打印包含 A4, A5, DF, E0 附近的文本行
            for line in text.split('\n'):
                if re.search(r'\b(A4|A5|DF|E0|Reserved)\b', line, re.I):
                    print(f"[Page {i+1}] {line.strip()}")

if __name__ == "__main__":
    check_reserved_range()

