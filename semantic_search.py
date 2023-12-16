import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the CSV file into a pandas DataFrame
df = pd.read_csv("laptops.csv")

# Combine the relevant columns into a single text column
df["text"] = df["Tên sản phẩm"] + " " + df["Bộ VXL"] + " " + df["Bộ nhớ RAM"] + " " + df["Ổ cứng"] + " " + df["Card màn hình"] + df[""]

# Initialize the TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer()

# Compute the TF-IDF matrix
tfidf_matrix = tfidf_vectorizer.fit_transform(df["text"])

# Function to retrieve relevant products using TF-IDF
def retrieve_products_tfidf(query):
    # Transform the query using the TF-IDF vectorizer
    query_vector = tfidf_vectorizer.transform([query])

    # Compute the cosine similarity between the query and all laptops
    similarity_scores = cosine_similarity(query_vector, tfidf_matrix).flatten()

    # Sort the laptops based on similarity scores in descending order
    sorted_indices = similarity_scores.argsort()[::-1]

    # Retrieve all laptops with non-zero similarity scores
    relevant_laptops = df.iloc[sorted_indices][similarity_scores > 0]

    return relevant_laptops

# Example usage
query = "Máy tính Laptop HP"
relevant_laptops = retrieve_products_tfidf(query)

print("Relevant Laptops:")
print(relevant_laptops)