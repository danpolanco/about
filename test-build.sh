#!/bin/bash

# Test script for resume build and validation
# Mimics the GitHub Actions workflow locally

set -e

echo "🏗️  Building resume..."
cd src
python build.py

echo ""
echo "✅ Validating JSON..."
cd ..
cat build/resume.json | jq empty
echo "✅ JSON validation passed"

echo ""
echo "📄 Resume Summary:"
echo "   Sections: $(jq -r 'keys | join(", ")' build/resume.json)"
echo "   Name: $(jq -r '.basics.name' build/resume.json)"
echo "   Label: $(jq -r '.basics.label' build/resume.json)"
echo "   Theme: $(jq -r '.basics.meta.theme' build/resume.json)"

echo ""
echo "🎯 Resume ready for publishing!"
echo "📍 Will be available at: https://registry.jsonresume.org/danpolanco"
