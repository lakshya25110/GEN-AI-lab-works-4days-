import json
import os
import pickle
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever

def ingest_catalog():
    if not os.path.exists("product_catalog.json"):
        print("Error: product_catalog.json not found. Run generate_catalog.py first.")
        return

    with open("product_catalog.json", "r") as f:
        products = json.load(f)

    documents = []
    for prod in products:
        text_content = f"Title: {prod['title']}\nDescription: {prod['description']}\nCategory: {prod['category']}\nPrice: ${prod['price']}"
        doc = Document(
            page_content=text_content,
            metadata={
                "id": prod["id"],
                "category": prod["category"],
                "title": prod["title"]
            }
        )
        documents.append(doc)

    print(f"Loaded {len(documents)} products.")

    # 1. Create Chroma Vector Index
    print("Creating ChromaDB Vector Index (Local Embeddings)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    persist_directory = "./chroma_db"
    
    # Store in Chroma
    vector_db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    print("ChromaDB Indexing Complete.")

    # 2. Create BM25 Keyword Search Index
    print("Creating BM25 Keyword Index...")
    bm25_retriever = BM25Retriever.from_documents(documents)
    
    # We save the retriever structure (which holds term frequencies etc.) to a file
    with open("bm25_retriever.pkl", "wb") as f:
        pickle.dump(bm25_retriever, f)
    print("BM25 Indexing Complete.")

if __name__ == "__main__":
    ingest_catalog()
