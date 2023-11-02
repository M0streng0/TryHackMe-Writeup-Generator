#!/bin/bash
# Check if 'python3' command is available
command -v python3 >/dev/null 2>&1 || { echo >&2 "Python 3 is required but it's not installed. Aborting."; exit 1; }

# Check if 'requirements.txt' file exists
if [ ! -f "requirements.txt" ]; then
    echo "'requirements.txt' file not found. Aborting."
    exit 1
fi

# Create a Python virtual environment
python3 -m venv writeup_generator

# Activate the virtual environment
source writeup_generator/bin/activate

# Install Python 3 requirements using pip3
pip3 install -r requirements.txt

# Check the installation status
if [ $? -eq 0 ]; then
    echo "All Python 3 requirements have been successfully installed."
else
    echo "Failed to install Python 3 requirements. Please check the error messages."
fi

# Deactivate the virtual environment
deactivate