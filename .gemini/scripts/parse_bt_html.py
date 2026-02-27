import re
import argparse
import sys

def parse_html_toc(html_content):
    """提取 HTML 目录树"""
    pattern = r'class="topic-link".*?>(?:<span.*?></span>)?\s*(.*?)\s*</a>'
    matches = re.findall(pattern, html_content, re.DOTALL)
    
    toc = []
    for match in matches:
        clean_match = re.sub(r'<[^>]*>', '', match).strip()
        if clean_match:
            toc.append(clean_match)
    return toc

def extract_section(html_content, section_id):
    """提取指定章节的正文内容 (基于 <hX class="title">...<span class="formal-number">X.Y</span>...<span class="formal-title">Name</span></hX>)"""
    # 此处为简化版正则提取，针对 BT SIG 的标准规范文档结构
    # 找到目标章节的起始位置
    start_pattern = f'<h[1-6][^>]*class="title"[^>]*>.*?<span class="formal-number">{re.escape(section_id)}</span>.*?<span class="formal-title">(.*?)</span>.*?</h[1-6]>'
    start_match = re.search(start_pattern, html_content, re.DOTALL)
    
    if not start_match:
        return f"未找到章节: {section_id}"
    
    section_title = start_match.group(1).strip()
    start_pos = start_match.end()
    
    # 找到下一个同级或更高层的 h 标签作为结束位置
    end_pattern = r'<h[1-6][^>]*class="title"[^>]*>.*?<span class="formal-number">'
    # 在目标章节之后搜索
    end_match = re.search(end_pattern, html_content[start_pos:], re.DOTALL)
    
    end_pos = start_pos + end_match.start() if end_match else len(html_content)
    
    content = html_content[start_pos:end_pos]
    
    # 清理内容中的 html 标签，保留基本文本
    # 注意：这只是一个基础的纯文本提取，对于复杂的表格和列表，建议使用 BeautifulSoup 等库进行更精细的处理
    text_content = re.sub(r'<p[^>]*>', '\\n', content)
    text_content = re.sub(r'<li[^>]*>', '\\n- ', text_content)
    text_content = re.sub(r'<[^>]*>', '', text_content)
    
    # 去除多余空行
    text_content = re.sub(r'\\n\s*\\n', '\\n\\n', text_content).strip()
    
    return f"# {section_id} {section_title}\\n\\n{text_content}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bluetooth SIG HTML 规范解析工具")
    parser.add_argument("file", help="HTML 文件路径")
    parser.add_argument("--toc", action="store_true", help="提取完整的目录树 (Table of Contents)")
    parser.add_argument("--section", type=str, help="提取指定章节编号的正文，例如: 3.5.2")
    
    args = parser.parse_args()
    
    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            html = f.read()
            
        if args.toc:
            print("=== Table of Contents ===")
            toc = parse_html_toc(html)
            for item in toc:
                print(item)
                
        if args.section:
            print(f"=== Section {args.section} ===")
            content = extract_section(html, args.section)
            print(content)
            
    except FileNotFoundError:
        print(f"错误: 找不到文件 '{args.file}'")
        sys.exit(1)
    except Exception as e:
        print(f"发生错误: {e}")
        sys.exit(1)
