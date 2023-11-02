#!/usr/bin/env python3
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import tkinter as tk
from tkinter import filedialog

# Function to fetch the challenge page content using Selenium
def fetch_challenge_page_selenium(challenge_url):
    driver = webdriver.Chrome()  # Change this to the appropriate driver for your browser
    driver.get(challenge_url)
    
    # Find all elements with the class "class-link" and set aria-expanded to "true"
    topic_elements = driver.find_elements(By.CLASS_NAME, 'class-link')
    for topic_element in topic_elements:
        driver.execute_script("arguments[0].setAttribute('aria-expanded', 'true');", topic_element)
    
    challenge_html = driver.page_source
    driver.quit()
    
    return challenge_html

# Function to parse the challenge page and extract relevant information
def parse_challenge_page(challenge_html):
    soup = BeautifulSoup(challenge_html, 'html.parser')

    # Extract the challenge title from the HTML title tag
    challenge_title = (soup.find('title').text.strip()).replace("|","\\|")

    # Extract the tasks
    tasks = []
    task_elements = soup.find_all('div', {'class': 'card-header task-header'})
    for task_element in task_elements:
        task_title = (task_element.find('a', {'class': 'card-link'}).text.strip()).replace("                              "," : ")
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
    # Get the current date and time
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%H:%M %d-%m-%y")
    message = "Henrique Oliveira - M0streng0"
    markdown_writeup = f"{formatted_datetime} \\| {message}\n\n"

    markdown_writeup += f"# {challenge_title}\n\n"

    for i, task in enumerate(tasks, start=1):
        markdown_writeup += f"## {task['title']}\n"
        task_questions = questions[i - 1]  # Get the questions for the current task
        for j, question in enumerate(task_questions, start=1):
            markdown_writeup += f"### Question {j}\n"
            markdown_writeup += f"{question}\n\n"
            markdown_writeup += "```\n\n```\n\n> \n\n"

    return markdown_writeup

# Create a simple tkinter window to open a file dialog
def save_file(markdown_writeup):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.asksaveasfilename(initialfile="README",defaultextension=".md", filetypes=[("Markdown Files", "*.md")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(markdown_writeup)
        print(f"Markdown writeup saved to: {file_path}")
    else:
        print("Markdown writeup not saved.")

if __name__ == "__main__":
    challenge_url = input("Enter the TryHackMe challenge URL: ")
    challenge_html = fetch_challenge_page_selenium(challenge_url)

    if challenge_html:
        challenge_title, tasks, questions = parse_challenge_page(challenge_html)
        markdown_writeup = generate_markdown_writeup(challenge_title, tasks, questions)

        # Ask the user where to save the file
        save_file(markdown_writeup)