# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Project structure normalization
- Comprehensive test suite with pytest
- Code formatting with Black and isort
- CONTRIBUTING.md with contribution guidelines
- CHANGELOG.md following Keep a Changelog format
- LICENSE file (MIT License)
- .gitignore file for Python projects
- PyTest configuration with coverage reporting
- Development dependencies in pyproject.toml

## [1.0.2] - 2025-05-20

### Added
- Initial version of DeepSeek CLI
- Basic chat functionality
- Spell checking mode (-s/--spell)
- Translation mode (-t/--trans)
- Version flag (-v/--version)
- Color output toggle (-nc/--no-color)
- API key configuration via environment variable (DEEPSEEK_API_KEY)
- Base URL configuration via environment variable (DEEPSEEK_BASE_URL)
- Model configuration via environment variable (DEEPSEEK_MODEL)
- Log file configuration via environment variable (DEEPSEEK_LOG_FILE)
- Efficient streaming output with color highlighting
- Code block detection and syntax highlighting
- ANSI escape sequence handling
- Performance optimizations (precompiled regex, efficient text processing)

### Changed

### Deprecated

### Removed

### Fixed

### Security

[Unreleased]: https://github.com/deepseek-ai/ds-cli/compare/v1.0.2...HEAD
[1.0.2]: https://github.com/deepseek-ai/ds-cli/releases/tag/v1.0.2
