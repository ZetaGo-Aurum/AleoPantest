import os

def replace_in_files(directory, search_str, replace_str):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.py', '.md', '.sh', '.html', '.yml', '.bat')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if search_str in content:
                        new_content = content.replace(search_str, replace_str)
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Updated: {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    base_dir = r"c:\Users\rayhan\Documents\PantestTool\AloPantest"
    
    # 1. Replace aleopantest with aleopantest (lowercase)
    print("Replacing aleopantest with aleopantest...")
    replace_in_files(base_dir, "aleopantest", "aleopantest")
    
    # 2. Replace Aleopantest with Aleopantest (PascalCase)
    print("Replacing Aleopantest with Aleopantest...")
    replace_in_files(base_dir, "Aleopantest", "Aleopantest")
    
    # 3. Replace aleopantest run with aleopantest run (usage examples)
    print("Replacing aleopantest run with aleopantest run...")
    replace_in_files(base_dir, "aleopantest run", "aleopantest run")
    
    # 4. Replace aleopantest with aleopantest (hyphenated)
    print("Replacing aleopantest with aleopantest...")
    replace_in_files(base_dir, "aleopantest", "aleopantest")

    print("Bulk replacement complete.")
