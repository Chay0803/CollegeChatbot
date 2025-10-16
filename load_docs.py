import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

DATA_DIR = os.environ.get("DATA_DIR", "data1/final_chatbot_data.pdf")
PERSIST_DIR = os.environ.get("PERSIST_DIR", "chroma_db")


def build_vectorstore():
    all_docs = []

    # Load all PDFs
    for file in os.listdir(DATA_DIR):
        if file.lower().endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(DATA_DIR, file))
            docs = loader.load()
            print(f"{file} -> {len(docs)} pages loaded")
            all_docs.extend(docs)

    print(f"Total documents loaded: {len(all_docs)}")
    if not all_docs:
        raise ValueError("No documents found in data folder!")

    # Deduplicate pages by text
    seen, unique_docs = set(), []
    for d in all_docs:
        if d.page_content.strip() not in seen:
            seen.add(d.page_content.strip())
            unique_docs.append(d)

    print(f"After deduplication: {len(unique_docs)} pages remain")

    # Split long pages into smaller chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunked_docs = splitter.split_documents(unique_docs)
    print(f"After splitting: {len(chunked_docs)} chunks ready for embedding")

    # Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Create and persist vectorstore
    vectorstore = Chroma.from_documents(chunked_docs, embeddings, persist_directory=PERSIST_DIR)
    print("Vectorstore created and persisted!")

    return vectorstore


# Load existing vectorstore if present, else create new
if os.path.exists(PERSIST_DIR) and os.listdir(PERSIST_DIR):
    print("Loading existing Chroma vectorstore...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
else:
    print("Creating new Chroma vectorstore...")
    vectorstore = build_vectorstore()

print("Vectorstore contains", vectorstore._collection.count(), "vectors")


def get_vectorstore():
    return vectorstore
