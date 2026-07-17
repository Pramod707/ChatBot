import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
import time

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

if "vector" not in st.session_state:
    st.session_state.embeddings = OllamaEmbeddings(model="nomic-embed-text")
    st.session_state.loader = WebBaseLoader(
        "https://docs.langchain.com/oss/python/deepagents/overview/"
    )
    st.session_state.doc = st.session_state.loader.load()
    st.session_state.text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=250
    )
    st.session_state.final_doc = st.session_state.text_splitter.split_documents(
        st.session_state.doc
    )
    st.session_state.vector_store = FAISS.from_documents(
        st.session_state.final_doc, st.session_state.embeddings
    )

st.title("Chatgroq rag demo")
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

prompt = ChatPromptTemplate.from_template(
    """
    Answer the question as truthfully as possible using the provided context,
    and if the answer is not contained within the context, say "I don't know."

    Context: {context}
    Question: {question}
    
    """
)


def format_doc(docs):
    return "\n\n".join(doc.page_content for doc in docs)


doc_chain = prompt | llm | StrOutputParser()
retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 3})
rag_chain = {
    "context": retriever | RunnableLambda(format_doc),
    "question": RunnablePassthrough(),
} | doc_chain

prompt = st.text_input("Enter your prompt")

if prompt:
    start = time.process_time()
    res = rag_chain.invoke(prompt)
    print("response time", time.process_time() - start)
    st.write(res)
