from pathlib import Path
from openai import OpenAI

client = OpenAI(api_key='')


def upload_file(file_path):
    response = client.files.create(
        file=Path(file_path),
        purpose="assistants"
    )
    return response.id


file_path = input("File Path: ")
file_id = upload_file(file_path)

assistant = client.beta.assistants.create(
    instructions="Now you're an AI assistant helping the interviewer quickly summarize the key points in resume. You need to answer the questions asked by the interviewer based on the word or pdf resume file provided.",
    model="gpt-3.5-turbo-1106",
    file_ids=[file_id],
    tools=[{"type": "retrieval"}]
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="What is the candidate's educational background?"
)

run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id
)

while run.status != "completed":
    keep_retrieving_run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    print(f"Run status: {keep_retrieving_run.status}")

    if keep_retrieving_run.status == "completed":
        print("\n")
        break

all_messages = client.beta.threads.messages.list(
    thread_id=thread.id
)

print(f"USER: {message.content[0].text.value}")
print(f"ASSISTANT: {all_messages.data[0].content[0].text.value}")