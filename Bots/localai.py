from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# prompt templete
prompt = PromptTemplate.from_template(
    """
    You are the helpful ai assistant . Please respond to the user question
    
    question : {question}
    
    
    """
)
st.title("HI , im local ai assistant")
input_text = st.text_input("Search the topic which you want to know")

# chatbot
llm = Ollama(
    model="qwen2.5:7b",
)
output_parser = StrOutputParser()

##chain
chain = prompt | llm | output_parser

#
if input_text:
    response = chain.invoke({"question": input_text})
    st.write(response)
