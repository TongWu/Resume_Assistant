# Assessment Introduction

This is a repo for SAP 2023-2024 AI Engineer Internship Technical Assessment. The assessment requires the candidate to create a Generative AI app prototype that introduces myself to users. The app should be able to provide pertinent answers to user’s question.

This project is written by Python which integrated with OpenAI API, the presentation form of this app is a command-line application.

## Idea

The core concept of the project is to harness the power of artificial intelligence to create an easy-to-use interface, enabling interviewers to quickly and comprehensively understand applicants. Designed with a command-line interface, this tool provides an unparalleled user experience with its rapid response and high efficiency. Keeping the user in mind, the project not only addresses everyday needs but also innovates for special scenarios. For instance, following each upload or selection of a resume, the tool automatically generates a brief introduction of the applicant, allowing users to grasp key points swiftly. Additionally, it offers a choice between different GPT models, such as gpt-3.5 and gpt-4, enabling users to select based on their needs and costs. The inclusion of special command inputs, local storage of session and assistant IDs, and support for command-line variables further enhance the tool's practicality and convenience.

## Design

The program executes core functionalities such as file uploading, assistant creation, and question answering through the OpenAI API. Its operation can be divided into several key phases:

1.  **Resume File Selection:** Utilizing the Tkinter library, the program provides a user-friendly interface through a system window for selecting resume files.
2.  **Model Selection and File Uploading:** The program supports two GPT models (gpt-3.5-turbo-1106 and gpt-4-1106-preview) and uploads resume files via the files.create method of the OpenAI client object, setting the file's purpose to "assistance" and returning a file ID for subsequent use.
3.  **Resume Summary Generation:** Upon uploading the resume, the program automatically generates a concise summary using the GPT API without requiring user intervention.
4.  **Answering User Questions:** Following the self introduction, the program answers user questions in a similar manner, ensuring accuracy and timeliness.

### Resume File Selection

-   Using the Tk library to call a system window for file selection, providing a user-friendly UI.

![image-20240112131705849](https://images.wu.engineer/images/2024/01/12/202401121317374.png)

### Model Selection and File Uploading

-   With file uploading to GPT, available models include gpt-3.5-turbo-1106 and gpt-4-1106-preview.
-   The program uploads the file through the files.create method of the client object, setting its purpose as "assistance," and returns a file ID for later use.

### Resume Summary Generation

-   The program automatically generates a summary of the resume using the GPT API when uploading a resume for the first time or recovering from a locally saved session context, requiring no user operation.
-   An assistant is created through the API, with its preset instruction words stored locally in instructions.json, and the previously uploaded file ID is attached to the assistant.
-   Subsequently, a thread is started, attaching instructions for generating a resume summary, also stored locally.
-   A runner object is created to submit the instructions to the assistant, with regular status refreshes to await a response.
-   Once a reply is received, it is printed, and the program awaits the next question.

![image-20240112140708703](https://images.wu.engineer/images/2024/01/12/202401121407725.png)

### Answering User Questions

-   After self-introduction, the application lets the user keep asking question.
-   The application will do specific instructions when the user type special command, like “EXIT”, “SELECT”, etc.

### Additional Parameter Options

The program integrates a series of commands (such as SELECT, LIST, etc.), enhancing the interactivity and functionality of the user interface. These commands allow users to more conveniently browse and manage locally stored conversations. For instance, viewing a list of all conversations (using the LIST command) or selecting a specific conversation to continue the dialogue (using the SELECT command).

![image-20240113132232923](https://images.wu.engineer/images/2024/01/13/202401131322960.png)

### Store conversation and context

The program is capable of locally storing the ID and context of each conversation. Through the LIST command, users can view all saved conversations, and with the SELECT command, they can choose a particular conversation to display its chat history. This feature provides users with a convenient way to review and continue previous conversations, enhancing the practicality and user experience of the AI assistant.

![image-20240113143433983](https://images.wu.engineer/images/2024/01/13/202401131434012.png)

## Conclusion

The technical implementation of the program covers file reading, API calls, thread management, and more. Key features include:

-   **File Selection and Upload:** A graphical user interface is built using Tkinter, allowing users to easily select local files and upload them to the server via the OpenAI API.
-   **Assistant and Thread Creation:** Dynamic interaction with users is achieved through programming interfaces for creating assistants and threads.
-   **Flexible Command-Line Interface:** The program offers various command-line options, including dry-run mode, file path selection, and model choice, making it more flexible and user-friendly.
-   **Local Storage and Configuration:** Configuration data and instruction words are stored in local files, allowing users to easily access and modify them as needed.

