import os
import shutil

# Path to the root directory to be deleted and recreated
root_directory = 'Author_Reviewer_Puzzle'

# Function to delete the directory
def delete_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        print(f"Deleted directory: {path}")
    else:
        print(f"Directory does not exist: {path}")

# Function to create the new directory structure and files
def create_directory_structure():
    # Define the folder structure
    folders = [
        "NLP_Reviewer_Puzzle/data/raw",
        "NLP_Reviewer_Puzzle/data/processed",
        "NLP_Reviewer_Puzzle/data/external",
        "NLP_Reviewer_Puzzle/data/interim",
        "NLP_Reviewer_Puzzle/data/output",
        "NLP_Reviewer_Puzzle/notebooks",
        "NLP_Reviewer_Puzzle/src/data",
        "NLP_Reviewer_Puzzle/src/models",
        "NLP_Reviewer_Puzzle/src/utils",
        "NLP_Reviewer_Puzzle/src/scripts",
        "NLP_Reviewer_Puzzle/tests"
    ]

    # Define the files to be created with their initial content
    files = {
        "NLP_Reviewer_Puzzle/.gitignore": """
data/raw/*
data/interim/*
data/processed/*
data/output/*
*.pyc
__pycache__/
""",
        "NLP_Reviewer_Puzzle/README.md": """
# NLP Reviewer Puzzle

This project involves processing PDF files to extract author names, abstract, and introduction sections for further analysis.

## Folder Structure

- **data/**: Contains all data-related files.
- **notebooks/**: Jupyter notebooks for EDA and prototyping.
- **src/**: Source code for data processing, model training, and utilities.
- **tests/**: Unit tests for the code.
- **README.md**: Project documentation.
- **requirements.txt**: List of Python dependencies.
- **setup.py**: Script for installing the project as a package.

## Setup

1. Clone the repository.
2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm
    ```
3. Run the preprocessing script:
    ```bash
    python src/scripts/run_preprocessing.py
    ```
""",
        "NLP_Reviewer_Puzzle/requirements.txt": """
PyMuPDF
spacy
pandas
""",
        "NLP_Reviewer_Puzzle/setup.py": """
from setuptools import setup, find_packages

setup(
    name='nlp_reviewer_puzzle',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'PyMuPDF',
        'spacy',
        'pandas'
    ],
)
""",
        "NLP_Reviewer_Puzzle/src/data/__init__.py": """
from .data_preprocessing import process_directory, process_pdf
from .extract_text import extract_text_first_pages
from .extract_authors import extract_author_names
from .extract_sections import extract_abstract_and_introduction

__all__ = [
    'process_directory',
    'process_pdf',
    'extract_text_first_pages',
    'extract_author_names',
    'extract_abstract_and_introduction'
]
""",
        "NLP_Reviewer_Puzzle/src/data/data_preprocessing.py": """
import fitz  # PyMuPDF
import spacy
import os

def extract_text_first_pages(file_path, num_pages=3):
    # Function implementation here
    pass

def extract_author_names(text):
    # Function implementation here
    pass

def extract_section(text, section_name, next_section_names):
    # Function implementation here
    pass

def extract_abstract_and_introduction(text):
    # Function implementation here
    pass

def process_pdf(file_path):
    # Function implementation here
    pass

def process_directory(directory):
    # Function implementation here
    pass
""",
        "NLP_Reviewer_Puzzle/src/models/__init__.py": """
# Initialize model-related code if needed
""",
        "NLP_Reviewer_Puzzle/src/utils/__init__.py": """
# Initialize utility-related code if needed
""",
        "NLP_Reviewer_Puzzle/src/scripts/__init__.py": """
# Initialize script-related code if needed
""",
        "NLP_Reviewer_Puzzle/src/scripts/run_preprocessing.py": """
import os
import pandas as pd
from src.data.data_preprocessing import process_directory

# Directory containing PDFs
pdf_directory = '/Users/Kranthi_1/NLP_Reviewer_Puzzle/Dataset/'

# Extract information from all PDFs in the directory and subdirectories
data = process_directory(pdf_directory)

# Create a DataFrame
df = pd.DataFrame(data)

# Save to CSV
output_path = 'data/output/extracted_pdf_data.csv'
df.to_csv(output_path, index=False)

print(f"Data saved to {output_path}")
""",
        "NLP_Reviewer_Puzzle/tests/__init__.py": ""
    }

    # Create the folders
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

    # Create the files with initial content
    for file_path, content in files.items():
        with open(file_path, 'w') as file:
            file.write(content)

    print("Folder structure and files created successfully.")

# Delete the existing directory
delete_directory(root_directory)

# Recreate the directory structure
create_directory_structure()
