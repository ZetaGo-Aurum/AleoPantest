"""Setup script untuk AloPantest"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="AloPantest",
    version="3.0.0",
    author="AloPantest Team",
    author_email="team@alopantest.com",
    description="Modern Penetration Testing Framework with TUI and Automation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZetaGo-Aurum/AleoPantest",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
    ],
    python_requires=">=3.8",
    install_requires=[
        'click>=8.0',
        'rich>=13.0',
        'requests>=2.25',
        'beautifulsoup4>=4.9',
        'pydantic>=2.0',
        'pyyaml>=6.0',
        'textual>=0.48.0',
    ],
    entry_points={
        'console_scripts': [
            'aleopantest=alo_pantest.cli:main',
        ],
    },
)
