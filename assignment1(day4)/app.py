import streamlit as st
import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from typing import List
from langchain_core.documents import Document

st.set_page_config(page_title="Enterprise Knowledge Copilot", layout="wide")

st.title("🛡️ Enterprise Knowledge Copilot")
st.markdown("Hybrid Search (Vector + Keyword) with Role-Based Access Control (RBAC)")

# Sidebar for Configuration
with st.sidebar:
    st.header("Configuration")
    groq_api_key = st.text_input("Groq API Key", type="password", help="Enter your Groq API Key here")
    
    st.header("RBAC Settings")
    user_role = st.selectbox("Your Current Role", ["Employee", "Manager", "HR", "Admin"])
    
    st.header("Data Ingestion")
    uploaded_files = st.file_uploader("Upload internal knowledge files", type=["pdf", "txt"], accept_multiple_files=True)
    doc_access_level = st.selectbox("Document Access Level", ["Employee", "Manager", "HR", "Admin"], help="Minimum role required to view these documents.")
    
    process_docs = st.button("Process & Ingest Documents")

# Initialize Session State
if "bm25_retriever" not in st.session_state:
    st.session_state.bm25_retriever = None
if "all_splits" not in st.session_state:
    st.session_state.all_splits = []

def get_embeddings():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

@st.cache_resource
def init_vector_store():
    # Store locally
    persist_dir = "./chroma_db"
    return Chroma(persist_directory=persist_dir, embedding_function=get_embeddings())

vector_store = init_vector_store()

if process_docs and uploaded_files:
    if not groq_api_key:
        st.warning("Please provide a Groq API Key First.")
    else:
        with st.spinner("Processing & Ingesting documents..."):
            all_docs = []
            for uploaded_file in uploaded_files:
                # Save file to a temporary directory to be processed by LangChain loaders
                temp_dir = tempfile.mkdtemp()
                temp_path = os.path.join(temp_dir, uploaded_file.name)
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                if uploaded_file.name.endswith(".pdf"):
                    loader = PyPDFLoader(temp_path)
                else:
                    loader = TextLoader(temp_path)
                
                docs = loader.load()
                
                # Metadata Injection for RBAC
                for doc in docs:
                    doc.metadata["access_level"] = doc_access_level
                    doc.metadata["source"] = uploaded_file.name
                    
                all_docs.extend(docs)
                
            # Split documents
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            splits = text_splitter.split_documents(all_docs)
            
            st.session_state.all_splits.extend(splits)
            
            # Update Vector Store (Chroma)
            vector_store.add_documents(splits)
            
            # Update BM25 Retriever
            st.session_state.bm25_retriever = BM25Retriever.from_documents(st.session_state.all_splits)
            st.session_state.bm25_retriever.k = 3
            
            st.success(f"Successfully ingested {len(splits)} chunks with access level strictness: {doc_access_level}")

st.header("Chat Interface")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Define hierarchy of roles (Admin can see everything, Employee can only see Employee docs)
valid_roles = {
    "Employee": ["Employee"],
    "Manager": ["Employee", "Manager"],
    "HR": ["Employee", "HR"],
    "Admin": ["Employee", "Manager", "HR", "Admin"]
}

class FilteredBM25Retriever:
    """Wrapper to add post-retrieval metadata filtering for BM25 since it doesn't natively support it like Chroma."""
    def __init__(self, base_retriever, allowed_roles):
        self.base_retriever = base_retriever
        self.allowed_roles = allowed_roles
        
    def invoke(self, query: str) -> List[Document]:
        docs = self.base_retriever.invoke(query)
        # Filter docs based on RBAC rule
        return [d for d in docs if d.metadata.get("access_level", "Employee") in self.allowed_roles]
        
    async def ainvoke(self, query: str) -> List[Document]:
        return self.invoke(query)

class CustomEnsembleRetriever:
    def __init__(self, retrievers, weights):
        self.retrievers = retrievers
        self.weights = weights

    def invoke(self, query):
        doc_scores = {}
        doc_contents = {}
        for i, retriever in enumerate(self.retrievers):
            try:
                docs = retriever.invoke(query) if hasattr(retriever, 'invoke') else retriever.get_relevant_documents(query)
            except Exception:
                docs = []
            for rank, doc in enumerate(docs):
                score = self.weights[i] / (rank + 60)
                content_hash = hash(doc.page_content)
                if content_hash not in doc_scores:
                    doc_scores[content_hash] = 0
                    doc_contents[content_hash] = doc
                doc_scores[content_hash] += score
        sorted_hashes = sorted(doc_scores, key=doc_scores.get, reverse=True)
        return [doc_contents[h] for h in sorted_hashes[:4]]

if prompt := st.chat_input("Ask a question based on your documents..."):
    if not groq_api_key:
        st.warning("Please enter your Groq API Key in the sidebar.")
        st.stop()
        
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if not st.session_state.bm25_retriever or not vector_store:
            st.info("No documents are available in the index yet. Please upload and process documents from the sidebar.")
            st.stop()

        # RBAC Filter for Vector Store - Enforcing security at the DB level
        allowed_roles = valid_roles.get(user_role, ["Employee"])
        search_filter = {"access_level": {"$in": allowed_roles}}
        
        # Build Retrievers
        try:
            vector_retriever = vector_store.as_retriever(
                search_kwargs={"k": 3, "filter": search_filter}
            )
            
            filtered_bm25 = FilteredBM25Retriever(st.session_state.bm25_retriever, allowed_roles)
            
            # Hybrid Ensemble Retriever combining Vector (Semantic) + BM25 (Keyword)
            custom_retriever = CustomEnsembleRetriever(
                retrievers=[vector_retriever, filtered_bm25], weights=[0.6, 0.4]
            )
            ensemble_retriever = RunnableLambda(custom_retriever.invoke)
        except Exception as e:
            st.error(f"Error initializing retrievers: {e}")
            st.stop()

        try:
            llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.1-8b-instant")
        except Exception as e:
            st.error(f"Failed to initialize Groq LLM: {e}. Check your API Key.")
            st.stop()
            
        system_prompt = (
            "You are an enterprise AI assistant. You answer questions strictly based on the retrieved context below.\n"
            "If the answer is not in the context, say 'I do not have access to this information.'\n\n"
            "Context:\n{context}"
        )
        
        prompt_tmpla = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])
        
        with st.spinner("Searching securely across your knowledge base..."):
            try:
                # Manual Retrieval and Generation to avoid deprecated/missing chain modules
                retrieved_docs = ensemble_retriever.invoke(prompt)
                context_str = "\n\n".join([doc.page_content for doc in retrieved_docs])
                formatted_prompt = prompt_tmpla.format_messages(input=prompt, context=context_str)
                llm_response = llm.invoke(formatted_prompt)
                
                response = {"answer": llm_response.content, "context": retrieved_docs}
                answer = response["answer"]
                
                # Extract and deduplicate sources
                sources = set()
                if "context" in response and response["context"]:
                    for doc in response["context"]:
                        source = doc.metadata.get('source', 'Unknown Document')
                        acc_level = doc.metadata.get('access_level', 'Unknown')
                        sources.add(f"{source} (Level: {acc_level})")
                        
                if sources:
                    answer += f"\n\n**Sources:** {', '.join(sources)}"
                else:
                    answer += f"\n\n**Sources:** No specific context matched."
                
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"An error occurred during query execution: {e}")
