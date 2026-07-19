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
from langchain_core.output_parsers import StrOutputParser
import time

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

st.title("QA with llama")

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant.

Use ONLY the provided context to answer the user's question.

If the answer is not present in the context, reply exactly:
"I don't know."

Give a concise answer.

Context:
{context}

Question:
{question}

Answer:
""")
prompt1 = st.text_input("Enter your Question from the pdf!!")


def vector_embeddings():
    ##data ingestion steps
    if "vector_store" not in st.session_state:
        st.session_state.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        ##loading docs
        st.session_state.loader = DirectoryLoader(
            path="./pdfs",
            glob="*.pdf",
            loader_cls=PyPDFLoader,
        )
        st.session_state.docs = st.session_state.loader.load()
        ##splitting the docs
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=250
        )
        st.session_state.chunks = st.session_state.text_splitter.split_documents(
            st.session_state.docs
        )
        ##creating vector store
        st.session_state.vector_store = FAISS.from_documents(
            st.session_state.chunks, st.session_state.embeddings
        )


if st.button("Document Embedding"):
    vector_embeddings()
    st.write("Vector store is ready")


def format_doc(docs):
    return "\n\n".join(doc.page_content for doc in docs)


doc_chain = prompt | llm | StrOutputParser()
retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 3})
rag_chain = {
    "context": retriever | RunnableLambda(format_doc),
    "question": RunnablePassthrough(),
} | doc_chain


if prompt1:
    retriever = st.session_state.vector_store.as_retriever(search_kwargs={"k": 3})
    # Retrieve relevant documents
    docs = retriever.invoke(prompt1)
    rag_chain = (
        {
            "context": retriever | RunnableLambda(format_doc),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    # Generate answer
    answer = rag_chain.invoke(prompt1)
    start = time.process_time()

    st.write(answer)

    print("response time", time.process_time() - start)

    with st.expander("Document Similarity Search"):
        for i, doc in enumerate(docs):
            st.write(f"### Document {i + 1}")
            st.write(doc.page_content)
            st.write(doc.metadata)
            st.write("--------------------------------------")
