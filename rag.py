from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

DB_PATH = "vectorstore"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )


def load_rag():
    embeddings = get_embeddings()

    db = FAISS.load_local(
        DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    return db


def search_knowledge(query, k=4):
    """
    Search the nutrition knowledge base using semantic similarity.
    Returns the most relevant documents.
    """

    db = load_rag()

    results = db.similarity_search(
        query,
        k=k
    )

    return results