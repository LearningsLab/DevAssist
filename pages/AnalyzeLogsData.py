import streamlit as st
from dotenv import load_dotenv
import time
import numpy as np
from PIL import Image
from langchain import ElasticVectorSearch
from langchain.embeddings import OpenAIEmbeddings
import openai
import os
import requests
import json
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
from langchain.text_splitter import CharacterTextSplitter

load_dotenv()
OPENAI_API_KEY = os.getenv('openai_key')
openai.api_key=OPENAI_API_KEY

st.set_page_config(page_title="Analyze Logs Data", page_icon="📈")

tab1, tab2, tab3 = st.tabs(["Cloudwatch", "OpenSearch", "ElasticSearch"])

with tab1:
   st.header("Cloudwathc Logs")
   st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab2:
   st.header("OpenSearch logs")
   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
   st.header("ElasticSearch logs")
  
   def get_elasticsearch_data(index_name, query):
      # Elasticsearch endpoint
      url = f"http://vpc-similar-product-pwanh5zsjbcnorrre77cazmfce.ap-south-1.es.amazonaws.com/{index_name}/_search"
      
      # Request headers
      headers = {
         "Content-Type": "application/json"
      }
      
      # Request body
      body = {
         "query": {
            "match": {
                  "occasion": query
            }
         }
      }
      
      # Send the request
      response = requests.get(url, headers=headers, json=body)
      
      # Check the response status
      if response.status_code == 200:
         # Parse and process the response data
         response_data = response.json()
         # Handle the retrieved data according to your needs
         return response_data
      else:
         # Handle the error case
         st.write(f"Error: {response.status_code}")
         return None

      
   # Example usage
   index_name = "giftfinder_node"
   query = "Anniversary"

   result = get_elasticsearch_data(index_name, query)
   #st.write(result)
   # docs = [
   #  {"title1": "Document 1", "text1": "Content of document 1"},
   #  {"title2": "Document 2", "text2": "Content of document 2"},
   #  {"title3": "Document 3", "text3": "Content of document 3"},
   #  {"title4": "Document 4", "text4": "Content of document 4"},
   #  {"title5": "Document 5", "text5": "Content of document 5"},
   #  {"title6": "Document 6", "text6": "Content of document 6"}
   # ]
    
   # Convert JSON data to string
   json_string = json.dumps(result)
   
   # split into chunks
   text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=25,
    chunk_overlap=20,
    length_function=len
    )    
   chunks = text_splitter.split_text(json_string) 
   #st.write(chunks)

   embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
   knowledge_base = FAISS.from_texts(chunks, embeddings)
  
   user_question = st.text_input("Ask a question to your Elastic data:")
   if user_question:
      docs = knowledge_base.similarity_search(user_question)
      llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
      chain = load_qa_chain(llm, chain_type="stuff")
      with get_openai_callback() as cb:
         response = chain.run(input_documents=docs, question=user_question)
         st.write(cb)
      # response = openai.Completion.create(
      #    engine="davinci",
      #    prompt=docs,
      #    max_tokens=100,
      #    temperature=0.7,
      #    n=1,
      #    stop=None,
      #    documents=len(docs),
      #    question=user_question
      # )

      # answer = response.choices[0].text.strip()

      st.write("openai res: "+response)
   # Process the result
   
   if result:
      hits = result["hits"]["hits"]
      for hit in hits:
         source = hit["_source"]
         #st.write(source)
   else:
      st.write("Failed to retrieve data from Elasticsearch.")

