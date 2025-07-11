# Daniel Polanco - Resume

Automated resume built with JSON Resume and GitHub Actions.

## 🌐 Live Resume

- **Hosted**: [registry.jsonresume.org/danpolanco](https://registry.jsonresume.org/danpolanco)
- **Raw JSON**: [registry.jsonresume.org/danpolanco.json](https://registry.jsonresume.org/danpolanco.json)
- **Gist**: [gist.github.com/danpolanco/e0092caaa6d853193d2a6f69125c13dd](https://gist.github.com/danpolanco/e0092caaa6d853193d2a6f69125c13dd)

## 🏗️ Structure

```text
src/resume/
├── basics.json          # Personal info, contact, summary
├── work/                # Work experience (one file per job)
├── education/           # Education history
├── skills/              # Technical skills
├── projects/            # Notable projects
├── publications/        # Publications
├── awards/              # Awards and achievements
├── languages/           # Language proficiency
└── interests/           # Personal interests
```

## 🔧 Local Development

```bash
# Build resume locally
cd src
python build.py

# View built resume
cat ../build/resume.json | jq .

# Test build process
./scripts/test-build.sh

# Test gist setup (requires your token)
./scripts/test-gist-setup.sh YOUR_GIST_TOKEN e0092caaa6d853193d2a6f69125c13dd
```

## 🛠️ Environment Setup

```bash
# Update conda environment with GitHub CLI
conda env update -f environment.yaml

# Activate environment
conda activate danpolanco_about
```

## 🚀 Automation

GitHub Actions automatically:

- Builds resume when source files change
- Validates JSON structure
- Publishes to GitHub Gist using GitHub CLI
- Comments on PRs with preview info

### Required Secrets

For the workflow to function, set these repository secrets:

- `GIST_TOKEN`: Personal Access Token with `gist` scope
- `GIST_ID`: Your gist ID (e.g., `e0092caaa6d853193d2a6f69125c13dd`)

### Workflow Triggers

- Push to `main` branch
- Pull requests modifying resume content
- Changes to `src/resume/**` or `src/build.py`

## 📝 Making Changes

1. Edit files in `src/resume/`
2. Test locally: `cd src && python build.py`
3. Commit and push changes
4. Resume automatically publishes to [registry.jsonresume.org/danpolanco](https://registry.jsonresume.org/danpolanco)

## 🎨 Theme

Current theme: **macchiato**

To change theme, edit `src/resume/basics.json`:

```json
{
  "meta": {
    "theme": "macchiato"
  }
}
```

Available themes: [jsonresume.org/themes](https://jsonresume.org/themes)
