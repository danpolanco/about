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

def load_work():
    """Load all work experience files from src/resume/work/."""
    repo_root = get_repo_root()
    work_dir = repo_root / "src" / "resume" / "work"
    
    if not work_dir.exists():
        return []
    
    work_experiences = []
    
    # Get all JSON files in the work directory
    for work_file in sorted(work_dir.glob("*.json")):
        with open(work_file, 'r', encoding='utf-8') as f:
            work_data = json.load(f)
            work_experiences.append(work_data)
    
    # Sort by start date (most recent first)
    work_experiences.sort(key=lambda x: x.get('startDate', ''), reverse=True)
    
    return work_experiences

def load_volunteer():
    """Load all volunteer experience files from src/resume/volunteer/."""
    repo_root = get_repo_root()
    volunteer_dir = repo_root / "src" / "resume" / "volunteer"
    
    if not volunteer_dir.exists():
        return []
    
    volunteer_experiences = []
    
    # Get all JSON files in the volunteer directory
    for volunteer_file in sorted(volunteer_dir.glob("*.json")):
        with open(volunteer_file, 'r', encoding='utf-8') as f:
            volunteer_data = json.load(f)
            volunteer_experiences.append(volunteer_data)
    
    # Sort by start date (most recent first)
    volunteer_experiences.sort(key=lambda x: x.get('startDate', ''), reverse=True)
    
    return volunteer_experiences

def load_education():
    """Load all education files from src/resume/education/."""
    repo_root = get_repo_root()
    education_dir = repo_root / "src" / "resume" / "education"
    
    if not education_dir.exists():
        return []
    
    education_entries = []
    
    # Get all JSON files in the education directory
    for education_file in sorted(education_dir.glob("*.json")):
        with open(education_file, 'r', encoding='utf-8') as f:
            education_data = json.load(f)
            education_entries.append(education_data)
    
    # Sort by start date (most recent first)
    education_entries.sort(key=lambda x: x.get('startDate', ''), reverse=True)
    
    return education_entries

def build_resume():
    """Build the complete resume JSON structure."""
    # Load basics section
    basics = load_basics()
    
    # Load work experience sections
    work = load_work()
    
    # Load volunteer experience sections
    volunteer = load_volunteer()
    
    # Load education sections
    education = load_education()
    
    # Create the JSONResume structure with proper schema reference
    resume = {
        "$schema": "https://raw.githubusercontent.com/jsonresume/resume-schema/v1.0.0/schema.json",
        "basics": basics
    }
    
    # Only include sections that have content
    if work:
        resume["work"] = work
    if volunteer:
        resume["volunteer"] = volunteer
    if education:
        resume["education"] = education
    
    return resume

def main():
    """Main build function."""
    try:
        # Create build directory
        build_dir = create_build_directory()
        
        # Build resume
        resume = build_resume()
        
        # Determine which sections are included
        sections = ["basics"]
        if resume.get("work"):
            sections.append("work")
        if resume.get("volunteer"):
            sections.append("volunteer")
        if resume.get("education"):
            sections.append("education")
        
        # Write to build/resume.json
        output_file = build_dir / "resume.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(resume, f, indent=2, ensure_ascii=False)
            f.write('\n')  # Add trailing newline
        
        print(f"Resume built successfully: {output_file}")
        print(f"Sections included: {', '.join(sections)}")
        
    except Exception as e:
        print(f"Build failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
