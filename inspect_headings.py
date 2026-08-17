import json

with open('manual_extracted_structure.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

headings = [el for el in data if el['type'] == 'heading']
for h in headings[:120]:
    indent = '  ' * (h['level'] - 1)
    level = h['level']
    text = h['text']
    print(f"{indent}H{level}: {text}")

print(f"\nTotal headings: {len(headings)}")
print(f"Total elements: {len(data)}")

# count by level
from collections import Counter
levels = Counter(h['level'] for h in headings)
print("Headings by level:", dict(sorted(levels.items())))
