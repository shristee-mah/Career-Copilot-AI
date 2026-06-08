import json
import re

file_path = 'notebooks/agent.ipynb'
with open(file_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

for cell in nb.get('cells', []):
    if 'source' in cell:
        for i, line in enumerate(cell['source']):
            # Remove any string assigned to GOOGLE_API_KEY
            line = re.sub(r'os\.environ\["GOOGLE_API_KEY"\]\s*=\s*".*"', 'os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"', line)
            line = re.sub(r"os\.environ\['GOOGLE_API_KEY'\]\s*=\s*'.*'", 'os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"', line)
            cell['source'][i] = line

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
print('Cleaned GOOGLE_API_KEY')
