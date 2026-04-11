import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

def ingest_documents():
    # 1. Load Data
    if not os.path.exists("company_faq.pdf"):
        print("Error: company_faq.pdf not found.")
        return

    loader = PyPDFLoader("company_faq.pdf")
    documents = loader.load()
    print(f"Loaded {len(documents)} pages from PDF.")

    # 2. Chunk Data
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks.")

    # 3. Create Local Embeddings & Store in ChromaDB
    # Using a small, efficient local model
    print("Initializing local HuggingFace embeddings (this may take a moment on first run)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    persist_directory = "./chroma_db"
    
    # Initialize Chroma
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    
    print(f"Successfully indexed documents into {persist_directory}")

if __name__ == "__main__":
    ingest_documents()
