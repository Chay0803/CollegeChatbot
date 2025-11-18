import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, util


from llama_api import ask_ollama

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

load_dotenv()

PDF_PATH = "data1"
DB_DIR = "chroma_digital_icfai"

if not os.path.exists(DB_DIR):
    print("🔹 Embedding Digital ICFAI PDF...")

    documents = []
    for filename in os.listdir(PDF_PATH):
        if filename.endswith(".pdf"):
            pdf_loader = PyMuPDFLoader(os.path.join(PDF_PATH, filename))
            documents.extend(pdf_loader.load())

    splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
    chunks = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")      
    vectorstore = Chroma.from_documents(chunks, embedding=embeddings, persist_directory=DB_DIR)
    vectorstore.persist()
    print("✅ Database created successfully.")
else:
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)

retriever_digital_icfai = vectorstore.as_retriever(search_kwargs={"k": 6})
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("digital_icfai_chat.html", {"request": request})


@app.post("/digital_icfai_chat", response_class=JSONResponse)
async def digital_icfai_chat_post(user_message: str = Form(...)):
    query = user_message.strip()
    docs = retriever_digital_icfai.get_relevant_documents(query)
    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""
You are the **Digital ICFAI Assistant**, a knowledgeable yet concise guide for the university's ERP and website.

Your job:
- Use ONLY the provided context to answer the user’s question.
- Respond naturally and conversationally, not like a document.
- Give the most direct, relevant answer possible.
- DO NOT repeat section titles or long lists unless explicitly requested.
- If the question is about how to do something, focus only on the steps.
- If the user asks for details about one item (e.g., a specific module or page),
  ignore unrelated or extra information.
- Please elaborate slightly on the following answer, adding helpful examples or short background if relevant.
When users ask "Chatbot", explain its purpose and benefits, not its technology.
Keep tone informative and natural.
Context:
{context}

Question: {query}

Answer (detailed, structured, and student-friendly — include helpful background, context, and related facts if they enrich understanding. 
Use short paragraphs and bullet points where possible):
"""
    try:
        answer = ask_ollama(prompt)
        

    except Exception as e:
        answer = f"⚠️ Error generating answer: {e}"

    return {"answer": answer}


@app.get("/digital_icfai_chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("digital_icfai_chat.html", {"request": request})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
