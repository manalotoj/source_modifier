from setuptools import setup, find_packages

# Load runtime dependencies from src/requirements.txt
with open("src/requirements.txt") as f:
    install_requires = f.read().splitlines()

# Load build dependencies (e.g., setuptools, wheel) from requirements-dev.txt
with open("requirements-dev.txt") as f:
    build_requires = f.read().splitlines()

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
    setup_requires=build_requires,      # Build dependencies from requirements-dev.txt
    entry_points={
        "console_scripts": [
            "source_modifier=src.main:main",
        ],
    },
)
