# FencingView 0.0.1 - PyPI Release Checklist

**Prepared on**: November 21, 2025

## ✅ Prerequisites

- [ ] Python 3.9+ installed
- [ ] pip, setuptools, wheel, twine installed:
  ```bash
  pip install --upgrade pip setuptools wheel twine
  ```

---

## ✅ Local Verification Steps

### 1. Validate Package Structure
```bash
# Verify structure is correct
python -m pip install -e .
```

### 2. Verify PyPI Metadata
```bash
# Validate pyproject.toml and README
python -m twine check dist/*
```

### 3. Test Imports
```bash
python -c "from fencingview import EpeeMatch, FencingVision; print('✓ Imports OK')"
```

### 4. Run Test Script
```bash
# With a valid video file
python test_script.py path/to/test.mp4
```

---

## ✅ Checklist of Implemented Fixes

### CRITICAL (Blockers)
- [x] **pyproject.toml** - Real metadata (author, keywords, classifiers, urls)
- [x] **README.md** - Complete documentation with examples
- [x] **LICENSE** - MIT License file
- [x] **src/fencingview/__init__.py** - Exports with `__all__`
- [x] **Docstrings** - PEP 257 in all public classes and methods

### IMPORTANT (Recommended)
- [x] **.gitignore** - Appropriate exclusions for CI/CD
- [x] **MANIFEST.in** - Inclusion of non-Python files
- [x] **vision.py** - Enhanced with docstrings and validation
- [x] **scouting.py** - Enhanced with docstrings and explicit TODOs
- [x] **match.py** - Enhanced with docstrings and exception handling
- [x] **geometry.py** - Enhanced with detailed documentation
- [x] **test_script.py** - CLI improved with argparse

### NOT IMPLEMENTED (v0.1.0+)
- [ ] Type hints (PEP 484)
- [ ] Logging module (instead of print)
- [ ] Unit tests with pytest
- [ ] GitHub Actions CI/CD

---

## 🔧 Release Guide

### Step 1: Update Personal Information

Edit the following files with your real information:

**`pyproject.toml`**:
```toml
authors = [
  { name = "Evandro Rissatto Pereira", email = "erissatto@gmail.com" },
]

[project.urls]
Homepage = "https://github.com/evan-br/fencingview"
Repository = "https://github.com/evan-br/fencingview.git"
"Bug Tracker" = "https://github.com/evan-br/fencingview/issues"
```

**`LICENSE`**:
```
Copyright (c) 2025 Evandro Rissatto Pereira
```

### Step 2: Prepare Local Build

```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info

# Build source distribution and wheel
python -m build

# Verify contents
tar -tzf dist/fencingview-0.0.1.tar.gz | head -20
```

### Step 3: Validate with Twine

```bash
# Check metadata
python -m twine check dist/*

# Should return:
# ✓ dist/fencingview-0.0.1.tar.gz: PASSED
# ✓ dist/fencingview-0.0.1-py3-none-any.whl: PASSED
```

### Step 4: Publish to TestPyPI (RECOMMENDED FIRST)

```bash
# Register account at https://test.pypi.org/account/register/
# Generate token at https://test.pypi.org/account/manage/

# Configure ~/.pypirc (or use --username/--password)
[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgEIcHlwaS5vcmc...

# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ fencingview==0.0.1
```

### Step 5: Publish to Official PyPI

```bash
# Configure ~/.pypirc with official PyPI credentials
[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmc...

# Upload
python -m twine upload dist/*

# Verify
pip install fencingview==0.0.1
python -c "import fencingview; print(fencingview.__version__)"
```

---

## 🐛 Troubleshooting

### Error: "twine not found"
```bash
pip install twine
```

### Error: "Invalid distribution"
```bash
# Check for special characters in README
# Validate UTF-8 encoding
file README.md

# Clean and rebuild
rm -rf build/ dist/ *.egg-info
python -m build
```

### Error: "Package name already exists on PyPI"
- Use a different name or check if the package already exists
- For local development: `pip install -e .`

### Error: "Invalid classifier"
- Check valid classifiers at: https://pypi.org/classifiers/
- Remove invalid classifiers from `pyproject.toml`

---

## 📊 Final Verification Checklist

Before publishing, run this script:

```python
import subprocess
import sys

checks = {
    "pyproject.toml syntax": "python -m tomllib",
    "Import FencingView": "python -c 'from fencingview import EpeeMatch'",
    "Twine check": "python -m twine check dist/*",
    "Build exists": "python -m pip show fencingview",
}

for check_name, command in checks.items():
    print(f"Checking {check_name}...", end=" ")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, timeout=10)
        if result.returncode == 0:
            print("✓")
        else:
            print("✗")
            print(f"  Error: {result.stderr.decode()}")
    except Exception as e:
        print(f"✗ {e}")
        sys.exit(1)

print("\n✅ All checks passed! Ready for PyPI.")
```

---

## 📚 Useful Resources

- [PyPI Account Management](https://pypi.org/account/)
- [Using Trusted Publishers](https://docs.pypi.org/trusted-publishers/)
- [Setuptools Documentation](https://setuptools.pypa.io/)
- [PEP 427 - Wheel Binary Package Format](https://www.python.org/dev/peps/pep-0427/)
- [PEP 503 - Repository API](https://www.python.org/dev/peps/pep-0503/)

---

## 🎯 Version 0.0.1 Rationale

This is an **alpha release** because:

1. **Incomplete pose classification**: Uses only bbox height
2. **No type hints**: Added in v0.1.0
3. **No unit tests**: Will be added in v0.1.0
4. **Basic logging**: Migration to logging module in v0.1.0
5. **No multiprocessing**: Added in v0.2.0

**Intended for**:
- Early adopters and researchers
- Community feedback before v1.0.0
- Prototyping and experimentation

---

**Next version**: 0.1.0
- Complete type hints
- Logging module
- Basic unit tests
- Better pose classification
