# config.py
from pathlib import Path
import argparse
import os
import urllib3
from dotenv import load_dotenv

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


ENV_PATH = Path(__file__).resolve().parent / ".env"
# Load environment configuration
load_dotenv(dotenv_path=ENV_PATH)

def get_env_config():
    """Retrieve validated environment settings."""
    config = {
        "API_KEY": os.getenv("ES_API_KEY"),
        "ES_URL": os.getenv("ES_URL")
    }
    
    missing = [k for k, v in config.items() if not v]
    if missing:
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        
    return config

def parse_args():
    """Handle command-line arguments."""
    parser = argparse.ArgumentParser(description="Ingest CSV to Elasticsearch.")
    parser.add_argument(
        "-f", "--file",
        type=str,
        required=True,
        help="Path to CSV file to ingest"
    )
    return parser.parse_args()