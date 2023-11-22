from openai import OpenAI, AuthenticationError
from instructions import instructions
import os
import shutil
import sys

# OpenAI client
def create_openAI_client(api_key):
    # create OpenAI client
    client = OpenAI(api_key=api_key)
    try:
        client.models.list()
        return client
    except AuthenticationError as error:
        sys.tracebacklimit = 0
        raise error
    

# upload files to assistant
def upload_files_to_assistant(
        client: OpenAI,
        file_input: str = "./base_docs/resolucion_70_de_2011.pdf"
):
    
    # upload files to assistant
    file = client.files.create(
        file=open(file_input, "rb"),
        purpose="assistants" 
    )
    return file if file else "file not uploaded"


#save temporary files
def save_temporary_files(file):
    if not os.path.exists("src/temp"):
        os.mkdir("src/temp")
    
    with open(f"src/temp/{file.name}", "wb") as f:
        bytes_data = file.getvalue()
        f.write(bytes_data)

    return f"src/temp/{file.name}"


# delete temporary files
def delete_temporary_files():
    if os.path.exists("src/temp"):
        shutil.rmtree("src/temp")


#create list of file ids
def uploader_files_list(
        file: str,
        file_ids: list[str] = []
):
    file_ids = file_ids.append(file)
    return file_ids
    

#create assistant
def create_assistant(
        client: OpenAI,
        file_id: str,
        name: str = "Reader Assistant",
        instructions: str = instructions,
        tools: list = [{"type": "retrieval"}],
        model: str = "gpt-4-1106-preview"
        
):
    assistant = client.beta.assistants.create(
        name=name,
        instructions=instructions,
        tools=tools,
        model=model,
        file_ids=[file_id]
    )
    return assistant


#retrieve assistant
def retrieve_assistant(
        client: OpenAI,
        assistant: dict,

):
    assistant = client.beta.assistant.retrieve(
        assistant_id=assistant.id

    )
    return assistant


# create threads
def create_thread(client: OpenAI):
        thread = client.beta.threads.create()
        return thread


# create messages
def create_message(
          client: OpenAI,
          thread: dict,
          file_ids: str,
          role: str = "user",
          content: str = "¿What is the document title?"
):
    message = client.beta.threads.messages.create(
      thread_id=thread.id,
      role=role,
      content=content,
      file_ids=file_ids
    )
    return message


# create runs
def create_runs(
          client: OpenAI,
          thread: dict,
          assistant: dict
):
    run = client.beta.threads.runs.create(
      thread_id=thread.id,
      assistant_id=assistant.id,
      instructions=instructions
    )
    return run


#evaluate run status
def evaluate_run_status(
          client: OpenAI,
          thread: dict,
          run: dict
):
    while True:
        runner = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
        if runner.status == "completed":
            break
    return runner.status

#retrieve messages
def retrive_messages(
          client: OpenAI,
          thread: dict
):
    messages = client.beta.threads.messages.list(
                thread_id=thread.id
    )  
    return messages.data[0].content[0].text.value


#check uploaded files
def check_uploaded_files(
        client: OpenAI,
        filename
):
    if filename == None:
        return False
    else:
        files_uploaded = client.files.list(
            purpose="assistants",
        )
        filenames_retrieved = [file.filename for file in files_uploaded.data]

        if filename.name in filenames_retrieved:
            return True
        else:
            return False


