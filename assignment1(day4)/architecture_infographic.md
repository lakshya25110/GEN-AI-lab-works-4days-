# Enterprise RAG Copilot - Architecture Infographic

The following diagram illustrates the complete end-to-end data flow for both the **Document Ingestion** phase and the **Hybrid Search Retrieval** phase of the Enterprise Knowledge Copilot.

```mermaid
graph TD
    %% Styling Classes
    classDef user fill:#6366f1,stroke:#fff,stroke-width:2px,color:#fff,rx:20,ry:20;
    classDef doc fill:#10b981,stroke:#fff,stroke-width:2px,color:#fff;
    classDef db fill:#f59e0b,stroke:#fff,stroke-width:2px,color:#fff,shape:cylinder;
    classDef ai fill:#ec4899,stroke:#fff,stroke-width:2px,color:#fff;
    classDef process fill:#3b82f6,stroke:#fff,stroke-width:2px,color:#fff;

    %% Data Ingestion Phase
    subgraph Ingestion["1️⃣ Data Ingestion & Indexing Pipeline"]
        direction TB
        A1["📄 Internal Documents"]:::doc -->|Upload| A2["⚙️ LangChain Loaders"]:::process
        A2 --> A3["✂️ Recursive Text Splitting"]:::process
        A3 --> A4["🏷️ RBAC Metadata Injection"]:::process
        
        A4 -->|Generate Embeddings| B1["🧠 SentenceTransformers"]:::ai
        B1 -->|Store Dense Vectors| DB1[("🗄️ ChromaDB\n(Vector Store)")]:::db
        
        A4 -->|Store Raw Text| DB2[("🔍 BM25\n(Keyword Store)")]:::db
    end

    %% Retrieval & Chat Phase
    subgraph Chat["2️⃣ Hybrid Search & RAG Generation"]
        direction TB
        U1(("👤 User Input")):::user -->|Query| R1{"🔐 RBAC Filter"}:::process
        
        R1 -->|Inject Role + Search| DB1
        R1 -->|Keyword Search| DB2

        DB1 -->|Semantic Results| S1{"⚖️ Ensemble Retriever"}:::process
        DB2 -->|Keyword Results| S1

        S1 -->|RRF Scoring / Merge| C1["🧩 Prompt Templating"]:::process
        
        C1 -->|Context + Query| AI1(("🤖 Groq: Llama 3.1")):::ai
        AI1 -->|Synthesized Response| U2(("✨ Final Answer")):::user
    end
```

### Key Highlights
* **Dual Indexing:** Notice how every document goes into **two separate databases** (ChromaDB for "meaning" and BM25 for "exact keywords").
* **Early RBAC Filtering:** The `RBAC Filter` step happens *before* the vector database retrieves the context. This prevents the system from accidentally surfacing restricted data into the memory of the LLM. 
* **Ensemble Fusion:** The `Ensemble Retriever` takes the outputs from both the vector data and keyword data, applying *Reciprocal Rank Fusion (RRF)* to mathematically select the best combination of results.
