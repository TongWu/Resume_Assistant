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
log_file_path = './log.csv'
instruction_path = './instructions.json'

def load_instructions(file_path):
    """
    Load instructions from a JSON file.

    :param file_path: The path to the JSON file containing the instructions.
    :return: A dictionary containing the instructions.
    """
    with open(file_path, 'r', encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
    jsonfile.close()
    return data

def get_model_version(model_cmd, isprint):
    """
    Determine the model version to use based on command line input or .env settings.

    :param isprint: Select to print the outcome or not.
    :param model_cmd: The model version specified via command line argument.
    :return: The selected model version.
    """
    # First check the cmd line input for model version
    if model_cmd:
        if isprint:
            print(f"Select the model {model_cmd} specified via command line. \n")
        return model_cmd
    # Second check .env file
    elif model_env:
        if isprint:
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
    """
    Open a file dialog for the user to select a file.

    :return: The path to the selected file, or None if no file is selected.
    """
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
    """
    Upload a file to OpenAI.

    :param file_path: The path to the file to be uploaded.
    :return: The ID of the uploaded file.
    """
    # OpenAI API
    response = client.files.create(
        file=Path(file_path),
        purpose="assistants"
    )
    return response.id

def create_assistant(prompt=None, model='gpt-3.5-turbo-1106', file_ids=None, tool_type="retrieval"):
    """
    Create an assistant using the OpenAI API.

    :param prompt: The instruction prompt for the assistant.
    :param model: The model version to use.
    :param file_ids: List of file IDs to be used by the assistant.
    :param tool_type: The type of tool to be used.
    :return: The created assistant object.
    """
    if not prompt:
        instructions = load_instructions(instruction_path)
        prompt = instructions['assistant']
    # Create an assistant
    return client.beta.assistants.create(
        instructions=prompt,
        model=get_model_version(model, True),
        file_ids=file_ids,
        tools=[{"type": tool_type}]
    )

def create_thread():
    """
    Create a new thread for interaction with an assistant.

    :return: The created thread object.
    """
    return client.beta.threads.create()

def spinning_cursor():
    """
    Generator for a spinning cursor animation.

    :return: Yields the next character in the spinning cursor sequence.
    """
    while True:
        for cursor in '|/-\\':
            yield cursor

def first_summary(assistant_id, thread_id, log_file):
    """
    Generate a brief summary based on a given prompt.

    :param log_file: Store the conversation.
    :param assistant_id: The ID of the assistant.
    :param thread_id: The ID of the thread.
    :return: None.
    """
    instructions = load_instructions(instruction_path)
    prompt = instructions['summary']
    if isinstance(prompt, str):
        log_conversation(log_file, f"\033[34mSummary Prompt:\033[0m\n{prompt}\n")

        ask_gpt(thread_id, prompt)
        response = run_gpt(assistant_id, thread_id).data[0].content[0].text.value
        print(f'\033[32mSELF INTRODUCTION:\033[0m\n{response}')

        log_conversation(log_file, f"\033[32mSELF INTRODUCTION:\033[0m\n{response}\n")
        log_file.close()

def ask_gpt(thread_id, user_message):
    """
    Send a message to the GPT assistant.

    :param thread_id: The ID of the thread.
    :param user_message: The message to send.
    :return: 0 indicating success.
    """
    # Push message to assistant
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_message
    )
    return 0

def run_gpt(assistant_id, thread_id):
    """
    Execute a run of the GPT assistant.

    :param assistant_id: The ID of the assistant.
    :param thread_id: The ID of the thread.
    :return: All messages from the run.
    """
    # Run the thread
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    printed = False
    spinner = spinning_cursor()
    # Retrieve the status
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

    # Return the answer message
    all_messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )

    return all_messages

def special_command(user_message, is_alter):
    """
    Process special commands entered by the user.

    :param user_message: The message or command entered by the user.
    :param is_alter: Boolean indicating if in alter mode.
    :return: True if a special command was processed, False otherwise.
    """
    # If user press ENTER, return 'HELP' command
    if user_message == '':
        user_message = 'HELP'
    if user_message == "HELP":
        print('There are few commands for simple function:')
        print('\033[32mLIST\033[0m: List all conversation stored in local, titled with the resume filename, with the saved timestamp.')
        print('\033[32mSELECT\033[0m: Select a conversation stored in local, continue ask with GPT with context.')
        print('\033[32mNEW\033[0m: Create a new conversation by uploading a resume.')
        print('\033[32mEXIT\033[0m: Exit the program.')
        if not is_alter:
            print('\033[32mANY OTHER CONTENT\033[0m: Ask for GPT about the resume.')
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

def keep_asking(assistant_id, thread_id, log_file):
    """
    Continuously ask questions to the GPT assistant.

    :param log_file: Store the conversation.
    :param assistant_id: The ID of the assistant.
    :param thread_id: The ID of the thread.
    :return: None.
    """
    while True:
        user_message = input("\n\033[34mSpecify your problem:\033[0m ")
        if not special_command(user_message, is_alter=False):
            log_conversation(log_file, f"\n\033[34mUser:\033[0m\n{user_message}\n")
            ask_gpt(thread_id, user_message)
            all_messages = run_gpt(assistant_id, thread_id)
            # print(f"\033[34m\nUSER: {message.content[0].text.value}\033[0m")
            response = all_messages.data[0].content[0].text.value
            print(f"\033[32mINTERVIEWEE:\033[0m\n{response}")
            log_conversation(log_file, f"\033[32mInterviewee:\033[0m\n{response}\n")
            log_file.close()

def alter_interface():
    """
    Provide an alternative command interface.

    :return: None.
    """
    while True:
        command = input("Specify command: ")
        special_command(command, is_alter=True)


def save_csv(file_path, assistant_id, thread_id, current_time, conversation_log_path):
    """
    Save conversation details to a CSV file.

    :param conversation_log_path: File path of conversation log.
    :param current_time: The timestamp of current time.
    :param file_path: The path of the file related to the conversation.
    :param assistant_id: The ID of the assistant.
    :param thread_id: The ID of the thread.
    :return: None
    """
    file_name = os.path.basename(file_path)
    model_name = get_model_version('', False)
    data = [file_name, assistant_id, thread_id, current_time, conversation_log_path, model_name]
    file_exists = os.path.isfile(log_file_path)
    with open(log_file_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['File Name', 'Assistant ID', 'Thread ID', 'Timestamp'])
        writer.writerow(data)

def read_csv():
    """
    Read and return the contents of the log CSV file.

    :return: A list of rows from the CSV file.
    """
    if not os.path.exists(log_file_path):
        print("The log file does not exist.")
        return []
    with open(log_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)
        if len(rows) <= 1:
            print('The log file has only the title row.')
            return []
    # Read csv without title
    data = rows[1:]
    return data

def print_log():
    """
    Print the log entries from the CSV file.

    :return: The data read from the CSV file.
    """
    data = read_csv()
    # Print filename and timestamp
    for i, row in enumerate(data):
        print(f"{i + 1}: {row[0]}, {row[5]}, {row[3]}")
    return data

def select_exist_log():
    """
    Allow the user to select an existing log entry.

    :return: The data of the selected log entry.
    """
    data = print_log()
    selection = int(input("Select resume file: "))
    if 1 <= selection <= len(data):
        return data[selection - 1]

def display_conversation(path):
    """
    Display the content of a log file.

    :param path: The path to the log file.
    """
    with open(path, 'r', encoding='utf-8') as file:
        print(file.read())

def continue_selected_log():
    """
    Continue interaction based on a selected log entry.

    :return: None.
    """
    data = select_exist_log()
    thread_id = data[2]
    assistant_id = data[1]
    # first_summary(assistant_id, thread_id)
    conversation_path = data[4]
    log_file = open(conversation_path, 'a', encoding='utf-8')
    display_conversation(conversation_path)
    keep_asking(assistant_id, thread_id, log_file)

def create_conversation_log(timestamp):
    """
    Create a new log file with a timestamp name.

    :return: The file object and file path of the new log file.
    """
    conversation_log_path = f"./logs/log_{timestamp}.txt"
    if not os.path.exists("./logs"):
        os.makedirs("./logs")
    log_file = open(conversation_log_path, 'a', encoding='utf-8')
    return log_file, conversation_log_path

def log_conversation(log_file, message):
    """
    Log a message to the log file.

    :param log_file: The log file object.
    :param message: The message to log.
    """
    log_file.write(message + '\n')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dryrun', action='store_true', help='Run in dry-run mode')
    parser.add_argument('-f', '--file-path', type=str, help='Specify the file path of the resume')
    parser.add_argument('-m', '--model', type=str, help='Specify the model version')
    args = parser.parse_args()

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
        assistant = create_assistant(model=args.model, file_ids=[file_id], tool_type="retrieval")
        thread = create_thread()
        # Save the current conservation window to local
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_file, conversation_path = create_conversation_log(current_time)
        save_csv(file_path, assistant.id, thread.id, current_time, conversation_path)

        # When user upload a resume, generate a brief introduction of this resume
        first_summary(assistant.id, thread.id, log_file)

        # Let user keep ask AI
        keep_asking(assistant.id, thread.id, log_file)
    else:
        print("Running in dry-run mode. Enter 'HELP' for special commands.")
        alter_interface()


if __name__ == "__main__":
    main()
