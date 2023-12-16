import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_distances

# Load the CSV file into a pandas DataFrame
df = pd.read_csv("laptops-hp-240.csv")

# Combine the relevant columns into a single text column
df["text"] = df.apply(lambda row: ' '.join(row.dropna().astype(str)), axis=1)

# Initialize the BERT-based sentence transformer
model = SentenceTransformer("bert-base-nli-mean-tokens")

# Encode the laptop descriptions into fixed-dimensional vectors
laptop_embeddings = model.encode(df["text"].tolist())

# Function to retrieve relevant products using BERT embeddings
def retrieve_products_bert(query, top_k=7):
    # Encode the query into a fixed-dimensional vector
    query_embedding = model.encode([query])[0]

    # Compute the cosine distances between the query and all laptop embeddings
    distances = cosine_distances([query_embedding], laptop_embeddings).flatten()

    # Sort the laptops based on distance scores in ascending order
    sorted_indices = distances.argsort()

    # Retrieve the top k laptops with the lowest distance scores
    top_indices = sorted_indices[:top_k]

    # Retrieve the relevant laptops based on the top indices
    relevant_laptops = df.iloc[top_indices]

    return relevant_laptops

# Example usage
query = "Máy tính giá khoảng 15 triệu"
relevant_laptops = retrieve_products_bert(query, top_k=20)

print("Relevant Laptops:")
print(relevant_laptops)