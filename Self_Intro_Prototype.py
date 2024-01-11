from pathlib import Path
from openai import OpenAI
import tkinter as tk
from tkinter import filedialog

client = OpenAI(api_key='')

def get_model_version():
    print("Select the GPT model version: ")
    print("1. gpt-3.5-turbo-1106        (16,385 tokens)   (Default)")
    print("2. gpt-4-1106-preview     (128,000 tokens)")
    models = ['gpt-3.5-turbo-1106', 'gpt-4-1106-preview']
    try:
        selection = int(input("Specify the model number: "))
        if 1 <= selection <= len(models):
            print(f'Select model {models[selection-1]}')
            return models[selection - 1]
        else:
            print("Invalid selection. Selecting default model (gpt-3.5-turbo-1106).")
            return models[0]
    except ValueError:
        print("Invalid input. Selecting default model (gpt-3.5-turbo-1106).")
        return models[0]

def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

def upload_file(file_path):
    response = client.files.create(
        file=Path(file_path),
        purpose="assistants"
    )
    return response.id


def main():
    # TODO: Pop out a select file GUI window, user-friendly
    print("Please select your resume file: ")
    file_path = select_file()
    file_id = upload_file(file_path)

    assistant = client.beta.assistants.create(
        instructions="Now you're an AI assistant helping the interviewer summarize and extend the key points in resume. You need to answer the questions asked by the user based on the resume file provided. Also, the user may ask some general questions, you need to answer these by default model.",
        model=get_model_version(),
        file_ids=[file_id],
        tools=[{"type": "retrieval"}]
    )

    thread = client.beta.threads.create()

    # TODO: When user upload a resume, generate a brief introduction of this resume

    while True:
        user_message = input("Specify your problem: ")
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_message
        )

        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id
        )

        printed = False
        while run.status != "completed":
            keep_retrieving_run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if not printed:
                print(f"Run status: {keep_retrieving_run.status}")
                printed = True

            if keep_retrieving_run.status == "completed":
                print("Completed")
                break

        all_messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )

        # print(f"USER: {message.content[0].text.value}")
        print(f"ASSISTANT: {all_messages.data[0].content[0].text.value}")


if __name__ == "__main__":
    main()
