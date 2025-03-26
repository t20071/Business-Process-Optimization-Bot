import streamlit as st
import os
from os import getenv
from PyPDF2 import PdfReader
import docx
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from streamlit_chat import message
from langchain.callbacks import get_openai_callback
from langchain.prompts import (
    SystemMessagePromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)


def main():
    load_dotenv()
    st.set_page_config(page_title="Business Process AI")
    st.header("Business Process AI")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    if "processComplete" not in st.session_state:
        st.session_state.processComplete = None

    with st.sidebar:
        uploaded_files = st.file_uploader(
            "Upload your business process document",
            type=["pdf", "docx"],
            accept_multiple_files=True,
        )
        process = st.button("Process")
    if process:
        files_text = get_files_text(uploaded_files)
        text_chunks = get_text_chunks(files_text)
        vetorestore = get_vectorstore(text_chunks)

        st.session_state.conversation = get_conversation_chain(
            vetorestore, getenv("OPENAI_KEY")
        )

        st.session_state.processComplete = True

    if st.session_state.processComplete == True:
        user_question = st.chat_input("ask me about your current business process")
        if user_question:
            handel_userinput(user_question)


def get_files_text(uploaded_files):
    text = ""
    for uploaded_file in uploaded_files:
        split_tup = os.path.splitext(uploaded_file.name)
        file_extension = split_tup[1]
        if file_extension == ".pdf":
            text += get_pdf_text(uploaded_file)
        elif file_extension == ".docx":
            text += get_docx_text(uploaded_file)
        else:
            text += get_csv_text(uploaded_file)
    return text


def get_pdf_text(pdf):
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def get_docx_text(file):
    doc = docx.Document(file)
    allText = []
    for docpara in doc.paragraphs:
        allText.append(docpara.text)
    text = " ".join(allText)
    return text


def get_csv_text(file):
    return "a"


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=900, chunk_overlap=100, length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings()
    knowledge_base = FAISS.from_texts(text_chunks, embeddings)
    return knowledge_base


def get_conversation_chain(vetorestore, openai_api_key):
    general_system_template = r""" 
    Your goal is to understand current development process from the context and help user optimise their current process.
    ----
    {context}
    ----
    """
    general_user_template = "Question:```{question}```"
    messages = [
        SystemMessagePromptTemplate.from_template(general_system_template),
        HumanMessagePromptTemplate.from_template(general_user_template),
    ]
    qa_prompt = ChatPromptTemplate.from_messages(messages)
    llm = ChatOpenAI(
        openai_api_key=openai_api_key,
        model_name="gpt-3.5-turbo",
        temperature=0,
    )
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vetorestore.as_retriever(),
        memory=memory,
        combine_docs_chain_kwargs={"prompt": qa_prompt},
    )
    return conversation_chain


# This function takes a user question as input, sends it to a conversation model and displays the conversation history along with some additional information.
def handel_userinput(user_question):
    with get_openai_callback() as cb:
        response = st.session_state.conversation({"question": user_question})
    st.session_state.chat_history = response["chat_history"]

    response_container = st.container()

    with response_container:
        for i, messages in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                message(messages.content, is_user=True, key=str(i))
            else:
                message(messages.content, key=str(i))


if __name__ == "__main__":
    main()
