"""
File: setup.py
Author: Fatemehsadat Mortazavi
Date: Jun 2026
Description: Package setup configuration for PV-PCM-Iran.
"""

from setuptools import setup, find_packages

setup(
    name="pv-pcm-iran",
    version="1.0.0",
    author="Fatemehsadat Mortazavi",
    description="Simulation of PV panel cooling with PCM in hot climates of Iran",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "matplotlib>=3.7.0",
        "scipy>=1.11.0",
    ],
)