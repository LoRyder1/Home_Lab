# Elasticsearch CSV Bulk Ingestion Tool

A lightweight, modular Python utility for parsing CSV files, converting records into NDJSON format, and bulk-ingesting them into an Elasticsearch instance (such as Security Onion).

## Features

- **CLI-Driven File Selection:** Specify target CSV files dynamically via command-line arguments.
- **Environment Isolation:** Keeps sensitive parameters (API key, Elasticsearch endpoint) secure in `.env` files.
- **NDJSON Format Generation:** Formats documents automatically for the Elasticsearch `_bulk` API.
- **Modular Configuration:** Separates runtime configuration (`config.py`) from main execution logic (`main.py`).

---

## Project Structure

```text
.
├── .env                  # Local environment configuration (Git-ignored)
├── .gitignore            # Excludes secrets, caches, and environment files
├── config.py             # Configuration loader & CLI argument parser
├── main.py               # Ingestion pipeline execution entry point
├── README.md             # Project documentation
