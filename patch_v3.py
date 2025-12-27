import os
import re

def patch_modules():
    modules_dir = r"c:\Users\rayhan\Documents\PantestTool\AloPantest\aleopantest\modules"
    
    for root, dirs, files in os.walk(modules_dir):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 1. Update version to 3.0.0
                content = re.sub(r'version\s*=\s*["\'][^"\']+["\']', 'version="3.0.0"', content)
                
                # 2. Update author to Aleocrophic Team
                content = re.sub(r'author\s*=\s*["\'][^"\']+["\']', 'author="Aleocrophic Team"', content)
                
                # 3. Ensure get_results() usage in run method
                # We'll replace return statements that don't use get_results()
                if "def run" in content:
                    # Find the run method body
                    run_start = content.find("def run")
                    # Simplified: find the next def or end of file
                    next_def = content.find("def ", run_start + 1)
                    if next_def == -1: next_def = len(content)
                    
                    run_body = content[run_start:next_def]
                    
                    # Replace various return patterns with self.get_results()
                    new_run_body = re.sub(r'return\s+result$', 'return self.get_results()', run_body, flags=re.MULTILINE)
                    new_run_body = re.sub(r'return\s+results$', 'return self.get_results()', new_run_body, flags=re.MULTILINE)
                    new_run_body = re.sub(r'return\s+self\.results$', 'return self.get_results()', new_run_body, flags=re.MULTILINE)
                    
                    # If it ends with just 'return' or nothing, and has add_result calls, add return self.get_results()
                    if "self.add_result" in new_run_body and "return self.get_results()" not in new_run_body:
                        # Find last line of run body and append
                        lines = new_run_body.splitlines()
                        # find last non-empty line
                        for i in range(len(lines)-1, -1, -1):
                            if lines[i].strip():
                                # Add return with same indentation as previous line
                                indent = len(lines[i]) - len(lines[i].lstrip())
                                lines.append(" " * indent + "return self.get_results()")
                                break
                        new_run_body = "\n".join(lines)
                    
                    content = content[:run_start] + new_run_body + content[next_def:]
                
                # 4. Add V3.0 Patch Header in docstring if not present
                if '"""' in content:
                    first_doc = content.find('"""')
                    second_doc = content.find('"""', first_doc + 3)
                    if second_doc != -1:
                        doc_content = content[first_doc+3:second_doc]
                        if "V3.0 Major Patch" not in doc_content:
                            new_doc = doc_content.strip() + "\n\nV3.0 Major Patch: Enhanced accuracy, powerful features, and standardized output."
                            content = content[:first_doc+3] + "\n" + new_doc + "\n" + content[second_doc:]

                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Patched: {path}")

if __name__ == "__main__":
    patch_modules()
