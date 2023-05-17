import streamlit as st

st.set_page_config(
    page_title="Ask me",
    page_icon="👋",
)


st.write("# Agent47 your Personal Assistant  👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    This project aims at empowering you connecting various data sources and get insights in your data.
    ### What can you do with it?
    - Connect to your documents (Excel, CSV, JSON, XML , Pdfs etc.)
    - Connect to DataBase (MySQL, Postgres, Oracle, SQL Server, MongoDB, Redis, Cassandra, SQLite etc.)
    - Connect to Google Sheets
    - Connect to Google Analytics
    - Connect to Google Ads
    - Connect to BigQuery
    - Connect to Logging Service ([ElasticSearch](https://streamlit.io), Splunk, Cloudwatch etc.)
    - Connect to Cloud Storage (S3, Azure Blob Storage, Google Cloud Storage etc.)
    - Connect to REST API

    ### What are its use cases?
     - Correlate data from various sources 
     - Get to know your customer issues
     - Get to know your customer behavior

     ### How we do it?
     - We create vector embeddings of your data and then use various NLP techniques to get insights from your data.
     
     ### What are vector embeddings?
    - Vector embeddings are numerical representations of your data.
    - There are various techniques to create vector embeddings of your data. 
        - Like Word2vec, Glove, FastText, BERT etc.
    
    ### How to store vector embeddings?
    - There are multiple ways to store vector embeddings. Like Pinecone, Deeplake, ElasticSearch, Faiss, Redis etc.

    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
"""
)