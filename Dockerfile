FROM python:3.8
EXPOSE 8501
WORKDIR /streamlit
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD streamlit run Home.py

###testing....
