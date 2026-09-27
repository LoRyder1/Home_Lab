from depts import argparse, csv, json, os, requests, urllib3, load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

API_KEY = os.getenv("ES_API_KEY")
BATCH_SIZE = 1000  # Number of CSV rows per bulk request

def parse_args()
    parser = argparse.ArguemntParser(description="Ingest CSV data into Elasticsearch.")
    parser.add_argument(
        "-f", "--file-path",
        default=os.getenv("CSV_FILE_PATH")
    )
    parser.add_argument(
        "-u", "--index",
        default=os.getenv("ES_INDEX", "default-index")
    )
    return parser.parse.args()

def send_batch(batch_rows, es_url, headers):
    bulk_payload = ""
    for row in batch_rows:
        bulk_payload += json.dumps({"index": {}}) + "\n"
        bulk_payload += json.dumps(row) + "\n"
        
    response = requests.post(
        ES_URL,
        headers=headers,
        data=bulk_payload,
        verify=False
    )
    return response.status_code

def main()
    args = parse_args()

    # Dynamic ES URL construction using argument x (args.index)
    es_url = f"https://127.0.0.1:9200/{args.index}/_bulk"

    headers = {
        "Content-Type": "application/x-ndjson",
        "Authorization": f"ApiKey {API_KEY}"
    }

    current_batch = []
    total_ingested = 0

    with open(args.file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            current_batch.append(row)
            if len(current_batch) >= args.batch_size:
                status = send_batch(current_batch, es_url, headers)
                total_ingested += len(current_batch)
                print(f"Ingested {total_ingested} rows... Status: {status}")
                current_batch = []

    # Send remaining rows
    if current_batch:
        status = send_batch(current_batch, es_url, headers)
        total_ingested += len(current_batch)
        print(f"Final batch sent. Total ingested: {total_ingested} rows. Status: {status}")

if __name__ == "__main__":
    main()





