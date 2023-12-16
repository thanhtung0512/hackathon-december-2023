import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import normalize
from rank_bm25 import BM25Okapi
import re

# Load the CSV file into a pandas DataFrame
df = pd.read_csv("laptops.csv")

# Combine all relevant columns into a single text column
df["text"] = df.apply(lambda row: ' '.join(row.dropna().astype(str)), axis=1)

# Function to convert "x triệu" to "x.000.000đ"
def convert_currency(text):
    pattern = r"(\d+) triệu"
    match = re.search(pattern, text)
    if match:
        million_value = int(match.group(1))
        converted_value = million_value * 1000000
        return text.replace(match.group(0), f"{converted_value:,}đ")
    return text

# Apply the currency conversion to the text column
df["text"] = df["text"].apply(convert_currency)

# Initialize the vectorizers
tfidf_vectorizer = TfidfVectorizer()
count_vectorizer = CountVectorizer()

# Fit and transform the text data
tfidf_matrix = tfidf_vectorizer.fit_transform(df["text"])
count_matrix = count_vectorizer.fit_transform(df["text"])

# Normalize the count matrix
normalized_count_matrix = normalize(count_matrix)

# Compute the similarity scores using cosine similarity
tfidf_similarity_scores = pairwise_distances(tfidf_matrix, metric="cosine")
count_similarity_scores = pairwise_distances(normalized_count_matrix, metric="cosine")

# Initialize the BM25F model
bm25f_model = BM25Okapi(df["text"].apply(str.split))

# Function to retrieve relevant products using TF-IDF
def retrieve_products_tfidf(query, top_k=5):
    query_vector = tfidf_vectorizer.transform([query])
    similarity_scores = pairwise_distances(query_vector, tfidf_matrix, metric="cosine")
    top_indices = similarity_scores.argsort()[0][:top_k]
    return df.iloc[top_indices]

# Function to retrieve relevant products using BM25F
def retrieve_products_bm25f(query, top_k=5):
    tokenized_query = query.split()
    similarity_scores = bm25f_model.get_scores(tokenized_query)
    top_indices = similarity_scores.argsort()[-top_k:][::-1]
    return df.iloc[top_indices]

# Example usage
query = "Máy tính giá khoảng 15 triệu?"
tfidf_results = retrieve_products_tfidf(query)
bm25f_results = retrieve_products_bm25f(query)

print("Results using TF-IDF:")
print(tfidf_results)

print("\nResults using BM25F:")
print(bm25f_results)