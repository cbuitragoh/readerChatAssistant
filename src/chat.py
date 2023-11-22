import streamlit as st
from assistant import (
    check_uploaded_files,
    create_openAI_client,
    create_assistant,
    create_thread,
    create_runs,
    create_message,
    delete_temporary_files,
    evaluate_run_status,
    retrive_messages,
    retrieve_assistant,
    save_temporary_files,
    upload_files_to_assistant,
    uploader_files_list,
)
from logger import create_logger

#logging start
logger = create_logger()

#check no temporary files
delete_temporary_files()

#stateful variables
if "api_key" not in st.session_state:
    st.session_state.api_key = False

def set_api_key(state_api: bool):
    st.session_state.api_key = state_api

if "len_api_key" not in st.session_state:
    st.session_state.len_api_key = 0

def set_len_api_key(len_api_key: int):
    st.session_state.len_api_key = len_api_key

if "client" not in st.session_state:
    st.session_state.client = None

def set_client(client):
    st.session_state.client = client

if "state_file" not in st.session_state:
    st.session_state.state_file = False

def set_state_file(state_file: bool):
    st.session_state.state_file = state_file

if "file" not in st.session_state:
    st.session_state.file = None

def set_file(file):
    st.session_state.file = file

if "assistant" not in st.session_state:
    st.session_state.assistant = None

def set_assistant(assistant):
    st.session_state.assistant = assistant

if "thread" not in st.session_state:
    st.session_state.thread = None

def set_thread(thread):
    st.session_state.thread = thread

if "logger" not in st.session_state:
    st.session_state.logger = logger


# web page title
st.title(':green[Reader Assistant app] :book:')

# sidebar
with st.sidebar:
    openai_api_key = st.text_input(
        "OpenAI API Key",
        key="chatbot_api_key",
        type="password",
        on_change=set_api_key,
        args=(True,)
    )
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    file = st.file_uploader(
        "Upload a file to assistant",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=False,
        on_change=set_state_file,
        args=(True if st.session_state.state_file == False else False,)
    )
    
#Assistant settings
set_len_api_key(len(openai_api_key))
if st.session_state.api_key == True and st.session_state.len_api_key > 0:
    if st.session_state.client == None:
        client = create_openAI_client(openai_api_key)
        set_client(client)
    else:
        client = st.session_state.client
    if st.session_state.state_file == False or file == None:
        st.info("Please upload file to assistant to continue")
        st.stop()
    else:
        checked = check_uploaded_files(client=client, filename=file)
        if checked:
            logger.info("File already uploaded")
        else:
            with st.spinner("Uploading file to assistant..."):
                temp_file = save_temporary_files(file)
                file_to_assistant = upload_files_to_assistant(
                                client=client,
                                file_input=temp_file
                            )
                set_file(file_to_assistant)
    if st.session_state.assistant == None and st.session_state.file != None:
        assistant = create_assistant(
                    client=client,
                    file_id=(st.session_state.file).id,
                )
        set_assistant(assistant)
        logger.info(str(st.session_state.assistant))
    else:
        assistant = st.session_state.assistant
        #log the assistant.id for debugging use
        logger.info(str(st.session_state.assistant))
    
    if st.session_state.thread == None and st.session_state.assistant != None:
        thread = create_thread(
                    client=client
                )
        set_thread(thread)
        logger.info(str(st.session_state.thread))
    else:
        thread = st.session_state.thread
        #log the thread.id for debugging use
        logger.info(str(st.session_state.thread))
    if (
        st.session_state.thread != None and 
        st.session_state.assistant != None and
        st.session_state.file != None
    ):
        st.chat_message("assistant").write("I'm ready to work!")
else:
    st.info("Welcome our app. " '\n'
            "Please enter an OpenAI" '\n'
             "API key to continue.")
    st.stop()


#conversation
if prompt := st.chat_input(
    placeholder="Welcome to our app! Type " +
                 "what you want to consult in your document",
    max_chars=100
):
    if prompt == None:
        st.info("Please type a query to continue.")
        st.stop()
    else:
        st.chat_message("user").write(prompt)
        try:
            message = create_message(
                client=client,
                thread=thread,
                file_ids=[(st.session_state.file).id],
                content=prompt
            )
            run = create_runs(
                client=client,
                thread=thread,
                assistant=assistant
            )
            results = evaluate_run_status(
                client=client,
                thread=thread,
                run=run
            )
            response = retrive_messages(
                client=client,
                thread=thread
            )
            st.chat_message("assistant").write(response)

        except Exception as e:
            logger.exception(e)


        