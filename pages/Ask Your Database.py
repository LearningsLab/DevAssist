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
import psycopg2
import openai
import os

load_dotenv()
st.set_page_config(page_title="Ask your Database")
st.header("Ask your Database and get Insights!! 💬")
OPENAI_API_KEY = os.getenv("openai_key")
openai.api_key=OPENAI_API_KEY

conn = ''

with st.form("my_form"):
   st.write("Inside the form")
   all_db_types = ["Mysql","Postgres","MongoDB"]
   db_type    = st.selectbox("Select DB Type",all_db_types)
   dbusername = st.text_input("select db username")
   dbpassword = st.text_input("select db password")
   dbname     = st.text_input("select db name")
   dbhost     = st.text_input("select db host")

   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
        if db_type=='Mysql':
            conn = "mysql+pymysql://"+dbusername+":"+dbpassword+"@"+dbhost+"/"+dbname

        if db_type=='Postgres':
            conn = "postgresql+psycopg2://"+dbusername+":"+dbpassword+"@"+dbhost+"/"+dbname
            
        st.write(conn)
        
        if conn!='':
            db =  SQLDatabase.from_uri(
                conn,
                )
            # setup llm
            llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)


            # Create db chain

            QUERY = """
            Given an input question, first create a syntactically correct postgresql query to run, then look at the results of the query and return the answer.
            Use the following format:

            Question: "Question here"
            SQLQuery: "SQL Query to run"
            SQLResult: "Result of the SQLQuery"
            Answer: "Final answer here"

            """
            # Setup the database chain
            db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)

            user_question = st.text_input("write a query:")

            st.write(db_chain.run(user_question))

st.write("Outside the form")

#st.write(db)
