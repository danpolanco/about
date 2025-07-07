#!/usr/bin/env python3
"""
Build script to combine resume sections into a single JSONResume format file.
"""

import json
from pathlib import Path

def get_repo_root():
    """Get the repository root directory."""
    current_dir = Path.cwd()
    script_dir = Path(__file__).parent
    
    # If we're in the src directory, go up one level
    if current_dir.name == "src" or script_dir.name == "src":
        return script_dir.parent if script_dir.name == "src" else current_dir.parent
    else:
        # Assume we're already at repo root
        return current_dir

def create_build_directory():
    """Create the build directory if it doesn't exist."""
    repo_root = get_repo_root()
    build_dir = repo_root / "build"
    build_dir.mkdir(exist_ok=True)
    return build_dir

def load_basics():
    """Load the basics section from src/resume/basics.json."""
    repo_root = get_repo_root()
    basics_file = repo_root / "src" / "resume" / "basics.json"
    
    if not basics_file.exists():
        raise FileNotFoundError(f"Basics file not found: {basics_file}")
    
    with open(basics_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_resume():
    """Build the complete resume JSON structure."""
    # Load basics section
    basics = load_basics()
    
    # Create the JSONResume structure with proper schema reference
    resume = {
        "$schema": "https://raw.githubusercontent.com/jsonresume/resume-schema/v1.0.0/schema.json",
        "basics": basics
    }
    
    return resume

def main():
    """Main build function."""
    try:
        # Create build directory
        build_dir = create_build_directory()
        
        # Build resume
        resume = build_resume()
        
        # Write to build/resume.json
        output_file = build_dir / "resume.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(resume, f, indent=2, ensure_ascii=False)
            f.write('\n')  # Add trailing newline
        
        print(f"Resume built successfully: {output_file}")
        print("Sections included: basics")
        
    except Exception as e:
        print(f"Build failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
