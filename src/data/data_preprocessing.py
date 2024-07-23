import warnings
from urllib3.exceptions import NotOpenSSLWarning
import pandas as pd
import spacy
import re
import ast

# Suppress specific warnings
warnings.filterwarnings("ignore", category=NotOpenSSLWarning)

# Load spaCy model
nlp = spacy.load('en_core_web_sm')


def clean_author_name(authors):
    clean_names = []
    for author_list in authors:
        try:
            author_list = ast.literal_eval(author_list)
            for author in author_list:
                # Use spaCy to identify and extract PERSON entities
                doc = nlp(author)
                for ent in doc.ents:
                    if ent.label_ == 'PERSON':
                        clean_author = ent.text
                        clean_author = re.sub(r'\d+', '', clean_author).strip()
                        clean_author = re.sub(r'[^\w\s]', '', clean_author)  # Remove special characters
                        clean_author = re.sub(r'\s+', ' ', clean_author)  # Normalize whitespace
                        if clean_author and len(clean_author.split()) > 1:  # Ensure it's a name with at least two words
                            clean_names.append(clean_author)
        except (ValueError, SyntaxError):
            continue
    return clean_names


def clean_text(text):
    if pd.isna(text):
        return " "
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)
    return text.strip()


def preprocess_text(text):
    if pd.isna(text):
        return " "
    # Convert to lowercase and apply spaCy processing
    doc = nlp(text.lower())

    # Remove stopwords, perform lemmatization, and remove punctuation
    words = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]

    # Reconstruct text from tokens
    return ' '.join(words)


def preprocess_data(df):
    # Clean authors
    df['clean_authors'] = df['authors'].apply(lambda x: clean_author_name([x]))

    # Clean and preprocess abstract and introduction
    df['clean_abstract'] = df['abstract'].apply(lambda x: preprocess_text(clean_text(x)))
    df['clean_introduction'] = df['introduction'].apply(lambda x: preprocess_text(clean_text(x)))

    return df







