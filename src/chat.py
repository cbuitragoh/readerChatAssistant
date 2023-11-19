import streamlit as st

from assistant import (
    create_openAI_client,
    create_assistant,
    create_thread,
    create_runs,
    create_message,
    upload_files_to_assistant,
    uploader_files_list,
    evaluate_run_status,
    retrive_messages,
    retrieve_assistant
)
# web page title
st.title(':green[Assistant reader app] :book:')

# sidebar
with st.sidebar:
    openai_api_key = st.text_input(
        "OpenAI API Key",
        key="chatbot_api_key",
        type="password"
    )
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    file = st.file_uploader(
        "Upload a file to assistant",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=False
    )
    print("file:", file)
    
#Assistant settings
client = create_openAI_client(openai_api_key)

file_loaded = upload_files_to_assistant(
                    client=client,
                    #file_input=file["upload_url"]
                )

assistant = create_assistant(
                    client=client,
                    file_id=file_loaded.id,
                )

thread = create_thread(
                    client=client
                )

#convarsation
if prompt := st.chat_input(
    placeholder="Welcome to our app! write what you want to consult in your document",
    max_chars=100
):
    if prompt == None:
        st.info("Please type a query to continue.")
        st.stop()
    else:
        try:
            # select model is a must
            if not openai_api_key:
                st.error("Please enter an OpenAI API key.")
                st.stop()
            if not file:
                st.error("Please upload a file to continue.")
                st.stop()
            else:
                message = create_message(
                    client=client,
                    thread=thread,
                    file_ids=[file_loaded.id],
                    content=prompt
                )
                print("7")
                run = create_runs(
                    client=client,
                    thread=thread,
                    assistant=assistant
                )
                print("8")
                results = evaluate_run_status(
                    client=client,
                    thread=thread,
                    run=run
                )
                print("9")
                response = retrive_messages(
                    client=client,
                    thread=thread
                )
                print("10")
                st.chat_message("assistant").write(response)


        except Exception as e:
            print(e)