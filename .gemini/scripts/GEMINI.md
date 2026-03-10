# Script Library Index

This file acts as the central registry for the Agent's tool belt. All high-value, reusable scripts in `.gemini/scripts/` must be logged here.

## Registered Scripts

| Script Name | Function | Usage Example | Tags |
| :--- | :--- | :--- | :--- |
| `optimized_split_pdf.py` | Splits large PDF specifications into smaller parts based on XML bookmark data. | `python .gemini/scripts/optimized_split_pdf.py` | `pdf`, `core-spec` |
| `extract_gatt.py` | Extracts GATT definitions, hierarchy, and procedures from Core Spec Vol 3. | `python .gemini/scripts/extract_gatt.py` | `extraction`, `gatt` |
| `extract_l2cap.py` | Extracts L2CAP channel modes and packet formats. | `python .gemini/scripts/extract_l2cap.py` | `extraction`, `l2cap` |
| `extract_msc.py` | Extracts Message Sequence Charts text for Mermaid diagram generation. | `python .gemini/scripts/extract_msc.py` | `extraction`, `visualization` |
| `generate_root_index.py` | Regenerates the root knowledge base structure and index files. | `python .gemini/scripts/generate_root_index.py` | `maintenance`, `index` |
| `generate_kb_index.py` | Scans the Knowledge_Base directory and generates a JSON index. | `python .gemini/scripts/generate_kb_index.py` | `maintenance`, `index`, `json` |
| `parse_bt_html.py` | Parses Bluetooth SIG HTML specs (like BAP, CAS) to extract TOC and section contents. See `bt_html_parsing_guide.md` for details. | `python .gemini/scripts/parse_bt_html.py --toc "path/to.html"` | `html`, `parsing`, `extraction` |
