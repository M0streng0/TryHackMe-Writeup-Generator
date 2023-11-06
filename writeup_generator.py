#!/usr/bin/env python3
import logging

# Initialize logging
logging.basicConfig(filename='scraping.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
console_handler = logging.StreamHandler()  # Add a handler to log to the terminal
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
console_handler.setFormatter(formatter)
logger = logging.getLogger('')
logger.addHandler(console_handler)

import re
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time

# Configuration
USERNAME = "Henrique Oliveira - M0streng0"
MARKDOWN_FILE_EXTENSION = ".md"
MARKDOWN_FILE_TYPE = [("Markdown Files", "*" + MARKDOWN_FILE_EXTENSION)]

# Function to fetch the challenge page content using Selenium with headless Chrome
def fetch_challenge_page_selenium(challenge_url):
    try:
        # Check if the URL is from TryHackMe
        if not re.match(r'^https://tryhackme\.com', challenge_url):
            logging.error("The provided URL does not appear to be from TryHackMe.")
            return None

        chrome_options = Options()
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(challenge_url)

        # Find all elements with the class "class-link" and wait for a short time
        time.sleep(3)  # Adjust the sleep duration as needed
        topic_elements = driver.find_elements(By.CLASS_NAME, 'class-link')

        for topic_element in topic_elements:
            driver.execute_script("arguments[0].setAttribute('aria-expanded', 'true');", topic_element)

        challenge_html = driver.page_source
        driver.quit()

        return challenge_html
    except WebDriverException as e:
        logging.error(f"Error while fetching challenge page: {e}")
        logging.error("Please make sure the provided URL is valid.")
        return None

# Function to parse the challenge page and extract relevant information
def parse_challenge_page(challenge_html):
    soup = BeautifulSoup(challenge_html, 'html.parser')

    # Extract the challenge title from the HTML title tag
    challenge_title = (soup.find('title').text.strip()).replace("|", "\\|")

    # Extract the tasks
    tasks = []
    task_elements = soup.find_all('div', {'class': 'card-header task-header'})
    for task_element in task_elements:
        task_title = (task_element.find('a', {'class': 'card-link'}).text.strip()).replace(" " * 30, " : ")
        tasks.append({'title': task_title})

    # Extract the questions
    all_questions = []
    for question_elements in soup.find_all('div', {'class': 'card-body task-incomplete'}):
        questions = question_elements.find_all('div', {'class': 'room-task-question-details'})
        task_questions = []
        for question in questions:
            task_questions.append(question.text.strip())
        all_questions.append(task_questions)
    return challenge_title, tasks, all_questions

# Function to generate a markdown writeup
def generate_markdown_writeup(challenge_title, tasks, questions):
    formatted_datetime = datetime.now().strftime("%H:%M %d-%m-%y")
    markdown_writeup = f"{formatted_datetime} \\| {USERNAME}\n\n"
    markdown_writeup += f"# {challenge_title}\n\n"

    for i, task in enumerate(tasks, start=1):
        markdown_writeup += f"## {task['title']}\n"
        task_questions = questions[i - 1]  # Get the questions for the current task
        for j, question in enumerate(task_questions, start=1):
            markdown_writeup += f"### Question {j}\n\n{question}\n\n```\n\n```\n\n> \n\n"

    return markdown_writeup

# Create a simple tkinter window to open a file dialog
def save_file(markdown_writeup):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.asksaveasfilename(initialfile="README", defaultextension=MARKDOWN_FILE_EXTENSION,
                                             filetypes=[("Markdown Files", "*" + MARKDOWN_FILE_EXTENSION)])
    if file_path:
        with open(file_path, "w") as file:
            file.write(markdown_writeup)
        logging.info(f"Markdown writeup saved to: {file_path}")
    else:
        logging.warning("Markdown writeup not saved.")

if __name__ == "__main__":
    try:
        challenge_url = input("Enter the TryHackMe challenge URL: ")
        challenge_html = fetch_challenge_page_selenium(challenge_url)

        if challenge_html:
            challenge_title, tasks, questions = parse_challenge_page(challenge_html)
            markdown_writeup = generate_markdown_writeup(challenge_title, tasks, questions)

            # Ask the user where to save the file
            save_file(markdown_writeup)
    except KeyboardInterrupt:
        logging.info("Script execution interrupted by the user.")