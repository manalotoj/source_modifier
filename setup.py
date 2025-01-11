from setuptools import setup, find_packages
import os

# Load runtime dependencies from src/requirements.txt
requirements_path = os.path.join(os.path.dirname(__file__), "src", "requirements.txt")
try:
    with open(requirements_path) as f:
        install_requires = f.read().splitlines()
except FileNotFoundError:
    install_requires = []  # Fallback to no dependencies


# Load build dependencies (e.g., setuptools, wheel) from requirements-dev.txt
requirements_path = os.path.join(os.path.dirname(__file__), "requirements-dev.txt")
try:
    with open(requirements_path) as f:
        install_requires = f.read().splitlines()
except FileNotFoundError:
    install_requires = []  # Fallback to no dependencies

setup(
    name="source_modifier",
    version="0.1.0",
    author="Manalotoj",
    author_email="mail@mail.com",
    description="A Python script to modify source code.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/manalotoj/source_modifier",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.7",
    install_requires=install_requires,  # Runtime dependencies
    setup_requires=["setuptools>=42", "wheel"],      # Build dependencies from requirements-dev.txt
    entry_points={
        "console_scripts": [
            "source_modifier=source_modifier.main:main",
        ],
    },
)
