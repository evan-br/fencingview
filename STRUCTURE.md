# FencingView Project Structure

This document describes the organized project structure for FencingView v0.0.1+

## Directory Layout

```
fencingview/
├── src/                           # Python source code (installable package)
│   └── fencingview/
│       ├── __init__.py           # Package exports
│       ├── epee/
│       │   ├── vision.py         # YOLO + MediaPipe detection
│       │   ├── scouting.py       # Movement & pose classification
│       │   └── match.py          # Pipeline orchestration
│       └── common/
│           └── geometry.py       # Helper functions
│
├── examples/                      # Usage examples and demos
│   ├── demo_analysis.py          # Quick-start analysis script
│   └── README.md                 # How to run examples
│
├── docs/                         # Developer documentation
│   ├── INDEX.md                  # Documentation index
│   ├── CODE_REVIEW.md            # v0.0.1 code review
│   ├── CODE_REVIEW_PT_BR.md      # Portuguese version
│   ├── ARCHITECTURE.md           # System design
│   ├── RELEASE_GUIDE.md          # PyPI release steps
│   └── REVISION_SUMMARY.md       # Changes & improvements
│
├── .github/                      # GitHub-specific files
│   └── copilot-instructions.md   # AI assistant guidelines
│
├── pyproject.toml               # Package metadata (PEP 518)
├── MANIFEST.in                  # Non-Python files to include
├── README.md                    # Main project documentation
├── LICENSE                      # MIT License
├── .gitignore                   # Git exclusions
├── test_script.py               # (DEPRECATED - use examples/demo_analysis.py)
└── STRUCTURE.md                 # This file
```

## Key Files

### Package Root
- **`pyproject.toml`** - Project metadata, dependencies, build config
- **`README.md`** - Main documentation (users start here)
- **`LICENSE`** - MIT License text
- **`.gitignore`** - Git exclusions (*.pt, *.mp4, .venv, etc)
- **`MANIFEST.in`** - Include non-Python files in distribution

### Source Code (`src/`)
- **`src/fencingview/__init__.py`** - Package initialization and exports
- **`src/fencingview/epee/`** - Fencing-specific modules
- **`src/fencingview/common/`** - Shared utilities

### Examples & Demos (`examples/`)
- **`examples/demo_analysis.py`** - Quick demo script
- **`examples/README.md`** - Usage tutorials and advanced examples

### Documentation (`docs/`)
- **`docs/INDEX.md`** - Start here for developers
- **`docs/CODE_REVIEW.md`** - Code analysis and recommendations
- **`docs/RELEASE_GUIDE.md`** - How to publish to PyPI

### GitHub Integration (`.github/`)
- **`.github/copilot-instructions.md`** - Guidelines for AI assistants

---

## What to Keep vs. Remove

### ✅ Keep in Repository
```
src/fencingview/          # Core package
examples/                 # Demo scripts
docs/                     # Documentation
pyproject.toml           # Metadata
README.md                # Main docs
LICENSE                  # License
.gitignore               # Git config
MANIFEST.in              # Build config
.github/                 # GitHub config
```

### ❌ Remove or Move to .gitignore
```
*.pt                     # YOLO models (auto-download)
*.mp4 / *.avi / *.mov   # Video files (user-provided)
dist/                    # Build artifacts
build/                   # Build artifacts
*.egg-info/              # Build artifacts
__pycache__/             # Python cache
.venv/                   # Virtual environment
test_script.py           # (renamed to examples/demo_analysis.py)
START_HERE.md            # Redundant
```

---

## Installation & Usage

### Development Install
```bash
# From project root
pip install -e .
```

### Run Demo
```bash
# From project root
python examples/demo_analysis.py
python examples/demo_analysis.py path/to/video.mp4
python examples/demo_analysis.py --no-preview video.mp4
```

### PyPI Installation
```bash
pip install fencingview
```

---

## File Organization Rationale

### Why `/src/fencingview/`?
- Separates source from build artifacts
- Prevents accidental imports from wrong location
- Matches Python packaging best practices

### Why `/examples/`?
- Clear separation: demo code vs. production code
- Easy to exclude from builds if needed
- Users know where to find usage examples

### Why `/docs/`?
- Centralizes all documentation
- Easy to exclude from package distribution
- Separate from user-facing README

### Why keep `.github/copilot-instructions.md`?
- Guides AI assistants (like Copilot) in this repo
- Helpful for maintainers and contributors
- No storage impact (text file, tiny size)

---

## Transitioning from Old Structure

If you have the old layout:

```bash
# Remove old files from root
rm test_script.py                    # → use examples/demo_analysis.py
rm REVIEW_0.0.1.md                 # → see docs/CODE_REVIEW.md
rm REVISION_SUMMARY_0.0.1.md       # → see docs/REVISION_SUMMARY.md
rm PYPI_RELEASE_CHECKLIST.md       # → see docs/RELEASE_GUIDE.md
rm DOCUMENTATION_INDEX.md          # → see docs/ARCHITECTURE.md
rm REVISAO_PT_BR.md                # → see docs/CODE_REVIEW_PT_BR.md
rm START_HERE.md                   # → redundant with README.md

# The new files/dirs are created:
# - examples/demo_analysis.py       ← Renamed from test_script.py
# - examples/README.md              ← New demos documentation
# - docs/                           ← New directory with all docs
# - docs/INDEX.md                   ← Navigation hub
```

---

## Future Structure (v0.1.0+)

Recommended additions:

```
fencingview/
├── tests/                        # Unit tests (pytest)
│   ├── test_vision.py
│   ├── test_scouting.py
│   └── test_match.py
│
├── .github/workflows/            # CI/CD pipelines
│   ├── tests.yml                # Run tests on push
│   └── publish.yml              # Publish to PyPI
│
└── notebooks/                    # Jupyter tutorials (optional)
    └── getting_started.ipynb
```

---

## Build & Distribution

- **Source distribution**: `dist/fencingview-X.Y.Z.tar.gz`
- **Binary distribution**: `dist/fencingview-X.Y.Z-py3-none-any.whl`
- **Metadata**: `src/fencingview.egg-info/`

These are auto-generated by `python -m build` and should be in `.gitignore`.

---

**Version**: v0.0.1  
**Last updated**: November 22, 2025
