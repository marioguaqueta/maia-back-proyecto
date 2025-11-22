#!/bin/bash

# Start Wildlife Detection System

echo "=================================="
echo "🦁 Wildlife Detection System"
echo "=================================="
echo ""
echo "Starting backend and frontend..."
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3."
    exit 1
fi

# Check if required packages are installed
if ! python3 -c "import flask" &> /dev/null; then
    echo "⚠️  Flask not found. Installing dependencies..."
    pip3 install -r requirements.txt
fi

echo "🚀 Starting Flask backend (port 8000)..."
python3 app.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

echo "🌐 Starting Streamlit frontend (port 8501)..."
streamlit run streamlit_app.py &
STREAMLIT_PID=$!

echo ""
echo "=================================="
echo "✅ System Started!"
echo "=================================="
echo ""
echo "🌐 Streamlit UI:  http://localhost:8501"
echo "🔌 Flask API:     http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop both services"
echo "=================================="
echo ""

# Wait for both processes
wait $BACKEND_PID $STREAMLIT_PID

