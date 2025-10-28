# import os
# from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_community.vectorstores import Chroma
# from langchain.text_splitter import RecursiveCharacterTextSplitter

# DATA_DIR = os.environ.get("DATA_DIR", "data")
# PERSIST_DIR = os.environ.get("PERSIST_DIR", "chroma_db")


# def build_vectorstore():
#     all_docs = []

#     # Load all PDFs
#     for file in os.listdir(DATA_DIR):
#         if file.lower().endswith(".pdf"):
#             loader = PyPDFLoader(os.path.join(DATA_DIR, file))
#             docs = loader.load()
#             print(f"{file} -> {len(docs)} pages loaded")
#             all_docs.extend(docs)

#     print(f"Total documents loaded: {len(all_docs)}")
#     if not all_docs:
#         raise ValueError("No documents found in data folder!")

#     # Deduplicate pages by text
#     seen, unique_docs = set(), []
#     for d in all_docs:
#         if d.page_content.strip() not in seen:
#             seen.add(d.page_content.strip())
#             unique_docs.append(d)

#     print(f"After deduplication: {len(unique_docs)} pages remain")

#     # Split long pages into smaller chunks
#     splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
#     chunked_docs = splitter.split_documents(unique_docs)
#     print(f"After splitting: {len(chunked_docs)} chunks ready for embedding")

#     # Embeddings
#     embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

#     # Create and persist vectorstore
#     vectorstore = Chroma.from_documents(chunked_docs, embeddings, persist_directory=PERSIST_DIR)
#     print("Vectorstore created and persisted!")

#     return vectorstore


# # Load existing vectorstore if present, else create new
# if os.path.exists(PERSIST_DIR) and os.listdir(PERSIST_DIR):
#     print("Loading existing Chroma vectorstore...")
#     embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
#     vectorstore = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
# else:
#     print("Creating new Chroma vectorstore...")
#     vectorstore = build_vectorstore()

# print("Vectorstore contains", vectorstore._collection.count(), "vectors")


# def get_vectorstore():
#     return vectorstore

import os
import json
from datetime import datetime
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

DATA_DIR = os.environ.get("DATA_DIR", "data")
PERSIST_DIR = os.environ.get("PERSIST_DIR", "chroma_db")
META_FILE = os.path.join(PERSIST_DIR, "metadata.json")


def load_metadata():
    """Load metadata tracking which files are already embedded."""
    if os.path.exists(META_FILE):
        with open(META_FILE, "r") as f:
            return json.load(f)
    return {}


def save_metadata(metadata):
    """Save updated metadata after new embeddings are added."""
    os.makedirs(PERSIST_DIR, exist_ok=True)
    with open(META_FILE, "w") as f:
        json.dump(metadata, f, indent=4)


def get_modified_files(metadata):
    """Return a list of new or modified files."""
    modified_files = []
    for file in os.listdir(DATA_DIR):
        if not file.lower().endswith((".pdf", ".docx")):
            continue

        file_path = os.path.join(DATA_DIR, file)
        mod_time = os.path.getmtime(file_path)

        # Include if new or modified since last embedding
        if file not in metadata or metadata[file]["mod_time"] < mod_time:
            modified_files.append((file, mod_time))
    return modified_files


def load_docs(file_path):
    """Load PDF or DOCX files."""
    if file_path.lower().endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.lower().endswith(".docx"):
        loader = Docx2txtLoader(file_path)
    else:
        return []
    return loader.load()


def process_and_embed(files_to_process, metadata, vectorstore=None):
    """Split, embed, and optionally update the Chroma store."""
    if not files_to_process:
        print("✅ No new or modified files to embed.")
        return vectorstore

    all_docs = []
    for file, mod_time in files_to_process:
        path = os.path.join(DATA_DIR, file)
        docs = load_docs(path)
        print(f"📄 {file} -> {len(docs)} pages loaded")

        # Split into smaller chunks
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunked_docs = splitter.split_documents(docs)
        print(f"✂️  {file} -> {len(chunked_docs)} chunks ready for embedding")
        all_docs.extend(chunked_docs)

        # Update metadata
        metadata[file] = {"mod_time": mod_time, "processed_at": datetime.now().isoformat()}

    # Create embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Create or update Chroma store
    if vectorstore:
        vectorstore.add_documents(all_docs)
        vectorstore.persist()
        print("✅ Vectorstore updated with new documents!")
    else:
        vectorstore = Chroma.from_documents(all_docs, embeddings, persist_directory=PERSIST_DIR)
        vectorstore.persist()
        print("✅ New vectorstore created and persisted!")

    save_metadata(metadata)
    print("💾 Metadata updated and saved!")

    return vectorstore


def main():
    # Load existing metadata and vectorstore if present
    metadata = load_metadata()

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    if os.path.exists(PERSIST_DIR) and os.listdir(PERSIST_DIR):
        print("🔍 Loading existing Chroma vectorstore...")
        vectorstore = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
    else:
        print("🚀 No existing vectorstore found. Creating new one...")
        vectorstore = None

    # Check for new or modified files
    files_to_process = get_modified_files(metadata)

    # Process and embed
    vectorstore = process_and_embed(files_to_process, metadata, vectorstore)

    if vectorstore:
        print(f"📦 Vectorstore now contains {vectorstore._collection.count()} vectors.")
    else:
        print("⚠️ No vectorstore created (no valid documents).")


if __name__ == "__main__":
    main()
