import os
import fitz  # PyMuPDF
import pandas as pd

def extract_text_first_pages(file_path, num_pages=3):
    """Extract text from the first few pages of a PDF."""
    try:
        doc = fitz.open(file_path)
        text = ""
        for page_num in range(min(num_pages, doc.page_count)):
            page = doc.load_page(page_num)
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"Error reading the PDF file {file_path}: {e}")
        return ""

def extract_author_names_from_folder(file_path):
    """Extract author names from the subfolder structure under 'Dataset'."""
    try:
        # Extract the author name from the path
        parts = file_path.split(os.sep)
        # Assuming the structure is /path/to/Dataset/author_name/PDF_files.pdf
        # The author name should be the second last part
        author_name = parts[-2]
        return author_name
    except Exception as e:
        print(f"Error extracting author name from {file_path}: {e}")
        return ""

def extract_section(text, section_name, next_section_names):
    """Extract a specific section from the text until the next section name is found."""
    section_start = text.lower().find(section_name.lower())
    if section_start == -1:
        return ""

    # Find the start of the next section to limit the extraction
    section_end = len(text)
    for next_section in next_section_names:
        next_section_start = text.lower().find(next_section.lower(), section_start)
        if next_section_start != -1 and next_section_start < section_end:
            section_end = next_section_start

    return text[section_start:section_end].strip()

def extract_abstract_and_introduction(text):
    """Extract abstract and introduction sections."""
    abstract = extract_section(text, 'abstract', ['introduction', 'methods', 'materials'])
    introduction = extract_section(text, 'introduction', ['methods', 'materials', 'results'])
    return abstract, introduction

def process_pdf(file_path):
    """Process a single PDF to extract authors, abstract, and introduction."""
    print(f"Processing file: {file_path}")
    text = extract_text_first_pages(file_path)
    if not text:
        print(f"No text extracted from {file_path}")
        return "", "", ""

    author_name = extract_author_names_from_folder(file_path)
    abstract, introduction = extract_abstract_and_introduction(text)
    return author_name, abstract, introduction

def process_directory(directory):
    """Recursively process all PDF files in a directory."""
    data = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.pdf'):
                file_path = os.path.join(root, filename)
                author_name, abstract, introduction = process_pdf(file_path)
                data.append({
                    "file_name": filename,
                    "authors": author_name,
                    "abstract": abstract,
                    "introduction": introduction
                })
    return data