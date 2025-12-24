"""Setup script untuk AloPantest"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="AloPantest",
    version="1.0.0",
    author="AloPantest Team",
    author_email="team@alopantest.com",
    description="Comprehensive Penetration Testing Framework with 350+ Tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alopantest/alopantest",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
        "Topic :: System :: Networking",
        "Topic :: Security",
    ],
    python_requires=">=3.8",
    install_requires=[
        'click>=8.0',
        'rich>=10.0',
        'requests>=2.25',
        'beautifulsoup4>=4.9',
    ],
    entry_points={
        'console_scripts': [
            'alopantest=alo_pantest.cli:cli',
        ],
    },
)
