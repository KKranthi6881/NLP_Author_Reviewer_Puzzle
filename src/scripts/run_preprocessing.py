import os
import pandas as pd
import numpy as np
from src.data.data_pdfExtract import process_directory
from src.data.data_preprocessing import preprocess_data
from src.data.featureExtraction import tfidf_vectorization, word_embeddings, sentence_embeddings

# Directory containing PDFs
pdf_directory = '/Users/Kranthi_1/NLP_Reviewer_Puzzle/NLP_Reviewer_Puzzle/data/raw/Dataset'

# Extract information from all PDFs in the directory and subdirectories
data = process_directory(pdf_directory)

# Create a DataFrame
df = pd.DataFrame(data)

# Save to CSV
output_directory = '/Users/Kranthi_1/NLP_Reviewer_Puzzle/NLP_Reviewer_Puzzle/data/output'
os.makedirs(output_directory, exist_ok=True)
output_path = os.path.join(output_directory, 'extracted_pdf_data.csv')
df.to_csv(output_path, index=False)
print(f"Data saved to {output_path}")

# Reload the DataFrame from CSV for further processing (optional if not already in memory)
df = pd.read_csv(output_path)

# Preprocess data
df = preprocess_data(df)

# Ensure the 'clean_authors', 'clean_introduction', and 'clean_abstract' columns are properly formatted
#df['clean_authors'] = df['clean_authors'].apply(lambda x: ' '.join(x) if isinstance(x, list) else x).fillna('')
df['clean_introduction'] = df['clean_introduction'].apply(lambda x: ' '.join(x) if isinstance(x, list) else x).fillna('')
df['clean_abstract'] = df['clean_abstract'].apply(lambda x: ' '.join(x) if isinstance(x, list) else x).fillna('')

# Apply TF-IDF vectorization
try:
    df_tfidf_introduction = tfidf_vectorization(df['clean_introduction']).add_prefix('tfidf_intro_')
    df_tfidf_abstract = tfidf_vectorization(df['clean_abstract']).add_prefix('tfidf_abstract_')
    df_tfidf_authors = tfidf_vectorization(df['authors']).add_prefix('tfidf_authors_')
except ValueError as e:
    print(f"Error in TF-IDF vectorization: {e}")

# Apply word embeddings and store them in separate columns
df['word_embeddings_introduction'] = word_embeddings(df['clean_introduction']).apply(lambda x: x.tolist())
df['word_embeddings_abstract'] = word_embeddings(df['clean_abstract']).apply(lambda x: x.tolist())
df['word_embeddings_authors'] = word_embeddings(df['authors']).apply(lambda x: x.tolist())

# Apply sentence embeddings and store them in separate columns
df['sentence_embeddings_introduction'] = sentence_embeddings(df['clean_introduction']).apply(lambda x: x.tolist())
df['sentence_embeddings_abstract'] = sentence_embeddings(df['clean_abstract']).apply(lambda x: x.tolist())
df['sentence_embeddings_authors'] = sentence_embeddings(df['authors']).apply(lambda x: x.tolist())
'''
# Concatenate all the results into the original DataFrame
df_features = pd.concat([
    df,
    df_tfidf_introduction,
    df_tfidf_abstract,
    df_tfidf_authors
], axis=1)
'''
# Save the final DataFrame
final_output_path = os.path.join(output_directory, 'processed_pdf_data.csv')
df.to_csv(final_output_path, index=False)
print(f"Final data saved to {final_output_path}")

print(df.head())
