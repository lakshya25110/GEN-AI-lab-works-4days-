import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

def run_indexing():
    if not os.path.exists("nebula_manual.pdf"):
        print("Error: nebula_manual.pdf not found.")
        return

    loader = PyPDFLoader("nebula_manual.pdf")
    docs = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    
    embeddings = OpenAIEmbeddings()
    vector_db = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
    
    print("Lab 1 Indexing complete.")

if __name__ == "__main__":
    run_indexing()
