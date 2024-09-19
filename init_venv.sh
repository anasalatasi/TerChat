#!/bin/bash

# Function to create virtual environment
create_venv() {
    if command -v python3 &> /dev/null; then
        echo "Creating virtual environment with python3..."
        python3 -m venv venv
    elif command -v python &> /dev/null; then
        echo "Python3 not found. Creating virtual environment with python..."
        python -m venv venv
    else
        echo "Error: Neither python3 nor python is available. Please install Python and try again."
        exit 1
    fi
}

# Check if venv module is available
if ! python3 -m venv --help &> /dev/null && ! python -m venv --help &> /dev/null; then
    echo "venv module not found. Please install it and try again."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    create_venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
source venv/bin/activate

echo "Virtual environment is now active."

