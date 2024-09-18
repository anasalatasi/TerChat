#!/bin/bash

# Run pytest with coverage for server tests
pytest server/test_server.py --cov=server -v

# Generate coverage report
coverage report -m

# Check if tests passed and coverage is above threshold
# if [ $? -eq 0 ]; then
#     coverage_percentage=$(coverage report | grep TOTAL | awk '{print $NF}' | sed 's/%//')
#     if (( $(echo "$coverage_percentage >= 80" | bc -l) )); then
#         echo "All tests passed and coverage is above 80%!"
#         exit 0
#     else
#         echo "Tests passed but coverage is below 80%. Current coverage: $coverage_percentage%"
#         exit 1
#     fi
# else
#     echo "Some tests failed. Please check the output above."
#     exit 1
# fi

