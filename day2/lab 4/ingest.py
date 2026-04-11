import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def ingest_all_docs():
    all_documents = []
    
    # 1. Load PDF
    if os.path.exists("hr_policy.pdf"):
        print("Loading PDF...")
        pdf_loader = PyPDFLoader("hr_policy.pdf")
        all_documents.extend(pdf_loader.load())
    else:
        print("Warning: hr_policy.pdf not found.")
        
    # 2. Load CSV
    if os.path.exists("inventory.csv"):
        print("Loading CSV...")
        csv_loader = CSVLoader(file_path="inventory.csv")
        all_documents.extend(csv_loader.load())
    else:
        print("Warning: inventory.csv not found.")
        
    # 3. Load TXT
    if os.path.exists("company_history.txt"):
        print("Loading TXT...")
        txt_loader = TextLoader("company_history.txt")
        all_documents.extend(txt_loader.load())
    else:
        print("Warning: company_history.txt not found.")

    if not all_documents:
        print("Error: No documents found to index.")
        return

    print(f"Loaded a total of {len(all_documents)} unchunked documents from mixed sources.")

    # Chunk the combined documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = text_splitter.split_documents(all_documents)
    print(f"Split into {len(chunks)} combined chunks.")

    # Embed and Store
    print("Initializing Embeddings Model...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    persist_directory = "./chroma_db"
    
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    
    print(f"Successfully indexed Multi-Document RAG into {persist_directory}")

if __name__ == "__main__":
    ingest_all_docs()
