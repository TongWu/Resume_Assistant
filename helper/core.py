from helper.openai_utility import ask_gpt, run_gpt
from helper.config import instruction_path
import helper.preload as preload
import helper.alter_interface as alter


def first_summary(assistant_id, thread_id, talk_file_path):
    """
    Generate a brief summary based on a given prompt.

    :param talk_file_path: Store the conversation file path.
    :param assistant_id: The ID of the assistant.
    :param thread_id: The ID of the thread.
    :return: None.
    """
    instructions = preload.load_instructions(instruction_path)
    prompt = instructions['summary']
    if isinstance(prompt, str):
        with open(talk_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f"\033[34mSummary Prompt:\033[0m\n{prompt}\n")

            ask_gpt(thread_id, prompt)
            response = run_gpt(assistant_id, thread_id).data[0].content[0].text.value
            print(f'\033[32mSelf Introduction:\033[0m\n{response}')

            log_file.write(f"\033[32mSelf Introduction:\033[0m\n{response}\n")


def keep_asking(assistant_id, thread_id, talk_file_path):
    """
    Continuously ask questions to the GPT assistant.

    :param talk_file_path: Store the conversation file path.
    :param assistant_id: The ID of the assistant.
    :param thread_id: The ID of the thread.
    :return: None.
    """
    while True:
        user_message = input("\n\033[34mSpecify your problem:\033[0m ")
        if not alter.special_command(user_message, is_alter=False):
            with open(talk_file_path, 'a', encoding='utf-8') as log_file:
                ask_gpt(thread_id, user_message)
                all_messages = run_gpt(assistant_id, thread_id)
                # print(f"\033[34m\nUSER: {message.content[0].text.value}\033[0m")
                response = all_messages.data[0].content[0].text.value
                print(f"\033[32mINTERVIEWEE:\033[0m\n{response}")
                log_file.write(f"\n\033[34mUser:\033[0m\n{user_message}\n")
                log_file.write(f"\033[32mInterviewee:\033[0m\n{response}\n")
                log_file.close()
