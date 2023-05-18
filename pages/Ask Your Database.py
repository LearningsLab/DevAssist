from dotenv import load_dotenv
import chunk
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain

import openai
import os

load_dotenv()
st.set_page_config(page_title="Ask your Database")
st.header("Ask your Database and get Insights!! 💬")
OPENAI_API_KEY = os.getenv("openai_key")
openai.api_key=OPENAI_API_KEY


st.write(OPENAI_API_KEY)
st.write("Connect your Database")
#user_question = st.text_input("Ask a question about your PDF:")

db =  SQLDatabase.from_uri(
    "mysql+pymysql://bakewish:EmtTSRwDeKOk@admin.bakewish.in/bakewish_030123",
    )
st.write("db connection established")
# Create a cursor object to execute SQL commands
#st.write(db)