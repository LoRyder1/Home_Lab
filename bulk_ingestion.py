import pandas as pd
from elasticsearch import Elasticsearch, helpers

# 1. Initialize client (Update with host, API key, or basic auth)
es = Elasticsearch(
    "https://localhost:9200",
    api_key="YOUR_API_KEY",
    verify_certs=False  # Adjust for production SSL
)

INDEX_NAME = "my-csv-index"

def generate_docs(csv_path, chunksize=1000):
    for chunk in pd.read_csv(csv_path, chunksize=chunksize):
        # Clean/transform data if necessary
        chunk = chunk.where(pd.notnull(chunk), None)
        
        for record in chunk.to_dict(orient="records"):
            yield {
                "_index": INDEX_NAME,
                "_source": record
            }

def main():
    csv_file_path = "data.csv"
    
    # Bulk ingest using helper function
    success_count, errors = helpers.bulk(
        es, 
        generate_docs(csv_file_path),
        chunk_size=1000,
        request_timeout=60
    )
    print(f"Successfully indexed {success_count} documents.")

if __name__ == "__main__":
    main()