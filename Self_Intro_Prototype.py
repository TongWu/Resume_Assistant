import csv
import time
from pathlib import Path
from openai import OpenAI
import tkinter as tk
from tkinter import filedialog
import os
from dotenv import load_dotenv
from datetime import datetime
import sys
import argparse
import json

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
model_env = os.getenv('GPT_MODEL')
client = OpenAI(api_key=api_key)

def load_instructions(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data

def get_model_version(model_cmd):
    # First check the cmd line input for model version
    if model_cmd:
        print(f"Select the model {model_cmd} specified via command line. \n")
        return model_cmd
    # Second check .env file
    elif model_env:
        print(f"Select the model {model_env} specify in the .env file. \n")
        return model_env
    # If both above not specified, select the model
    else:
        print("Select the GPT model version: ")
        print("1. gpt-3.5-turbo-1106        (16,385 tokens)   (Default)")
        print("2. gpt-4-1106-preview     (128,000 tokens)")
        models = ['gpt-3.5-turbo-1106', 'gpt-4-1106-preview']
        try:
            selection = int(input("Specify the model number: "))
            if 1 <= selection <= len(models):
                print(f'Select model {models[selection-1]} \n')
                return models[selection - 1]
        # If wrong number or empty, select default
            else:
                print("Invalid selection. Selecting default model (gpt-3.5-turbo-1106). \n")
                return models[0]
        except ValueError:
            print("Invalid input. Selecting default model (gpt-3.5-turbo-1106). \n")
            return models[0]

def select_file():
    print("Please select your resume file: ", end='')
    # Pop up window
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    # If user cancel selection, enter the alter command interface
    if file_path == "":
        print("Abort")
        return None
    else:
        return file_path

def upload_file(file_path):
    # OpenAI API
    response = client.files.create(
        file=Path(file_path),
        purpose="assistants"
    )
    return response.id

def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor

def first_summary(assistant_id, thread_id):
    ask_gpt(thread_id, "")

    print(f'\033[32mBRIEF SUMMARY:\033[0m\n{run_gpt(assistant_id, thread_id).data[0].content[0].text.value}')

def ask_gpt(thread_id, user_message):
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_message
    )
    return 0

def run_gpt(assistant_id, thread_id):
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    printed = False
    spinner = spinning_cursor()
    while run.status != "completed":
        keep_retrieving_run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        if not printed:
            print("Progressing... ", end='')
            printed = True

        sys.stdout.write(next(spinner) + '\b')
        sys.stdout.flush()
        time.sleep(0.1)

        if keep_retrieving_run.status == "completed":
            print("\033[32mCompleted\033[0m \n")
            break

    all_messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )

    return all_messages

def special_command(user_message, is_alter):
    if user_message == '':
        user_message = 'HELP'
    if user_message == "HELP":
        print('There are few commands for simple function:')
        print('LIST: List all conversation stored in local, titled with the resume filename, with the saved timestamp.')
        print('SELECT: Select a conversation stored in local, continue ask with GPT with context.')
        print('NEW: Create a new conversation by uploading a resume.')
        print('EXIT: Exit the program.')
        if not is_alter:
            print('ANY OTHER CONTENT: Ask for GPT about the resume.\n')
        else:
            print()
    elif user_message == "LIST":
        print_log()
    elif user_message == 'SELECT':
        continue_selected_log()
    elif user_message == "NEW":
        main()
    elif user_message == "EXIT":
        sys.exit()
    else:
        if is_alter:
            pass
        else:
            return False
    return True

def keep_asking(assistant_id, thread_id):
    while True:
        user_message = input("\n\033[34mSpecify your problem:\033[0m ")
        if not special_command(user_message, is_alter=False):
            ask_gpt(thread_id, user_message)
            all_messages = run_gpt(assistant_id, thread_id)
            # print(f"USER: {message.content[0].text.value}")
            print(f"\033[32mASSISTANT:\033[0m\n{all_messages.data[0].content[0].text.value}")

def alter_interface():
    while True:
        command = input("Specify command: ")
        special_command(command, is_alter=True)


def save_csv(file_path, assistant_id, thread_id):
    file_name = os.path.basename(file_path)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = [file_name, assistant_id, thread_id, current_time]
    csv_file = 'log.csv'
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['File Name', 'Assistant ID', 'Thread ID', 'Timestamp'])
        writer.writerow(data)

def read_csv():
    file_path = 'log.csv'
    if not os.path.exists(file_path):
        print("The log file does not exist.")
        return []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)
        if len(rows) <= 1:
            print('The log file has only the title row.')
            return []
    data = rows[1:]
    return data

def print_log():
    data = read_csv()
    for i, row in enumerate(data):
        print(f"{i + 1}: {row[0]}, {row[3]}")
    return data

def select_exist_log():
    data = print_log()
    selection = int(input("Select resume file: "))
    if 1 <= selection <= len(data):
        return data[selection - 1]

def continue_selected_log():
    data = select_exist_log()
    thread_id = data[2]
    assistant_id = data[1]
    first_summary(assistant_id, thread_id)
    keep_asking(assistant_id, thread_id)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dryrun', action='store_true', help='Run in dry-run mode')
    parser.add_argument('-f', '--file-path', type=str, help='Specify the file path of the resume')
    parser.add_argument('-m', '--model', type=str, help='Specify the model version')
    args = parser.parse_args()

    # instruction_data = load_instructions('instructions.json')


    file_path = None
    if args.file_path:
        file_path = args.file_path
    elif not args.dryrun:
        file_path = select_file()
        if file_path is None:
            print("Enter alter interface...\n")
            alter_interface()
    print(file_path+'\n') if file_path else print("No file selected.\n")

    # If input with --dryrun or -d, do not create the assistant, give a command interface for more commands
    if not args.dryrun:
        file_id = upload_file(file_path)
        assistant = client.beta.assistants.create(
            instructions="",
            model=get_model_version(args.model),
            file_ids=[file_id],
            tools=[{"type": "retrieval"}]
        )
        thread = client.beta.threads.create()
        # Save the current conservation window to local
        save_csv(file_path, assistant.id, thread.id)

        # When user upload a resume, generate a brief introduction of this resume
        first_summary(assistant.id, thread.id)

        # Let user keep ask AI
        keep_asking(assistant.id, thread.id)
    else:
        print("Running in dry-run mode. Enter 'HELP' for special commands.")
        alter_interface()


if __name__ == "__main__":
    main()
