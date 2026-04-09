from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List, Dict
import time

class ChunkingEngine:
    def __init__(self, embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)

    def fixed_size_chunking(self, text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        return splitter.split_text(text)

    def semantic_chunking(self, text: str) -> List[str]:
        # Semantic chunker splits text based on embedding drift
        splitter = SemanticChunker(self.embeddings, breakpoint_threshold_type="percentile")
        # splitter split_text expects a list of strings sometimes depending on version, 
        # but usually a single string.
        docs = splitter.create_documents([text])
        return [doc.page_content for doc in docs]

    def sliding_window_chunking(self, text: str, window_size: int = 800, step_size: int = 400) -> List[str]:
        # Simple sliding window approach
        chunks = []
        for i in range(0, len(text), step_size):
            chunk = text[i:i + window_size]
            chunks.append(chunk)
            if i + window_size >= len(text):
                break
        return chunks

    def compare_strategies(self, text: str) -> Dict[str, Dict]:
        results = {}
        
        # Fixed
        start = time.time()
        fixed = self.fixed_size_chunking(text)
        results["Fixed-Size"] = {
            "count": len(fixed),
            "avg_len": sum(len(c) for c in fixed) / len(fixed) if fixed else 0,
            "latency": time.time() - start
        }

        # Semantic
        start = time.time()
        semantic = self.semantic_chunking(text)
        results["Semantic"] = {
            "count": len(semantic),
            "avg_len": sum(len(c) for c in semantic) / len(semantic) if semantic else 0,
            "latency": time.time() - start
        }

        # Sliding Window
        start = time.time()
        sliding = self.sliding_window_chunking(text)
        results["Sliding Window"] = {
            "count": len(sliding),
            "avg_len": sum(len(c) for c in sliding) / len(sliding) if sliding else 0,
            "latency": time.time() - start
        }

        return results
