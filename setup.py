from setuptools import setup, find_packages

setup(
    name="source_modifier",  # Replace with your application name
    version="0.1.0",
    author="manalotoj",
    author_email="mail@mail.com",
    description="A tool to perform file replacement by text or by json path.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/manalotoj/source_modifier",  # Project URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Minimum Python version
    install_requires=open("requirements.txt").read().splitlines(),  # Dependencies
    entry_points={
        "console_scripts": [
            "source_modifier=source_modifier.main:main",  # CLI command
        ],
    },
)
