#!/bin/bash

# Quick start script for Automated Diagnostic System

echo "=========================================="
echo "Automated Diagnostic System - Quick Start"
echo "=========================================="
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed successfully"
echo ""

# Run tests
echo "🧪 Running tests..."
cd tests
python3 test_diagnostic_engine.py
TEST_RESULT=$?
cd ..

if [ $TEST_RESULT -eq 0 ]; then
    echo "✓ All tests passed!"
else
    echo "⚠️ Some tests failed, but continuing..."
fi

echo ""
echo "=========================================="
echo "🚀 Starting server..."
echo "=========================================="
echo ""
echo "Access the application at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
cd backend
python3 app.py
