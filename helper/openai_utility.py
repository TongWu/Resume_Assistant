import openai
from pathlib import Path
from helper.config import api_key, client, instruction_path
from sys import stdout
from time import sleep
from helper.cursor import spinning_cursor
from helper.preload import load_instructions, get_model_version


def check_openai_api_key():
    openai.api_key = api_key
    try:
        openai.models.list()
    except openai.AuthenticationError as e:
        print(e)
        return False
    else:
        return True


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

        stdout.write(next(spinner) + '\b')
        stdout.flush()
        sleep(0.1)

        if keep_retrieving_run.status == "completed":
            print("\033[32mCompleted\033[0m \n")
            break

    # Return the answer message
    all_messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )

    return all_messages
