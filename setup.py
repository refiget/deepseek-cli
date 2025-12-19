from setuptools import setup, find_packages
from pathlib import Path

# Read the version from version.py
version_path = Path(__file__).parent / "ds" / "version.py"
with open(version_path, "r") as f:
    exec(f.read())

# Minimal setup.py for compatibility with both setuptools and pyproject.toml
setup(
    name="ds-cli",
    version=__version__,
    packages=find_packages(),
    # Most configuration is now in pyproject.toml
)

