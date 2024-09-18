#!/bin/bash

cd server

# Run server tests with verbose output
python -m unittest discover -v server -p "test_*.py"

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "All tests passed successfully!"
    exit 0
else
    echo "Some tests failed. Please check the output above."
    exit 1
fi
