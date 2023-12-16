import pandas as pd
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_distances
import torch
import numpy as np

# Load the CSV file into a pandas DataFrame
df = pd.read_csv("laptops.csv")

# Combine the relevant columns into a single text column
df["text"] = df["Tên sản phẩm"] + " " + df["Bộ VXL"] + " " + df["Bộ nhớ RAM"] + " " + df["Ổ cứng"] + " " + df["Card màn hình"]

# Initialize the BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained("bert-base-multilingual-cased")
model = BertModel.from_pretrained("bert-base-multilingual-cased")

# Function to retrieve relevant products using BERT embeddings
def retrieve_products_bert(query, top_k=7):
    # Tokenize the query
    query_tokens = tokenizer.encode(query, add_special_tokens=True, truncation=True, max_length=128)

    # Encode the query into a fixed-dimensional vector
    query_embedding = model(torch.tensor([query_tokens]))[0][0].detach().numpy()

    # Encode the laptop descriptions into fixed-dimensional vectors
    laptop_embeddings = []
    for text in df["text"]:
        laptop_tokens = tokenizer.encode(text, add_special_tokens=True, truncation=True, max_length=128)
        laptop_embedding = model(torch.tensor([laptop_tokens]))[0][0].detach().numpy()
        laptop_embeddings.append(laptop_embedding)

    # Flatten the laptop_embeddings list
    laptop_embeddings = np.array(laptop_embeddings)

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
relevant_laptops = retrieve_products_bert(query, top_k=7)

print("Relevant Laptops:")
print(relevant_laptops)