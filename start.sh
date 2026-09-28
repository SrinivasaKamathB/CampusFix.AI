#!/usr/bin/env bash
# CampusFix AI Quick Launch Script

set -e
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"

echo "=========================================================="
echo "🚀 Launching CampusFix AI Platform"
echo "   Visual Campus Maintenance & Resolution Intelligence"
echo "=========================================================="

cd "$BACKEND_DIR"

# Initialize & verify database
python3 test_api.py

echo ""
echo "✨ Starting Server on http://localhost:8000 ..."
echo "👉 Open http://localhost:8000 in your browser to demo the app!"
echo "=========================================================="

exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
