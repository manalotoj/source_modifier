from setuptools import setup, find_packages
import os

print("Detected packages:", find_packages(where="src"))

# Load runtime dependencies from src/source_modifier/requirements.txt
runtime_requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
try:
    with open(runtime_requirements_path) as f:
        runtime_install_requires = f.read().splitlines()
except FileNotFoundError:
    runtime_install_requires = []

setup(
    name="source_modifier",
    version="0.1.1",
    author="Manalotoj",
    author_email="mail@mail.com",
    description="A Python script to modify source code.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/manalotoj/source_modifier",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "source_modifier=source_modifier.main:main",
        ],
    },
)

