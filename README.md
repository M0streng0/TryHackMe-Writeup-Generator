# TryHackMe Writeup Generator

This Python script allows you to easily generate writeups for TryHackMe challenges. You can create structured Markdown writeups for your tasks and questions, making it simple to document your solutions and findings. The script even offers the flexibility to choose the save location for your writeup.

**Features:**
- Quickly generate TryHackMe challenge writeups in Markdown format.
- Create organized sections for each task and its associated questions.
- Choose your preferred save location for the generated writeup.

Feel free to use this tool to streamline your TryHackMe writeup creation process and share your solutions with the community.

## Installation

To get started with TryHackMe Writeup Generator, you can follow these simple installation steps:

### Prerequisites

- **Python 3**: Make sure you have Python 3 installed. You can download it from [python.org](https://www.python.org/downloads/).

- **pip3**: Ensure you have the `pip3` package manager installed. It is usually included with Python 3.

### Installation Script

1. Clone this repository to your local machine or download it as a ZIP archive.

2. Open a terminal or command prompt.

3. Navigate to the project directory.

4. Run the following bash script to create a virtual environment and install the required Python libraries:

   ```bash
   ./install.sh
   ```

## Usage

To run the TryHackMe Writeup Generator program, follow these steps:

1. Open a terminal or command prompt.

2. Navigate to the project directory.

3. Activate the virtual environment by running:

   ```bash
   source writeup_generator/bin/activate
   ```

4. Run the main script by executing:

   ```python
   python3 writeup_generator.py
   ```

   This will start the TryHackMe Writeup Generator interface.

5. You will be asked for a TryHackMe URL, simply copy-paste the url and press enter (example: https://tryhackme.com/room/introtooffensivesecurity)

6. To exit the virtual environment when you're done, simply run:

   ```bash
   deactivate
   ```

## Contributing

I welcome contributions from the community! If you have any ideas, improvements, or bug fixes to share, please feel free to submit a pull request. For major changes, please open an issue first to discuss the proposed changes.