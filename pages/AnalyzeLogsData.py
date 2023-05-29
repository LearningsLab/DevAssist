import streamlit as st
from dotenv import load_dotenv
import time
import numpy as np
from PIL import Image
from langchain import ElasticVectorSearch
from langchain.embeddings import OpenAIEmbeddings
import openai
import os

load_dotenv()
OPENAI_API_KEY = os.getenv('openai_key')
openai.api_key=OPENAI_API_KEY

st.set_page_config(page_title="Analyze Logs Data", page_icon="📈")
import streamlit as st

tab1, tab2, tab3 = st.tabs(["Cloudwatch", "OpenSearch", "ElasticSearch"])

with tab1:
   st.header("Cloudwathc Logs")
   st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab2:
   st.header("OpenSearch logs")
   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
   st.header("ElasticSearch logs")
   #st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
   embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
   elastic_vector_search = ElasticVectorSearch(
      elasticsearch_url="https://search-logs-71-65vca3dfvyuy76y5fcqu53tw6q.ap-south-1.es.amazonaws.com:9243",
      index_name="logstash-apisfloweraura",
      embedding=embedding
   )
   user_question = st.text_input("Search logs")
   if user_question!='':
      st.write(elastic_vector_search.similarity_search(user_question))