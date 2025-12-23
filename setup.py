"""
Taskly - Moniteur Système Moderne
Installation et configuration du package.
"""
from setuptools import setup, find_packages
from pathlib import Path

# Lire le README pour la description longue
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="taskly",
    version="1.1.0",
    author="Axel G",
    author_email="",  # À remplir si souhaité
    description="Un moniteur système moderne avec interface Apple-style",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/axel-g-dev/Taskly",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: System :: Monitoring",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "flet>=0.28.0",
        "psutil>=5.9.0",
    ],
    entry_points={
        "console_scripts": [
            "taskly=main:main",
        ],
    },
    include_package_data=True,
    keywords="system monitor activity taskly macos performance cpu ram network",
    project_urls={
        "Bug Reports": "https://github.com/axel-g-dev/Taskly/issues",
        "Source": "https://github.com/axel-g-dev/Taskly",
        "Documentation": "https://github.com/axel-g-dev/Taskly/blob/main/docs/DOCUMENTATION.md",
    },
)
