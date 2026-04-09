from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List, Dict
import os

class VectorRetriever:
    def __init__(self, embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
        self.indices = {}

    def build_index(self, strategy_name: str, chunks: List[str]):
        """Builds and stores a FAISS index for a specific strategy."""
        if not chunks:
            return
        vectorstore = FAISS.from_texts(chunks, self.embeddings)
        self.indices[strategy_name] = vectorstore

    def retrieve(self, query: str, strategy_name: str, k: int = 4) -> List[str]:
        """Retrieves top-k chunks for a strategy."""
        if strategy_name not in self.indices:
            raise ValueError(f"Index for strategy '{strategy_name}' not built.")
        
        vectorstore = self.indices[strategy_name]
        docs = vectorstore.similarity_search(query, k=k)
        return [doc.page_content for doc in docs]

    def save_indices(self, path: str):
        """Saves all built indices to disk."""
        for name, vs in self.indices.items():
            vs.save_local(os.path.join(path, name))

    def load_indices(self, path: str):
        """Loads indices from disk."""
        for name in os.listdir(path):
            idx_path = os.path.join(path, name)
            if os.path.isdir(idx_path):
                self.indices[name] = FAISS.load_local(idx_path, self.embeddings, allow_dangerous_deserialization=True)
