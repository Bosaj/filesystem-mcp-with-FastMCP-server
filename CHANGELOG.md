# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

There are no tagged releases in this repository yet, so all history is recorded under [Unreleased].

## [Unreleased]

### Added
- `README.md` rewritten to accurately describe the implemented FastMCP server, Streamlit host, and MCP connector, including an explicit "Not implemented" note for the PDF resource / health-check tool referenced only in code comments.
- `LICENSE` (MIT).
- `docs/wiki-draft/` with Home, Getting Started, Architecture, and FAQ pages (draft content for the GitHub Wiki).
- `.github/workflows/ci.yml`: lightweight CI running `python -m py_compile` and a critical-errors-only `flake8` pass on every push and pull request.
- Workspace notes and sample data (`workspace/mcp/notes.txt`), example env port update, `.pyc` ignore rule (2025-12-29, Bosaj).
- MCP presentation slides, `MCP presntations.pptx` (2025-12-31, Yassine Ben Acha).

### Security
- No committed secrets were found in the tracked files or the full git history of this repository. `.env` is git-ignored; only `.env.example` (placeholder value) is tracked.

### Changed
- Initial project scaffold, README, and `.gitignore` history (2025-12-28 to 2025-12-29, Abdellatif Chakor / chakorabdellatif).
