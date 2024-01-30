from sys import exit
from Self_Intro_Prototype import main
from helper.log_utility import print_log, continue_selected_log

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
        print(
            '\033[32mLIST\033[0m: List all conversation stored in local, titled with the resume filename, with the saved timestamp.')
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
        exit()
    else:
        if is_alter:
            pass
        else:
            return False
    return True


def alter_interface():
    """
    Provide an alternative command interface.

    :return: None.
    """
    while True:
        command = input("Specify command: ")
        special_command(command, is_alter=True)