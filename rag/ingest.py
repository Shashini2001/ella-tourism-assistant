import os
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
PERSIST_DIR = Path(__file__).resolve().parent.parent / "chroma_db"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def load_documents():
    loader = DirectoryLoader(
        str(DATA_DIR),
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )
    docs = loader.load()

    for doc in docs:
        parent_folder = Path(doc.metadata["source"]).parent.name
        doc.metadata["category"] = parent_folder
        doc.metadata["filename"] = Path(doc.metadata["source"]).name

    return docs


def build_vectorstore():
    print(f"Loading documents from {DATA_DIR} ...")
    docs = load_documents()
    print(f"Loaded {len(docs)} documents.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80,
    )
    chunks = splitter.split_documents(docs)
    print(f"Split into {len(chunks)} chunks.")

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    print("Embedding and storing in Chroma ...")
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(PERSIST_DIR),
    )
    vectordb.persist()
    print(f"Done. Vector store saved to {PERSIST_DIR}")


if __name__ == "__main__":
    build_vectorstore()
