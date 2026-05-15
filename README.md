# Intelligent Log Analyzer

A comprehensive log analysis system with anomaly detection, RAG, and LLM capabilities.

## Features

- Log ingestion and parsing
- Anomaly detection
- Incident management
- RAG-based querying
- LLM integration
- Alert system
- Reporting

## Setup

1. Create virtual environment: `python -m venv venv`
2. Activate: `venv\Scripts\activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Configure environment variables in `.env`
5. Run: `python app/main.py`

## Project Structure

- `app/`: Main application code
  - `api/`: API routes and dependencies
  - `core/`: Configuration, database, security, logging
  - `models/`: Data models
  - `schemas/`: Pydantic schemas
  - `services/`: Business logic services
  - `utils/`: Utility functions
- `datasets/`: Data storage
- `vector_store/`: Vector database
- `trained_models/`: Trained ML models
- `logs/`: Application logs
- `tests/`: Unit tests