

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
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Config settings
CSV_FILE_PATH = "/mnt/storage_fast/G_Labs_anti_forensics/I30-windows-update.csv"
ES_URL = "https://127.0.0.1:9200/so-i30-windows-update/_bulk"



# Fetch from OS environment
# not best eventually want to use a better maintable way to handle API Keys
API_KEY = os.environ.get("ES_API_KEY")



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


