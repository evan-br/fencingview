# FencingView Documentation Index

This directory contains detailed documentation about FencingView development, architecture, and releases.

## Quick Links

- **[ARCHITECTURE.md](./ARCHITECTURE.md)** — System design and layered pipeline explanation
- **[CODE_REVIEW.md](./CODE_REVIEW.md)** — v0.0.1 code review findings and recommendations
- **[RELEASE_GUIDE.md](./RELEASE_GUIDE.md)** — Step-by-step PyPI release checklist
- **[REVISION_SUMMARY.md](./REVISION_SUMMARY.md)** — Summary of v0.0.1 revisions

## For Users

If you want to **use FencingView**, start here:
1. Read [../README.md](../README.md) — Main project overview
2. Run [../examples/demo_analysis.py](../examples/demo_analysis.py) — See it in action
3. Check [../examples/README.md](../examples/README.md) — Usage examples and tutorials

## For Developers

If you're contributing or extending FencingView:
1. Review [ARCHITECTURE.md](./ARCHITECTURE.md) — Understand the 3-layer pipeline
2. Check [CODE_REVIEW.md](./CODE_REVIEW.md) — Known issues and TODOs
3. Read source docstrings in `src/fencingview/`

## For Maintainers

If you're publishing a new version:
1. Follow [RELEASE_GUIDE.md](./RELEASE_GUIDE.md) — Release checklist
2. Update version in `pyproject.toml`
3. Review [REVISION_SUMMARY.md](./REVISION_SUMMARY.md) — Track changes

---

## File Descriptions

### ARCHITECTURE.md
Technical deep-dive into FencingView's design:
- 3-layer pipeline: Vision → Scouting → Match
- MediaPipe pose extraction and coordinate transformation
- Movement tracking and pose classification algorithms
- Generator-based processing for memory efficiency

### CODE_REVIEW.md
Comprehensive v0.0.1 code review:
- Critical issues fixed for PyPI release
- Known limitations and TODOs for v0.1.0+
- Recommendations for future improvements
- Type hints, logging, and testing roadmap

### RELEASE_GUIDE.md
Complete PyPI release process:
- Prerequisites and validation steps
- Local build and testing
- TestPyPI and official PyPI publication
- Troubleshooting common errors

### REVISION_SUMMARY.md
Summary of changes and improvements:
- Files modified and why
- New documentation and structure
- Build and packaging setup
- Performance and quality notes

---

## Version History

- **v0.0.1** (Current) — Alpha release
  - YOLO person detection + MediaPipe pose
  - Basic movement and pose classification
  - Generator-based frame processing
  - PyPI-ready packaging

- **v0.1.0** (Planned)
  - Type hints (PEP 484)
  - Improved logging
  - Unit tests
  - Better pose classification

---

## Contributing

To contribute to FencingView:
1. Fork the repository
2. Create a feature branch
3. Read architecture docs
4. Follow code style from existing files
5. Add docstrings and tests
6. Submit a pull request

---

Last updated: November 22, 2025
