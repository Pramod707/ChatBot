from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langserve import add_routes
from langchain_community.llms import Ollama
import os
import uvicorn
from dotenv import load_dotenv

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")


app = FastAPI(
    title="langchain server", version="0.1.0", description="a simple spi server"
)

add_routes(app, ChatGroq(model="qwen2.5:7b"), path="/groq")
model = ChatGroq(model="qwen2.5:7b", temperature=0.5)
llm = Ollama(model="qwen2.5:7b", temperature=0.5)

prompt1 = ChatPromptTemplate.from_template(
    "write me a essay on topic {topic} of 100 words"
)
prompt2 = ChatPromptTemplate.from_template(
    "write me a poem on topic {topic} of 100 words"
)

add_routes(app, prompt1 | model, path="/essay")
add_routes(app, prompt2 | llm, path="/poem")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
