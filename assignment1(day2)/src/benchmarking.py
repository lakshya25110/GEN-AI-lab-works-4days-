import os
import json
import time
from src.ingestion import DocumentProcessor
from src.chunking import ChunkingEngine
from src.retriever import VectorRetriever
from src.generator import Generator
from src.evaluation import RAGEvaluator

# USER PROVIDED GROQ KEY
GROQ_API_KEY = "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"
PDF_PATH = r"c:\lakshya documents\assignment1(day2)\temp_manual.pdf"

TEST_QUESTIONS = [
    "What are the specific datasets used in the Retail Analytics Platform?",
    "What is the schema for the Sales Transactions dataset?",
    "How is environment separation handled in the CI/CD pipeline?",
    "What are the constraints on analytical queries via SQL endpoints?",
    "Who owns the intellectual property of this document?"
]

def run_benchmarking():
    # 1. Ingestion
    processor = DocumentProcessor()
    text = processor.process_document(PDF_PATH)
    
    # 2. Setup Engines
    chunking_engine = ChunkingEngine()
    retriever = VectorRetriever()
    generator = Generator(api_key=GROQ_API_KEY)
    evaluator = RAGEvaluator(generator)
    
    strategies = {
        "Fixed-Size": chunking_engine.fixed_size_chunking(text),
        "Semantic": chunking_engine.semantic_chunking(text),
        "Sliding Window": chunking_engine.sliding_window_chunking(text)
    }
    
    # Build Indices
    for name, chunks in strategies.items():
        retriever.build_index(name, chunks)
        
    results = []
    
    for question in TEST_QUESTIONS:
        q_result = {"question": question, "strategies": {}}
        for name in strategies.keys():
            start_time = time.time()
            context = retriever.retrieve(question, name)
            answer = generator.generate_answer(question, context)
            latency = time.time() - start_time
            
            # Eval
            evals = evaluator.run_full_eval(question, answer, context)
            
            q_result["strategies"][name] = {
                "answer": answer,
                "latency": latency,
                "faithfulness": evals["faithfulness"].get("score", 0),
                "relevance": evals["relevance"].get("score", 0)
            }
        results.append(q_result)
        
    # Save results to a temporary JSON for report generation
    with open("benchmark_results.json", "w") as f:
        json.dump(results, f, indent=4)
    
    print("Benchmarking Complete. Results saved to benchmark_results.json")

if __name__ == "__main__":
    run_benchmarking()
