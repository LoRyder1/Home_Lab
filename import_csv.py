# Purpose of this script is to parse csv that is stored locally and import into SIEM
# use SIEM to analyze data! Better than using Timeline Explorer in Windows
# Used API Key


# ES | QL  - elastic search query language to find timestomped anomalies 
# FROM so-i30-windows-update
# | WHERE Btime IS NOT NULL AND Mtime IS NOT NULL
# | WHERE Btime > Mtime
# | KEEP Name, FullPath, Btime, Mtime, Ctime, Size
# | LIMIT 100 

# Export variable in your shell - API Key
# export ES_API_KEY="YOUR_ENCODED_API_KEY_HERE"

import csv
import json
import argparse
import os
import requests
import urllib3
from dotenv import load_dotenv

# Disable SSL warnings for self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load env variables from .env file
load_dotenv()

# Set up CLI argument parser
parser = argparse.ArgumentParser(description="Ingest CSV into Elasticsearch.")
parser.add_argument(
    "-f", "--file",
    type=str,
)

args = parser.parse_args()

CSV_FILE_PATH = args.file


# Best for local development, not production
API_KEY = os.getenv("ES_API_KEY")
ES_URL = os.getenv("ES_URL")


# Validate required variables are loaded
missing_vars = [var_name for var_name, var_val in [
    ("ES_API_KEY", API_KEY),
    ("CSV_FILE_PATH", CSV_FILE_PATH),
    ("ES_URL", ES_URL)
] if not var_val]

if missing_vars:
    raise ValueError(f"Missing required environment variable(s) in .env: {', '.join(missing_vars)}")


headers = {
    "Content-Type": "application/x-ndjson",
    "Authorization": f"ApiKey {API_KEY}"
}


bulk_data = ""
with open(CSV_FILE_PATH, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Action metadata header
        bulk_data += json.dumps({"index": {}}) + "\n"
        # Document payload
        bulk_data += json.dumps(row) + "\n"

# Send bulk request to local Elasticsearch
response = requests.post(
    ES_URL,
    headers=headers,
    data=bulk_data,
    verify=False
)

print(f"Status Code: {response.status_code}")
print(response.text[:200]) # Print response preview


