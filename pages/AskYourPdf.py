# from dotenv import load_dotenv
import chunk
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from dotenv import load_dotenv

import openai
import os

load_dotenv()

st.set_page_config(page_title="Ask your PDF")
st.header("Ask your PDF 💬")
OPENAI_API_KEY = os.getenv('openai_key')
openai.api_key=OPENAI_API_KEY
#os.environ["OPENAI_API_KEY"]

st.write("Inside the form"+OPENAI_API_KEY)
# st.write(openai.Engine.list())

# from langchain.embeddings.openai import OpenAIEmbeddings
# embeddings = OpenAIEmbeddings(
#     deployment="your-embeddings-deployment-name",
#     model="your-embeddings-model-name",
#     api_base="https://your-endpoint.openai.azure.com/",
#     api_type="azure",
# )
# text = "This is a test query."
# query_result = embeddings.embed_query(text)

# load_dotenv()


# upload file
pdf = st.file_uploader("Upload your PDF", type="pdf")

# extract the text
if pdf is not None:
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    # st.write(text)
    # split into chunks
    text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=250,
    chunk_overlap=200,
    length_function=len
    )    
    chunks = text_splitter.split_text(text) 
        
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    knowledge_base = FAISS.from_texts(chunks, embeddings)
    user_question = st.text_input("Ask a question about your PDF:")
    if user_question:
        docs = knowledge_base.similarity_search(user_question)
        llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
        chain = load_qa_chain(llm, chain_type="stuff")
        with get_openai_callback() as cb:
          response = chain.run(input_documents=docs, question=user_question)
          st.write(cb)
           
        st.write(response)

    # def readEmbeddings(embeddings):

    # # split into chunks
    # text_splitter = CharacterTextSplitter(
    # separator="\n",
    # chunk_size=250,
    # chunk_overlap=200,
    # length_function=len
    # )
    # chunks = text_splitter.split_text(text)
    # st.write(chunks)

    # create embeddings
# embeddings = OpenAIEmbeddings()
# knowledge_base = FAISS.from_texts(chunks, embeddings)

# # show user input
# user_question = st.text_input("Ask a question about your PDF:")
# if user_question:
#     docs = knowledge_base.similarity_search(user_question)
