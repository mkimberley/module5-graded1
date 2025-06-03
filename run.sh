#!/bin/bash
source ~/venv/bin/activate

# Run pytest and check its exit status
pytest
if [ $? -eq 0 ]; then
    cd src
    pip install -r requirements.txt
    python3 main.py
else
    echo "Tests failed. Aborting further execution."
    exit 1
fi