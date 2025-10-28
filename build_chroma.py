import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

DATA_DIR = os.environ.get("DATA_DIR", "data")

# Load all PDFs and DOCX files
files = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.endswith((".pdf", ".docx"))]

documents = []
for file in files:
    if file.lower().endswith(".pdf"):
        loader = PyPDFLoader(file)
    elif file.lower().endswith(".docx"):
        loader = Docx2txtLoader(file)
    else:
        continue
    print(f"📄 Loading {os.path.basename(file)} ...")
    documents.extend(loader.load())

print(f"✅ Loaded {len(documents)} documents total.")

# Split into smaller chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = splitter.split_documents(documents)
print(f"✂️ Split into {len(chunks)} chunks.")

# Create embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Build and persist vectorstore
vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="chroma_db")
vectorstore.persist()

print("✅ Vectorstore built successfully with DOCX and PDF files.")
