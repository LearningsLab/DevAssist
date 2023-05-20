import streamlit as st
import time
import numpy as np
from PIL import Image


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
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
