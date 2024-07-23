import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import ast


df = pd.read_csv('/Users/Kranthi_1/NLP_Reviewer_Puzzle/NLP_Reviewer_Puzzle/data/output/processed_pdf_data.csv')


# Function to convert string representation of list to a numpy array
def convert_to_array(embedding_str):
    embedding_list = ast.literal_eval(embedding_str)
    return np.array(embedding_list)


# Function to calculate cosine similarity between two vectors
def calculate_cosine_similarity(vec1, vec2):
    vec1 = vec1.reshape(1, -1)
    vec2 = vec2.reshape(1, -1)
    similarity = cosine_similarity(vec1, vec2)[0][0]
    return similarity


# Function to normalize the dimensions of embeddings
def normalize_embedding_dimension(vec, target_dim):
    current_dim = vec.shape[0]
    if current_dim < target_dim:
        # Pad with zeros if current dimension is less than target dimension
        padding = np.zeros(target_dim - current_dim)
        vec = np.concatenate((vec, padding), axis=0)
    elif current_dim > target_dim:
        # Truncate if current dimension is greater than target dimension
        vec = vec[:target_dim]
    return vec


# Function to calculate cosine similarity matrix for embeddings
def calculate_cosine_similarity_matrix(data_column):
    num_documents = len(data_column)
    similarity_matrix = np.zeros((num_documents, num_documents))

    # Determine the target dimension based on the first embedding
    target_dim = len(convert_to_array(data_column.iloc[0]))

    for i in range(num_documents):
        for j in range(num_documents):
            vec1 = normalize_embedding_dimension(convert_to_array(data_column.iloc[i]), target_dim)
            vec2 = normalize_embedding_dimension(convert_to_array(data_column.iloc[j]), target_dim)
            similarity_matrix[i, j] = calculate_cosine_similarity(vec1, vec2)

    return similarity_matrix


# Example usage with your DataFrame column (replace 'word_embeddings_introduction' with your actual column name)
cosine_similarity_introduction = calculate_cosine_similarity_matrix(df['word_embeddings_introduction'])

# Convert the similarity matrix to a DataFrame for better readability
cosine_similarity_df = pd.DataFrame(cosine_similarity_introduction, index=df['file_name'], columns=df['file_name'])


# Find the most similar pairs
def find_most_similar_pairs(similarity_df, top_n=5):
    # Create a list to store the most similar pairs
    similar_pairs = []

    # Iterate through the DataFrame to find the most similar pairs
    for i in range(len(similarity_df)):
        for j in range(i + 1, len(similarity_df)):
            similar_pairs.append((similarity_df.index[i], similarity_df.columns[j], similarity_df.iat[i, j]))

    # Sort the pairs by similarity score in descending order
    similar_pairs = sorted(similar_pairs, key=lambda x: x[2], reverse=True)

    # Return the top N most similar pairs
    return similar_pairs[:top_n]


# Get the top 5 most similar pairs
most_similar_pairs = find_most_similar_pairs(cosine_similarity_df, top_n=5)

# Print the most similar pairs
for pair in most_similar_pairs:
    print(f"Document 1: {pair[0]}, Document 2: {pair[1]}, Similarity: {pair[2]}")

# Optional: Save the similarity DataFrame to a CSV file for further analysis
cosine_similarity_df.to_csv('/Users/Kranthi_1/NLP_Reviewer_Puzzle/NLP_Reviewer_Puzzle/data/output/cosine_similarity_introduction.csv')
