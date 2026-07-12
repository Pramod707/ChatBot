from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")


##prompt templete

prompt = PromptTemplate.from_template(
    (
        "System",
        "You are the helpful ai assistant . Please respond to the user question",
    ),
    ("user", "{question}"),
)

##streamlit framework

st.title("LANGCHAIN WITH GROQ")
st.text_input("Search the topic which you want to know")

##chatbot
llm = ChatGroq(model="llama-3.1-8b-instant")
output_parser = StrOutputParser()
chain = prompt | llm | output_parser
