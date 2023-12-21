from flask import Flask, request, jsonify
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_distances
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restful import Resource, Api
from tiktoken import get_encoding
tokenizer = get_encoding("cl100k_base")
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)
# Load the CSV file into a pandas DataFrame
df = pd.read_csv("database_official_postprocessed_final.csv")

# Combine the relevant columns into a single text column
df["text"] = (
    df["Tên sản phẩm"]
    + " "
    + df["Bộ VXL"]
    + " "
    + df["Bộ nhớ RAM"]
    + " "
    + df["Giá niêm yết"]
    + " "
    + df["Giá ưu đãi tháng 12"]
    + " "
    + df["Bảo hành"]
)

# Initialize the BERT-based sentence transformer
model = SentenceTransformer("keepitreal/vietnamese-sbert")

# Set your OpenAI GPT-3 API key
openai.api_key = "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"

# Encode the laptop descriptions into fixed-dimensional vectors
laptop_embeddings = model.encode(df["text"].tolist())

# Initialize an empty conversation string
conversation_history = ""


@app.route("/search", methods=["POST"])
def search_products():
    global conversation_history  # Declare conversation_history as a global variable

    # Get the user's query from the POST request
    data = request.get_json()
    user_query = data.get("query")
    top_k = int(data.get("top_k", 5))

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

    # Retrieve relevant laptops based on the user's query
    relevant_laptops = retrieve_products_bert(user_query, top_k)
    results = relevant_laptops.to_dict(orient="records")

    # Add user query and relevant products to the conversation history
    conversation_history += f"User: {user_query}"

    # Use OpenAI GPT-3 to generate a response based on the conversation history
    prompt = f" you are chatbot for answer user query in choosing laptops based, retrieve information from relevant products i gave you.\n Relevant products: {jsonify(results)}\nConversation History:\n{conversation_history}\n"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
                "role": "user",
                "content": f"You are an assistant designed to answer user queries and help them choose the best-fit laptops based on relevant products related to their questions i gave you later. You have the ability to retrieve information from the relevant products I provide. Additionally, you can ask users for further details to better understand their requirements if the initial information is not clear. Response as markdown.\n Relevant products: {(results)}\n User query: {user_query}",
            },
        ],
        max_tokens=1000,  # Adjust max_tokens as needed
    )
    print("Relevant product:", (results))
    print("History chat:", conversation_history)

    # Extract the generated response from OpenAI GPT-3
    gpt_response = response["choices"][0]["message"]["content"]

    # Add GPT-3 response to the conversation history
    conversation_history += f"Assistant: {gpt_response}\n"

    return jsonify({"results": results, "gpt_response": gpt_response})


if __name__ == "__main__":
    app.run(host="192.168.1.211", port=5000, debug=True)
