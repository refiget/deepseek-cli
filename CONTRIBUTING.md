# Contributing to DeepSeek CLI

Thank you for considering contributing to the DeepSeek CLI project! This document provides guidelines for contributing to this project.

## Code of Conduct

We are committed to fostering an open and welcoming environment. All contributors are expected to adhere to the following code of conduct:

- Be respectful and inclusive
- Listen actively and consider different viewpoints
- Accept constructive criticism gracefully
- Focus on what's best for the community and the project
- Avoid personal attacks or derogatory comments

## How to Contribute

### Reporting Issues

If you encounter a bug or have a feature request, please create an issue in the project repository:

1. Check if the issue already exists
2. If it doesn't exist, create a new issue with:
   - A clear and descriptive title
   - A detailed description of the issue or feature request
   - Steps to reproduce the bug (if applicable)
   - Expected behavior
   - Actual behavior
   - Screenshots or error messages (if applicable)
   - Your environment (Python version, OS, etc.)

### Pull Requests

We welcome pull requests for bug fixes, improvements, and new features:

1. Fork the repository
2. Create a new branch for your changes
3. Make your changes with clear, descriptive commit messages
4. Test your changes thoroughly
5. Update documentation if necessary
6. Create a pull request with:
   - A clear description of the changes
   - Reference to any related issues
   - Explanation of the implementation (if complex)

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ds-cli.git
   cd ds-cli
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the package in development mode with all dependencies:
   ```bash
   pip install -e .[dev]
   ```

## Coding Standards

### Code Style

- We use [Black](https://black.readthedocs.io/) for code formatting
- We use [isort](https://pycqa.github.io/isort/) for import sorting
- Follow Python's [PEP 8](https://peps.python.org/pep-0008/) style guide

Run the following commands to ensure your code follows the style guidelines:

```bash
black ds/
tests/
isort ds/
tests/
```

### Import Guidelines

- Group imports: standard library first, then third-party, then local
- Use absolute imports for local modules
- Avoid wildcard imports (`from module import *`)

## Testing

### Running Tests

Run the test suite with pytest:

```bash
pytest
```

Run tests with coverage report:

```bash
pytest --cov=ds --cov-report=term-missing
```

### Writing Tests

- Write tests for all new functionality
- Use descriptive test names
- Test both positive and negative cases
- Keep tests focused and isolated
- Use fixtures for common test setup

### Test Structure

```
tests/
├── test_config.py       # Tests for configuration module
├── test_utils.py        # Tests for utility functions
├── test_chat.py         # Tests for chat functionality
└── test_translation.py  # Tests for translation functionality
```

## Documentation

### Updating Documentation

- Update the README.md if you change:
  - Installation instructions
  - Usage examples
  - Command-line options

- Update docstrings for new functions or changes to existing functions

### Docstring Style

Use Google-style docstrings:

```python
def function_name(param1, param2):
    """Description of the function.
    
    Args:
        param1 (type): Description of param1
        param2 (type): Description of param2
    
    Returns:
        type: Description of the return value
    
    Raises:
        ExceptionType: Description of when the exception is raised
    """
    # Function implementation
```

## Release Process

1. Update the CHANGELOG.md with the new version and changes
2. Update the version in `ds/__init__.py`
3. Run tests to ensure everything works correctly
4. Create a release in the repository
5. Upload to PyPI

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

Thank you for your contributions!
