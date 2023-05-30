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
   import boto3
   # Configure AWS credentials and region
   aws_access_key_id = "AKIAUTH5FOVEGBBWCJT4"
   aws_secret_access_key = "NvrskYQGzrUyqiRAP0//LGMffnLck/11t14FrWXB"
   region_name = "ap-south-1"  # Replace with your desired region
   log_group_name = "/aws/lambda/prod-fa-payment-init-new"
   # Initialize the CloudWatch Logs client
   client = boto3.client("logs", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)

   from datetime import datetime, timedelta

   # Set the page size (number of log events to fetch in each API call)
   page_size = 10
   counter=0

   # Fetch log events from all log streams within the log group
   log_events = []

   #Calculate the timestamp range for the last 24 hours
   end_time = datetime.utcnow()
   start_time = end_time - timedelta(hours=24)

   # Convert timestamps to milliseconds
   start_time_ms = int(start_time.timestamp() * 1000)
   end_time_ms = int(end_time.timestamp() * 1000)

   # Get a list of all log streams within the log group
   response = client.describe_log_streams(logGroupName=log_group_name)
   log_streams = response["logStreams"]
   log_stream_name = "2023/05/28/[7]d8a03086c3424b58aa966375a8c19841"

   # Fetch log events from all log streams within the log group
   log_events = []
   # for log_stream in log_streams:
   #     log_stream_name = log_stream["logStreamName"]
   #     print
      # Retrieve log events for the log stream within the desired timestamp range
   next_token = None
   while True:
      params = {
         "logGroupName": log_group_name,
         "logStreamName": log_stream_name,
         "startFromHead": True,
      }
      if next_token:
         params["nextToken"] = next_token
      response = client.get_log_events(**params)
      events = response["events"]
      #print('events',events,response)
      log_events.extend(events)
      next_token = response.get("nextToken")
      if not next_token or counter >= 10:
         break
   #st.write(log_events,"log_events")
   # Print the log events


   # Concatenate the strings
   concatenated_text = " "
   for events in log_events:
      concatenated_text += events['message']
      #st.write(concatenated_text)
   #now use the above text to generate embeddings using openai
   #st.write(concatenated_text)
   # split into chunks
   text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=1300,
    chunk_overlap=1200,
    length_function=len
    )    
   chunks = text_splitter.split_text(concatenated_text) 
   st.write(chunks,"chunks")

   embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
   knowledge_base = FAISS.from_texts(chunks, embeddings)
   user_question = st.text_input("Ask a question to your logs data:")
   if user_question:
      docs = knowledge_base.similarity_search(user_question)
      llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)
      chain = load_qa_chain(llm, chain_type="stuff")
      with get_openai_callback() as cb:
         response = chain.run(input_documents=docs, question=user_question)
         st.write(cb)
    
      st.write("openai res: "+response)
   # Process the result
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
   st.write(chunks)

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
     
      st.write("openai res: "+response)
   # Process the result
   
   if result:
      hits = result["hits"]["hits"]
      for hit in hits:
         source = hit["_source"]
         #st.write(source)
   else:
      st.write("Failed to retrieve data from Elasticsearch.")

