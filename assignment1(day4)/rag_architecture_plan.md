# Enterprise Knowledge Copilot Architecture Plan

This document outlines the design and deployment strategy for an open-source, scalable, and cost-efficient Enterprise Knowledge Copilot utilizing a Retrieval-Augmented Generation (RAG) architecture.

## 1. System Architecture

The architecture is designed to be lightweight, modular, and entirely open-source, ensuring data privacy and zero vendor lock-in.

-   **Orchestration Framework:** **LangChain**
    *   *Reasoning:* Widely adopted, extensive integrations with document loaders, and robust support for hybrid search and chaining.
-   **Embedding Model:** **SentenceTransformers (`all-MiniLM-L6-v2`)**
    *   *Reasoning:* Extremely fast, operates well on CPUs, and provides excellent baseline semantic search capabilities without requiring GPUs.
-   **Vector Database (Dense Search):** **Chroma**
    *   *Reasoning:* Open-source, easy to run locally or as a lightweight Docker container, and integrates seamlessly with LangChain.
-   **Keyword Database (Sparse Search):** **Whoosh or BM25**
    *   *Reasoning:* Whoosh is a fast, pure Python search engine library that requires no external service. Alternatively, LangChain's local `BM25Retriever` allows entirely in-memory BM25 indexing for small datasets.
-   **Large Language Model (LLM):** **Ollama (running `llama3` 8B or `mistral`)**
    *   *Reasoning:* Ollama provides a simple containerized approach to running quantized opens-source LLMs locally, ensuring zero data egress.
-   **API & Backend:** **FastAPI**
    *   *Reasoning:* High performance, asynchronous Python web framework used to expose endpoints, handle JWT authentication, and route RAG queries.

## 2. Data Ingestion & Indexing

A robust pipeline is required to prepare documents for the retrieval system.

-   **Document Loaders:** Use LangChain's `PyPDFLoader` for PDFs, `UnstructuredWordDocumentLoader` for Word files, and `TextLoader` for plaintext.
-   **Text Splitting:** Use `RecursiveCharacterTextSplitter`.
    *   *Configuration:* Set chunk size to ~1000 characters with an overlap of ~200 characters to ensure context isn't lost at the boundaries.
-   **Metadata Extraction:** Tag each chunk with metadata, critically:
    *   `source_file`: The origin document.
    *   `access_level`: The minimal role required to view this document (required for RBAC).
-   **Dual Indexing:**
    *   Pass the chunk text to SentenceTransformers to generate vector embeddings and index them in **Chroma** alongside the metadata.
    *   Index the exact text chunks in the **BM25 Retirever** (or Whoosh) to allow for keyword searching.

## 3. Hybrid Search Design

Hybrid search combines the semantic understanding of vector embeddings with the exact keyword matching of traditional search.

1.  **Dual Retrieval Execution:** When a query arrives, send it simultaneously to both the Chroma Vector DB (semantic search) and the BM25 system (keyword search). Request top-K results from both.
2.  **Ensemble Retriever:** Use LangChain's `EnsembleRetriever`.
3.  **Reciprocal Rank Fusion (RRF):** The `EnsembleRetriever` merges the results using RRF. It recalculates the score of each document based on its rank in both the vector and keyword result sets, smoothing out edge cases where a user searches for a specific internal acronym (best found by BM25) vs. a general concept (best found by Chroma).
4.  **Context Window Injection:** The top deduplicated results are injected into the contextual prompt for the LLM.

## 4. RBAC Implementation

Role-Based Access Control (RBAC) ensures employees only receive answers based on documents they are permitted to view.

-   **Authentication:** Use **JWT (JSON Web Tokens)** managed by the FastAPI backend. Users log in, and the backend verifies credentials against a lightweight store (e.g., SQLite or an internal directory) and issues a JWT.
-   **Token Payload:** The JWT payload contains the user's role (e.g., `role: "HR"`, `role: "Engineering"`, `role: "General"`).
-   **Retrieval Filtering:**
    *   When the API receives a chat query, the backend decrypts the JWT to identify the user's role.
    *   The retrieval step injects this role as a **Metadata Filter**.
    *   *Example:* When querying Chroma, apply a `where` clause: `{"access_level": {"$in": ["General", user_role]}}`.
    *   By filtering at the database layer *before* retrieval, we guarantee the LLM never sees restricted data, preventing unauthorized information generation.

## 5. Cost & Simplicity Optimization

-   **Zero Cloud AI Costs:** By utilizing local embeddings (SentenceTransformers) and local LLMs (Ollama), there are no payload or per-token charges.
-   **Minimal Infrastructure:** Avoiding heavyweight tools like Elasticsearch in favor of Python-native BM25 and Chroma drastically reduces the RAM, configuration, and maintainability overhead.
-   **Hardware Efficiency:** The `all-MiniLM-L6-v2` embedding model runs blazingly fast on CPUs. A quantized 8B LLM (like Mistral v0.3 or Llama 3) can run on low-end GPUs or even modern consumer hardware.

## 6. Deployment Guide (Docker-based)

A multi-container `docker-compose` setup is the simplest path to deployment.

```yaml
version: '3.8'

services:
  fastapi-backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - OLLAMA_HOST=http://ollama:11434
      - CHROMA_DB_URL=http://chroma:8000
    depends_on:
      - chroma
      - ollama

  chroma:
    image: chromadb/chroma:latest
    ports:
      - "8001:8000"
    volumes:
      - chroma-data:/chroma/chroma

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama-data:/root/.ollama
    # Command to pull model on boot if not exists
    command: >-
      bash -c "ollama serve & sleep 5 && ollama pull llama3 && wait"

volumes:
  chroma-data:
  ollama-data:
```

**Setup Steps:**
1.  Install Docker and Docker Compose.
2.  Place the `docker-compose.yml` and the FastAPI source code in the directory.
3.  Run `docker-compose up -d`.
4.  Optionally, expose the FastAPI endpoint locally or map it securely via an Nginx reverse proxy.

## 7. Risks & Best Practices

-   **Risk: Hallucinations:** Even with RAG, LLMs can hallucinate.
    *   *Mitigation:* Use rigorous prompting (e.g., "If the answer is not contained in the provided context, state 'I do not have enough information'.").
-   **Risk: Scale Limitations (BM25):** In-memory BM25 fails above gigabytes of text.
    *   *Path forward:* If the document corpus grows massively, migrate the BM25 implementation to an Elasticsearch or OpenSearch container.
-   **Best Practice: Iterative Chunking:** Monitor queries. If the model frequently struggles to comprehend tables or long paragraphs, experiment with specific splitters (like LangChain's MarkdownHeaderTextSplitter) instead of generic character splitting.
-   **Best Practice: Secret Management:** Never hardcode JWT secret keys; rely on `.env` files and secure secret managers in production.
