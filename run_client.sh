#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install requirements
pip install -r requirements.txt

# Run the client
python client/client.py
