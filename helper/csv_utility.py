from os import path
from helper.config import log_file_path
from helper.preload import get_model_version
import csv


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
    file_name = path.basename(file_path)
    model_name = get_model_version('', False)
    data = [file_name, assistant_id, thread_id, current_time, conversation_log_path, model_name]
    file_exists = path.isfile(log_file_path)
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
    if not path.exists(log_file_path):
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
