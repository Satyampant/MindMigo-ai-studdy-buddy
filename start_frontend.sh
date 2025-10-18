#!/bin/bash
echo "Starting Studdy Buddy AI Frontend..."
echo "====================================="
cd "$(dirname "$0")/frontend"
echo ""
echo "Frontend running at: http://localhost:8080"
echo "Backend should be at: http://localhost:8000"
echo ""
python -m http.server 8080
