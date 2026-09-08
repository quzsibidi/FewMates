import os
import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

# Initialize Persistent ChromaDB Client
client = chromadb.PersistentClient(path="./chroma_db")
embedding_fn = embedding_functions.DefaultEmbeddingFunction()

collection = client.get_or_create_collection(
    name="academic_docs",
    embedding_function=embedding_fn
)

def process_and_index_pdf(file_path: str, filename: str) -> int:
    reader = PdfReader(file_path)
    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"
            
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = text_splitter.split_text(full_text)
    
    ids = [f"{filename}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"source": filename, "chunk_id": i} for i in range(len(chunks))]
    
    collection.add(
        documents=chunks,
        ids=ids,
        metadatas=metadatas
    )
    return len(chunks)

def query_rag_context(query: str, n_results: int = 3) -> str:
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    documents = results.get("documents", [[]])[0]
    if not documents:
        return ""
        
    return "\n---\n".join(documents)