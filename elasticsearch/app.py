from crawler.elasticsearch.app import Elasticsearch
from elasticsearch.helpers import bulk
import pandas as pd

# Load the CSV file into a pandas DataFrame
df = pd.read_csv("database_official_postprocessed.csv")

# Initialize Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# Create an index for the laptop products
index_name = "laptops"
es.indices.create(index=index_name, ignore=400)

# Define a function to prepare data for bulk indexing
def create_indexing_data(df):
    for _, row in df.iterrows():
        yield {
            "_op_type": "index",
            "_index": index_name,
            "_source": row.to_dict()
        }

# Bulk index the laptop products into Elasticsearch
bulk(es, create_indexing_data(df))

# Define a function to search for relevant laptop products
def search_laptops(query, top_k=5):
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["Tên sản phẩm", "Bộ VXL", "Bộ nhớ RAM", "Ổ cứng", "Card màn hình", "Kích thước màn hình",
                           "Cổng giao tiếp", "Hệ điều hành", "Kích thước", "Màu sắc", "Chất liệu"],
            }
        }
    }

    # Search using Elasticsearch
    response = es.search(index=index_name, body=body, size=top_k)

    # Extract and return the relevant laptops
    hits = response['hits']['hits']
    relevant_laptops = [hit['_source'] for hit in hits]

    return relevant_laptops

# Example usage:
user_query = "laptop for gaming"
top_k_results = search_laptops(user_query, top_k=3)
print(top_k_results)
