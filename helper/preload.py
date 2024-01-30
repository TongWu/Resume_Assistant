import json
from tkinter import filedialog
from helper.config import model_env
import tkinter as tk

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
            print(f"Select the model \033[31m{model_env}\033[0m specify in the .env file. \n")
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
                print(f'Select model {models[selection - 1]} \n')
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