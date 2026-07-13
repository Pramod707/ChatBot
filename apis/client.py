import requests
import streamlit as st


def get_groq_req(input_text):
    response = requests.post(
        "http://localhost:8000/essay/invoke", json={"input": {"topic": input_text}}
    )
 
    return response.json()["output"]["content"]


def get_ollama_req(input_text):
    response = requests.post(
        "http://localhost:8000/poem/invoke", json={"input": {"topic": input_text}}
    )
    return response.json()["output"]


##streamlit framework

st.title("langchain with apis")
input_text1 = st.text_input("write a essay on ")
input_text2 = st.text_input("write a poem on ")

if input_text1:
    st.write(get_groq_req(input_text1))

if input_text2:
    st.write(get_ollama_req(input_text2))
