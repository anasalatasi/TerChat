#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

rm -rvf messages.db

# Install requirements
pip install -r requirements.txt

# Run the server
python server/server.py
