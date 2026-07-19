import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

st.title("QA with llama")

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

prompt = ChatPromptTemplate.from_template(
    """
    Answer the question as truthfully as possible using the provided context,
    and if the answer is not contained within the context, say "I don't know."

    Context: {context}
    Question: {question}
    """
)
prompt1 = st.text_input("Enter your Question from the pdf!!")


def vector_embeddings(docs):
    st.session_state.embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    st.session_state.loader = DirectoryLoader(
        glob="*.pdf",
        loader_cls=PyPDFLoader,
    )
    st.session_state.docs = st.session_state.loader.load()
    vector_store = FAISS.from_documents(
        st.session_state.docs, st.session_state.embeddings
    )
    st.session_state.vector_store = vector_store


if st.button("Document Embedding"):
    vector_embeddings()
    st.write("Vector store is ready")
