import re
import os

cli_path = 'aleopantest/cli.py'
with open(cli_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern for imports: from aleopantest.modules.* import (...)
import_blocks = re.finditer(r'from aleopantest\.modules\.([a-zA-Z0-9_]+)\s+import\s+\(([\s\S]*?)\)', content)

missing_classes = set()

for match in import_blocks:
    module_name = match.group(1)
    imported_str = match.group(2)
    # Extract classes
    classes = [c.strip() for c in imported_str.replace('\n', ' ').split(',') if c.strip()]
    
    # Try dynamic import and check each class
    try:
        mod = __import__(f'aleopantest.modules.{module_name}', fromlist=[''])
        for cls in classes:
            if not hasattr(mod, cls):
                missing_classes.add(cls)
                print(f"Missing {cls} in {module_name}")
    except ModuleNotFoundError:
        print(f"Missing entire module {module_name}")
        missing_classes.update(classes)

print(f"Total missing classes: {len(missing_classes)}")

# Now we need to remove these classes from the import blocks
new_content = content
for cls in missing_classes:
    # Remove from imports: 'cls,' or 'cls' at end of block
    new_content = re.sub(r'\b' + cls + r'\b\s*,?', '', new_content)
    # Remove from TOOLS_REGISTRY: 'key': cls,
    new_content = re.sub(r"\'[a-zA-Z0-9_-]+\':\s*" + cls + r"\s*,", '', new_content)

# Clean up empty commas in imports like '(, , Something)' -> '(Something)'
new_content = re.sub(r',\s*,', ',', new_content)
new_content = re.sub(r'\(\s*,', '(', new_content)
new_content = re.sub(r',\s*\)', ')', new_content)

with open(cli_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("cli.py cleaned.")
