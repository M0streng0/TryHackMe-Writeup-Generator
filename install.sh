#!/bin/bash
set -e  # Exit immediately if any command fails

# Check if Python is available
if ! command -v python3 &>/dev/null; then
    echo "Python is required but not installed. Aborting."
    exit 1
fi

# Check if 'requirements.txt' file exists
if [ ! -f "requirements.txt" ]; then
    echo "'requirements.txt' file not found. Aborting."
    exit 1
fi

# Check if the virtual environment is already activated
if [ -n "$VIRTUAL_ENV" ]; then
    echo "A Python virtual environment is already activated. Deactivate it before running this script."
    exit 1
fi

# Create a Python virtual environment
python3 -m venv writeup_generator

# Activate the virtual environment
source writeup_generator/bin/activate

# Install Python requirements using pip
if pip3 install -r requirements.txt; then
    echo "All Python requirements have been successfully installed."
else
    echo "Failed to install Python requirements. Please check the error messages."
    deactivate  # Deactivate the virtual environment in case of failure
    exit 1
fi

# Deactivate the virtual environment
deactivate
