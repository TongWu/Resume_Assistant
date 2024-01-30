from datetime import datetime
import argparse
from helper import openai_utility, alter_interface, log_utility, csv_utility, core, config
from openai import OpenAI
from helper.preload import select_file


def main():
    if not config.api_key:
        config.api_key = input("Please enter your OpenAI API key: ")
        if not config.api_key:
            print("No API key provided, exit...")
            return
    config.client = OpenAI(api_key=config.api_key)
    while not openai_utility.check_openai_api_key():
        config.api_key = input("API key authentication error, type a new key here: ")
        if not config.api_key:
            print("No API key provided, exit...")
            return
        config.client = OpenAI(api_key=config.api_key)

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
            alter_interface.alter_interface()
    print(file_path + '\n') if file_path else print("No file selected.\n")

    # If input with --dryrun or -d, do not create the assistant, give a command interface for more commands
    if not args.dryrun:
        file_id = openai_utility.upload_file(file_path)
        assistant = openai_utility.create_assistant(model=args.model, file_ids=[file_id], tool_type="retrieval")
        thread = openai_utility.create_thread()
        # Save the current conservation window to local
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conversation_path = log_utility.create_conversation_log(current_time)
        csv_utility.save_csv(file_path, assistant.id, thread.id, current_time, conversation_path)

        # When user upload a resume, generate a brief introduction of this resume
        core.first_summary(assistant.id, thread.id, conversation_path)

        # Let user keep ask AI
        core.keep_asking(assistant.id, thread.id, conversation_path)
    else:
        print("Running in dry-run mode. Enter 'HELP' for special commands.")
        alter_interface.alter_interface()


if __name__ == "__main__":
    main()
