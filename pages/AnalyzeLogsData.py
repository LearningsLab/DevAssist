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
   docs = [
    {"document": {"title": "Document 1", "text": "Content of document 1"}},
    {"document": {"title": "Document 2", "text": "Content of document 2"}}
   ]

   # embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
   # knowledge_base = FAISS.from_texts(result, embeddings)
   #st.write("vector res: "+knowledge_base)
   user_question = st.text_input("Ask a question to your Elastic data:")
   if user_question:
      # docs = knowledge_base.similarity_search(user_question)
      # llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
      # chain = load_qa_chain(llm, chain_type="stuff")
      # with get_openai_callback() as cb:
      #    response = chain.run(input_documents=docs, question=user_question)
      #    st.write(cb)
      response = openai.Completion.create(
         engine="davinci",
         prompt=docs,
         max_tokens=100,
         temperature=0.7,
         n=1,
         stop=None,
         documents=len(docs),
         question=user_question
      )

      answer = response.choices[0].text.strip()

      st.write("openai res: "+answer)
   # Process the result
   if result:
      hits = result["hits"]["hits"]
      for hit in hits:
         source = hit["_source"]
         #st.write(source)
   else:
      st.write("Failed to retrieve data from Elasticsearch.")

