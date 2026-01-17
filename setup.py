"""Setup script for Kaizen Blitz application."""

from setuptools import setup, find_packages

setup(
    name="kaizen-blitz",
    version="1.0.0",
    description="Desktop application for managing Kaizen Blitz rapid improvement projects",
    author="Your Company",
    author_email="info@yourcompany.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "PyQt6>=6.6.1",
        "PyQt6-Charts>=6.6.0",
        "SQLAlchemy>=2.0.23",
        "reportlab>=4.0.7",
        "python-docx>=1.1.0",
        "openpyxl>=3.1.2",
        "matplotlib>=3.8.2",
        "seaborn>=0.13.0",
        "Pillow>=10.1.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
        ],
    },
    entry_points={
        "console_scripts": [
            "kaizen-blitz=kaizen_blitz.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
