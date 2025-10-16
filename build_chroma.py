import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


DATA_DIR = os.environ.get("DATA_DIR", "data1")
pdf_files = [os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.endswith(".pdf")]

documents = []
for file in pdf_files:
    loader = PyPDFLoader(file)
    documents.extend(loader.load())

splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=100)
chunks = splitter.split_documents(documents)


embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vectorstore = Chroma.from_documents(
    chunks,
    embedding=embeddings,
    persist_directory="chroma_db"   
)
vectorstore.persist()

print("Vectorstore built and saved in 'chroma_db'")
