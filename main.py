# main.py
import csv
import json
import requests
import urllib3
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

CSV_FILE_PATH = os.getenv("CSV_FILE_PATH")
ES_URL = os.getenv("ES_URL")
API_KEY = os.getenv("ES_API_KEY")

headers = {
    "Content-Type": "application/x-ndjson",
    "Authorization": f"ApiKey {API_KEY}"
}

BATCH_SIZE = 1000  # Number of CSV rows per bulk request
current_batch = []
total_ingested = 0

def send_batch(batch_rows):
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

with open(CSV_FILE_PATH, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        current_batch.append(row)
        if len(current_batch) >= BATCH_SIZE:
            status = send_batch(current_batch)
            total_ingested += len(current_batch)
            print(f"Ingested {total_ingested} rows... Status: {status}")
            current_batch = []

# Send remaining rows
if current_batch:
    status = send_batch(current_batch)
    total_ingested += len(current_batch)
    print(f"Final batch sent. Total ingested: {total_ingested} rows. Status: {status}")