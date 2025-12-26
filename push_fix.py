#!/usr/bin/env python3
"""Push fix to GitHub"""
import subprocess
import os
import sys

os.chdir(r'c:\Users\rayhan\Documents\PantestTool\AloPantest')

try:
    # Reset to abort any merge
    print("Resetting repository...")
    subprocess.run(['git', 'reset', '--hard', 'HEAD'], check=True, timeout=10)
    
    # Pull latest
    print("Pulling latest changes...")
    subprocess.run(['git', 'pull', '--rebase'], check=False, timeout=10)
    
    # Push
    print("Pushing to GitHub...")
    subprocess.run(['git', 'push'], check=True, timeout=10)
    
    print("✓ Successfully pushed to GitHub")
    sys.exit(0)
    
except subprocess.CalledProcessError as e:
    print(f"✗ Git command failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)
