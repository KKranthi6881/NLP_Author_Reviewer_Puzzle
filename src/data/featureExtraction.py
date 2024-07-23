import pandas as pd
import numpy as np
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer

# Load spaCy model
nlp = spacy.load('en_core_web_sm')


def tfidf_vectorization(data):
    # Ensure the data is in string format and remove any empty strings
    data = data.apply(lambda x: ' '.join(x) if isinstance(x, list) else x)
    data = data.replace('', np.nan).dropna()

    # TF-IDF Vectorization with error handling
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    try:
        tfidf_matrix = tfidf_vectorizer.fit_transform(data)
    except ValueError as e:
        if "empty vocabulary" in str(e):
            print(f"Warning: Empty vocabulary encountered in data. Skipping TF-IDF vectorization for this data.")
            return pd.DataFrame()
        else:
            raise
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())
    return tfidf_df


def get_word_embeddings(text):
    # Ensure the text is a string
    if not isinstance(text, str):
        return np.zeros(300)  # Return a zero vector for non-string inputs
    # Pre-trained Word Embeddings (GloVe)
    doc = nlp(text)
    embeddings = np.array([token.vector for token in doc if not token.is_stop and token.is_alpha])
    return embeddings.mean(axis=0) if embeddings.any() else np.zeros(300)  # 300-dimensional vector


def word_embeddings(data):
    # Apply word embeddings extraction
    word_embeddings = data.apply(get_word_embeddings)
    return word_embeddings


def get_sentence_embeddings(text):
    # Ensure the text is a string
    if not isinstance(text, str):
        return np.zeros(300)  # Return a zero vector for non-string inputs
    # Sentence Embeddings
    doc = nlp(text)
    return doc.vector


def sentence_embeddings(data):
    # Apply sentence embeddings extraction
    sentence_embeddings = data.apply(get_sentence_embeddings)
    return sentence_embeddings
