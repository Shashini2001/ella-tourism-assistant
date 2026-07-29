from pathlib import Path
from functools import lru_cache

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

PERSIST_DIR = Path(__file__).resolve().parent.parent / "chroma_db"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def _get_vectordb():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return Chroma(
        persist_directory=str(PERSIST_DIR),
        embedding_function=embeddings,
    )


def retrieve(query: str, category: str | None = None, k: int = 4):
    
    vectordb = _get_vectordb()

    search_kwargs = {"k": k}
    if category:
        results = vectordb.similarity_search(
            query, k=k, filter={"category": category}
        )
    else:
        results = vectordb.similarity_search(query, k=k)

    return [
        {
            "text": doc.page_content,
            "source": doc.metadata.get("filename", "unknown"),
            "category": doc.metadata.get("category", "unknown"),
        }
        for doc in results
    ]
