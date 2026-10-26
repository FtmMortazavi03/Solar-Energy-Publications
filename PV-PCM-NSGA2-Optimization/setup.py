"""
File: setup.py
Author: Fatemehsadat Mortazavi
Date: Aug 2026
Description: Package setup configuration for PV-PCM-NSGA2-Optimization.
"""

from setuptools import setup, find_packages

setup(
    name="pv-pcm-nsga2",
    version="1.0.0",
    author="Fatemehsadat Mortazavi",
    description="Multi-objective optimization of PV-PCM systems using NSGA-II for hot and dusty climates in Iran",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "matplotlib>=3.7.0",
        "scipy>=1.11.0",
        "pymoo>=0.6.0",
    ],
)