from helper.csv_utility import read_csv
from os import path, makedirs
from helper.core import keep_asking

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
    print("\n\033[31m=====Chat Log Begin=====\033[0m\n")
    with open(path, 'r', encoding='utf-8') as file:
        print(file.read())
    print("\n\033[31m=====Chat Log End=====\033[0m\n")


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
    # log_file = open(conversation_path, 'a', encoding='utf-8')
    display_conversation(conversation_path)
    keep_asking(assistant_id, thread_id, conversation_path)


def create_conversation_log(timestamp):
    """
    Create a new log file with a timestamp name.

    :return: The file object and file path of the new log file.
    """
    conversation_log_path = f"./logs/log_{timestamp}.txt"
    if not path.exists("../logs"):
        makedirs("../logs")
    # log_file = open(conversation_log_path, 'a', encoding='utf-8')
    return conversation_log_path