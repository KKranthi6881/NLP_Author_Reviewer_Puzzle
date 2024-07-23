import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import ast


df = pd.read_csv('/Users/Kranthi_1/NLP_Reviewer_Puzzle/NLP_Reviewer_Puzzle/data/output/processed_pdf_data.csv')


df1 = pd.read_csv('/Users/Kranthi_1/NLP_Reviewer_Puzzle/NLP_Reviewer_Puzzle/data/output/cosine_similarity_introduction.csv')

pd.options.display.width= None
pd.options.display.max_columns= None
pd.set_option('display.max_rows', 3000)
pd.set_option('display.max_columns', 3000)
print(df1)





