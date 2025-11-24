#!/usr/bin/env python
"""
Fix build.sh line endings and permissions for Unix/Linux
This ensures build.sh works correctly on Render
"""
import os
from pathlib import Path

def fix_build_script():
    """Convert build.sh to Unix line endings and set executable permission"""
    build_file = Path(__file__).parent / 'build.sh'
    
    if not build_file.exists():
        print("❌ build.sh not found!")
        return False
    
    # Read the file
    with open(build_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace Windows line endings with Unix line endings
    content = content.replace('\r\n', '\n')
    
    # Write back with Unix line endings
    with open(build_file, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)
    
    print("✅ Fixed line endings in build.sh")
    
    # Try to set executable permission (works on Unix-like systems)
    try:
        os.chmod(build_file, 0o755)
        print("✅ Set executable permission on build.sh")
    except Exception as e:
        print(f"⚠️  Could not set executable permission: {e}")
        print("   (This is normal on Windows - Render will handle it)")
    
    return True

if __name__ == '__main__':
    print("🔧 Fixing build.sh for Unix/Linux...")
    print()
    
    if fix_build_script():
        print()
        print("✅ build.sh is ready for deployment!")
    else:
        print()
        print("❌ Failed to fix build.sh")
