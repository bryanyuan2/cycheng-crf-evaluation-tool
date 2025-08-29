#!/usr/bin/env python3
"""
Setup script for CRF Evaluation Tool.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="crf-evaluation-tool",
    version="2.0.0",
    author="bryanyuan2",
    author_email="bryanyuan2@gmail.com",
    description="A tool for evaluating CRF (Conditional Random Field) test results with confusion matrix analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bryanyuan2/crf-evaluation-tool",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        # No external dependencies for now
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
        ],
    },
    entry_points={
        "console_scripts": [
            "crf-eval=main:main",
        ],
    },
)
