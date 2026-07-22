import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
import streamlit as st
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

st.title("GEMMA MODEL DOCUMENT Q&A")

llm = ChatGroq(model="Gemma-7b-it")

prompt = ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only if You dont know the ans 
    just say I DON'T KNOW!!
    
    context:{cotext}
    question:{question}
    """
)


def vector_embeddings():

    if "vector_store" not in st.session_state:
        st.session_state.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001"
        )
        st.session_state.loader = DirectoryLoader(
            path="./pdfs", glob="*.pdf", loader_cls=PyPDFLoader
        )
        st.session_state.docs = st.session_state.loader.load()
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=250
        )
        st.session_state.chunks = st.session_state.text_splitter.split_documents(
            st.session_state.docs
        )
        st.session_state.vector_store = FAISS.from_documents(
            st.session_state.chunks, st.session_state.embeddings
        )


def format_doc():
    return "\n\n".join(doc.page_content for doc in st.session_state.docs)


prompt1 = st.text_input("What you want to ask from the documents ?")
if st.button("create Document Embedding"):
    vector_embeddings()
    st.write("Vector store is ready")


if prompt1:
    retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 3})
    doc_chain = prompt | llm | StrOutputParser()
    rag_chain = {
        "context": retriever | RunnableLambda(format_doc),
        "question": RunnablePassthrough(),
    } | doc_chain

    answer = rag_chain.invoke(prompt1)
    st.write(answer)

    with st.expander("Document similarity search"):
        for i, doc in enumerate(st.session_state.docs):
            st.write(doc.page_content)
            st.write("000000000000000000000000000000000")
