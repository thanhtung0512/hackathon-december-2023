from flask import Flask, request, jsonify
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_distances
from pyvi.ViTokenizer import tokenize

app = Flask(__name__)

# Load the CSV file into a pandas DataFrame
df = pd.read_csv("database_official_postprocessed.csv")

# Combine the relevant columns into a single text column
df["text"] = df["Tên sản phẩm"] + " " + df["Bộ VXL"] + " " + df["Bộ nhớ RAM"] + " " + df["Giá niêm yết"] + " " + df["Giá ưu đãi tháng 12"] + " " + df["Bảo hành"]

# Initialize the BERT-based sentence transformer
model = SentenceTransformer("keepitreal/vietnamese-sbert")

# model = SentenceTransformer("VoVanPhuc/sup-SimCSE-VietNamese-phobert-base")

# Encode the laptop descriptions into fixed-dimensional vectors
laptop_embeddings = model.encode(df["text"].tolist())

@app.route("/search", methods=["GET"])
def search_products():
    query = request.args.get("query")
    top_k = int(request.args.get("top_k", 5))

    # Function to retrieve relevant products using BERT embeddings
    def retrieve_products_bert(query, top_k=5):
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

    relevant_laptops = retrieve_products_bert(query, top_k)
    results = relevant_laptops.to_dict(orient="records")

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)