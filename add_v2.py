import os
import glob

for filepath in glob.glob('**/*.html', recursive=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'style.css"' in content:
        content = content.replace('style.css"', 'style.css?v=2"')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")
