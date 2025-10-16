import os
from langchain.document_loaders import PyPDFLoader

docs_path = "C:\\Users\\krishna\\Downloads\\ifhe-chatbot-1-master\\ifhe-chatbot-1-master\\data"

all_docs = []
for file in os.listdir(docs_path):
    if file.endswith(".pdf"):  # Adjust for your file types
        loader = PyPDFLoader(os.path.join(docs_path, file))
        docs = loader.load()
        print(f"{file} -> {len(docs)} pages loaded")
        all_docs.extend(docs)

print(f"Total documents loaded: {len(all_docs)}")
