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

def load_section(section_name):
    """Load all JSON files from a resume section directory."""
    repo_root = get_repo_root()
    section_dir = repo_root / "src" / "resume" / section_name
    
    if not section_dir.exists():
        return []
    
    section_entries = []
    
    # Get all JSON files in the section directory
    for section_file in sorted(section_dir.glob("*.json")):
        with open(section_file, 'r', encoding='utf-8') as f:
            section_data = json.load(f)
            section_entries.append(section_data)
    
    # Sort by appropriate date field (most recent first)
    # Different sections use different date fields
    date_field = "startDate"  # Default for work, education, volunteer, projects
    if section_name == "awards":
        date_field = "date"
    elif section_name == "publications":
        date_field = "releaseDate"
    elif section_name == "certificates":
        date_field = "date"
    elif section_name in ["skills", "languages", "interests", "references"]:
        # These sections typically don't have dates, so keep original order
        return section_entries
    
    section_entries.sort(key=lambda x: x.get(date_field, ''), reverse=True)
    
    return section_entries

def build_resume():
    """Build the complete resume JSON structure."""
    # Load basics section
    basics = load_basics()
    
    # Load other sections using the generic function
    work = load_section("work")
    volunteer = load_section("volunteer")
    education = load_section("education")
    awards = load_section("awards")
    certificates = load_section("certificates")
    publications = load_section("publications")
    skills = load_section("skills")
    languages = load_section("languages")
    interests = load_section("interests")
    references = load_section("references")
    projects = load_section("projects")
    
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
    if awards:
        resume["awards"] = awards
    if certificates:
        resume["certificates"] = certificates
    if publications:
        resume["publications"] = publications
    if skills:
        resume["skills"] = skills
    if languages:
        resume["languages"] = languages
    if interests:
        resume["interests"] = interests
    if references:
        resume["references"] = references
    if projects:
        resume["projects"] = projects
    
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
        if resume.get("awards"):
            sections.append("awards")
        if resume.get("certificates"):
            sections.append("certificates")
        if resume.get("publications"):
            sections.append("publications")
        if resume.get("skills"):
            sections.append("skills")
        if resume.get("languages"):
            sections.append("languages")
        if resume.get("interests"):
            sections.append("interests")
        if resume.get("references"):
            sections.append("references")
        if resume.get("projects"):
            sections.append("projects")
        
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
