from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
##lanngsmit tracking
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")


##prompt templete

prompt = PromptTemplate.from_template(
    """
  You are the helpful ai assistant . Please respond to the user question
  
  question : {question}
"""
)
##streamlit framework

st.title("LANGCHAIN WITH GROQ")
input_text = st.text_input("Search the topic which you want to know")

##chatbot
llm = ChatGroq(model="llama-3.1-8b-instant")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

if input_text:
    st.write(chain.invoke({"question": input_text}))
