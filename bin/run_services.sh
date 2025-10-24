#!/bin/bash

set -e

echo "Starting services..."

# Start FastAPI in background
echo "Starting FastAPI on port 8001..."
uv run uvicorn src.web_service.main:app --host 0.0.0.0 --port 8001 &

sleep 3

# Start Streamlit
echo "Starting Streamlit on port 8501..."
uv run streamlit run src/web_service/streamlit_app.py --server.port 8501 --server.address 0.0.0.0
