FROM python:3.9
EXPOSE 8501
WORKDIR /usr/src/app
COPY ./ ./
RUN pip install -r requirements.txt
CMD streamlit run Home.py