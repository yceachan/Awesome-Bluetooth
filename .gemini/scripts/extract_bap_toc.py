import re

file_path = 'Docs/LE-Audio/Basic Audio Profile _ Bluetooth® Technology Website.html'
with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Match links like <a ... class="topic-link">...Section Name</a>
# Note: some might have spans inside
pattern = r'class="topic-link".*?>(?:<span.*?></span>)?\s*(.*?)\s*</a>'
matches = re.findall(pattern, html, re.DOTALL)

for match in matches:
    clean_match = re.sub(r'<[^>]*>', '', match).strip()
    if clean_match:
        print(clean_match)
