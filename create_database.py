import os
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# =========================
# CONFIG
# =========================
PDF_PATH = "data/nutrition.pdf"
DB_PATH = "vectorstore"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


# =========================
# LOAD PDF
# =========================

print("\n==============================")
print("AI HEALTH ASSISTANT")
print("Creating RAG Database")
print("==============================\n")

print("Loading PDF...")

loader = PyPDFLoader(PDF_PATH)
documents = loader.load()

print(f"PDF pages loaded: {len(documents)}")


# =========================
# SPLIT DOCUMENT
# =========================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)

chunks = text_splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks.")


# =========================
# CREATE EMBEDDINGS
# =========================

print("\nLoading embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)

print("Embedding model loaded.")


# =========================
# CREATE FAISS DATABASE
# =========================

print("\nCreating FAISS vector database...")

db = FAISS.from_documents(
    documents=chunks,
    embedding=embeddings
)

# Create folder if it doesn't exist
os.makedirs(DB_PATH, exist_ok=True)

# Save:
# vectorstore/index.faiss
# vectorstore/index.pkl

db.save_local(DB_PATH)

print("\n==============================")
print("RAG DATABASE CREATED")
print("==============================")
print(f"Database folder: {Path(DB_PATH).absolute()}")
print("\nGenerated files:")

print("✓ vectorstore/index.faiss")
print("✓ vectorstore/index.pkl")