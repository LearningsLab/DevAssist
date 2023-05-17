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

import openai
import os
st.set_page_config(page_title="Ask your Database")
st.header("Ask your Database and get Insights!! 💬")
os.environ["OPENAI_API_KEY"]="sk-input key here"
openai.api_key="sk-input key here"

st.write("Connect your Database")