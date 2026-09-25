# main.py
import csv
import json
import requests
from config import get_env_config, parse_args

# Load config and CLI arguments
config = get_env_config()
args = parse_args()

# CSV path originates exclusively from CLI arguments
CSV_FILE_PATH = args.file

headers = {
    "Content-Type": "application/x-ndjson",
    "Authorization": f"ApiKey {config['API_KEY']}"
}

bulk_data = ""
with open(CSV_FILE_PATH, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Action metadata header
        bulk_data += json.dumps({"index": {}}) + "\n"
        # Document payload
        bulk_data += json.dumps(row) + "\n"

# Send bulk request to Elasticsearch
response = requests.post(
    config["ES_URL"],
    headers=headers,
    data=bulk_data,
    verify=False
)

print(f"Status Code: {response.status_code}")
print(response.text[:200])