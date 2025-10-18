#!/bin/bash
echo "Starting Studdy Buddy AI Backend..."
echo "====================================="
cd "$(dirname "$0")"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
