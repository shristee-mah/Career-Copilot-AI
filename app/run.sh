#!/bin/bash
# Career Copilot AI - Streamlit App Launcher

echo ""
echo "================================================"
echo "  Career Copilot AI - Streamlit Application"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

# Check if streamlit is installed
if ! python -m pip show streamlit &> /dev/null; then
    echo "Installing required packages..."
    python -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies"
        exit 1
    fi
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo ""
    echo "Warning: .env file not found!"
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "Please edit .env and add your Google API Key"
    echo "Then run this script again"
    exit 0
fi

# Run the Streamlit app
echo ""
echo "Starting Career Copilot AI..."
echo ""
python -m streamlit run app.py
