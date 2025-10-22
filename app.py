# import streamlit as st
# import pandas as pd
# from llama_api import ask_ollama
# from course_matcher import match_courses
# from load_docs import get_vectorstore

# st.set_page_config(page_title="IFHE Chatbot", layout="wide")

# st.markdown(
#     """
#     <div style="background-color:#003366; padding: 18px 0; border-radius: 10px; text-align: center; margin-bottom: 30px;">
#         <span style="color: white; font-size: 2.2rem; font-weight: bold; letter-spacing: 1px;">
#             IFHE College Chatbot
#         </span>
#     </div>
#     """,
#     unsafe_allow_html=True
# )

# st.markdown("""
#     <style>
#     body { background-color: #f4f8fb; }
#     .stTabs [data-baseweb="tab-list"] { background: #e6eef7; border-radius: 8px; border: 1px solid #003366; padding: 4px; }
#     .stTabs [data-baseweb="tab"] { color: #003366; font-weight: 600; }
#     .stTabs [aria-selected="true"] { background: #003366 !important; color: #fff !important; border-radius: 6px 6px 0 0; }
#     h1, .stMarkdown h1 { color: #003366; }
#     .stButton>button { background-color: #003366; color: #fff; border-radius: 6px; border: none; font-weight: 600; }
#     .stButton>button:hover { background-color: #00509e; color: #fff; }
#     </style>
# """, unsafe_allow_html=True)

# st.markdown('<div class="main">', unsafe_allow_html=True)

# # Load Chroma vectorstore and convert to retriever
# retriever = get_vectorstore().as_retriever()

# def normalize_query(q):
#     q = q.strip().lower()
#     if "admission" in q:
#         return "What is the admission process and important deadlines?"
#     elif "fee" in q:
#         return "What is the fee structure?"
#     elif "calendar" in q:
#         return "Show the academic calendar and schedule"
#     elif "hostel" in q:
#         return "What are the hostel and transport facilities?"
#     elif "founder" in q:
#         return "Who is the founder of IFHE?"
#     return q

# tab1, tab2, tab3 = st.tabs(["Ask the Chatbot", "Course Recommender", "Employee Details"])

# # Tab 1: Chatbot
# with tab1:
#     question = st.text_input("Enter your question:")
#     if st.button("Ask"):
#         if question:
#             with st.spinner("Reading documents and generating response..."):
#                 query = normalize_query(question)
#                 docs = retriever.get_relevant_documents(query)
#                 context = "\n\n".join([d.page_content for d in docs[:10]])  
#                 prompt = f"""You are an academic assistant for IFHE University. Use the context below to answer the question clearly and helpfully.
#                 List all the courses offered by IFHE University(B.Tech, BBA, BSc, M.Tech, MSc etc) with their specializations.
#                 If the question is about admissions(including Post Gradute) provide details about the process, important dates, eligibility criteria, and required documents.
#                 Provide Urls for more information where relevant. Such as https://ifheindia.org/ or https://ifheindia.org/online-registration/ for admissions.
#                 if the query is about fees, scholarships, placements, campus facilities, faculty, or programs, provide accurate and concise information based on the context.
#                 Provide Urls for more information where relevant. Such as https://ifheindia.org/ or https://ifheindia.org/online-registration/ for admissions.
#                 If information about faculty is asked provide the url https://ifheindia.org/faculty/ for more details. Also mention that Details of faculty members are available on the official website.

# Context:
# {context}

# Question: {question}

# Answer:"""
#                 answer = ask_ollama(prompt)
#                 st.markdown("### Answer:")
#                 st.success(answer)
#         else:
#             st.warning("Please enter a question.")

# # Tab 2: Course Recommender
# with tab2:
#     st.subheader("Course Recommendations")
#     stream = st.selectbox("Select Your Stream", ["", "Science", "Commerce", "Arts"])
#     interest = st.selectbox("Select Your Area of Interest", ["", "Tech", "Law", "Management"])
#     english = st.selectbox("Are you comfortable in English?", ["", "Yes", "No"])
#     tenth = st.number_input("Enter your 10th percentage", min_value=0.0, max_value=100.0, step=0.1)
#     twelfth = st.number_input("Enter your 12th percentage", min_value=0.0, max_value=100.0, step=0.1)

#     if st.button("Recommend Courses"):
#         if stream and interest and english:
#             if tenth < 60 or twelfth < 60:
#                 st.error("You are not eligible. Minimum 60% required in both 10th and 12th.")
#             else:
#                 profile = {
#                     "stream": stream,
#                     "interest": interest,
#                     "english": english,
#                     "10th": tenth,
#                     "12th": twelfth
#                 }
#                 recs = match_courses(profile)
#                 if recs:
#                     for course in recs:
#                         st.success(f"{course}")
#                     st.markdown(
#                         """
#                         <a href="https://ifheindia.org/online-registration" target="_blank">
#                             <button style="background-color:#003366;color:white;padding:10px 24px;border:none;border-radius:6px;font-size:16px;">
#                                 Apply Now
#                             </button>
#                         </a>
#                         """,
#                         unsafe_allow_html=True
#                     )
#                 else:
#                     st.info("No matching courses found.")

# # Tab 3: Employee Lookup
# with tab3:
#     st.subheader("Employee Details Lookup")
#     try:
#         df = pd.read_csv("employees1.csv")
#         search_type = st.radio("Search by:", ["Employee ID", "Salary ≥", "Experience ≥"])

#         if search_type == "Employee ID":
#             empid_input = st.text_input("Enter Employee ID")
#             if st.button("Get Employee by ID"):
#                 if empid_input.strip():
#                     match = df[df["empid"].astype(str) == empid_input.strip()]
#                     if not match.empty:
#                         st.dataframe(match)
#                     else:
#                         st.error("Employee not found.")
#                 else:
#                     st.warning("Please enter a valid Employee ID.")

#         elif search_type == "Salary ≥":
#             salary_input = st.number_input("Enter Minimum Salary", min_value=0)
#             if st.button("Get Employees by Salary"):
#                 filtered = df[df["salary"] >= salary_input]
#                 if not filtered.empty:
#                     st.dataframe(filtered)
#                 else:
#                     st.warning("No employees found with that salary or more.")

#         elif search_type == "Experience ≥":
#             exp_input = st.number_input("Enter Minimum Experience (in years)", min_value=0)
#             if st.button("Get Employees by Experience"):
#                 filtered = df[df["experience"] >= exp_input]
#                 if not filtered.empty:
#                     st.dataframe(filtered)
#                 else:
#                     st.warning("No employees found with that experience or more.")
#     except FileNotFoundError:
#         st.error("employees.csv not found. Please upload it to use this feature.")
#     except Exception as e:
#         st.error(f"Error reading employee data: {e}")

# st.markdown('</div>', unsafe_allow_html=True)


# import streamlit as st
# import pandas as pd
# from llama_api import ask_ollama
# from course_matcher import match_courses
# from load_docs import get_vectorstore

# st.set_page_config(page_title="IFHE Chatbot", layout="wide")

# st.markdown(
#     """
#     <div style="background-color:#003366; padding: 18px 0; border-radius: 10px; text-align: center; margin-bottom: 30px;">
#         <span style="color: white; font-size: 2.2rem; font-weight: bold; letter-spacing: 1px;">
#             IFHE Assitance 
#         </span>
#     </div>
#     """,
#     unsafe_allow_html=True
# )

# st.markdown("""
#     <style>
#     body { background-color: #f4f8fb; }
#     .stTabs [data-baseweb="tab-list"] { background: #e6eef7; border-radius: 8px; border: 1px solid #003366; padding: 4px; }
#     .stTabs [data-baseweb="tab"] { color: #003366; font-weight: 600; }
#     .stTabs [aria-selected="true"] { background: #003366 !important; color: #fff !important; border-radius: 6px 6px 0 0; }
#     h1, .stMarkdown h1 { color: #003366; }
#     .stButton>button { background-color: #003366; color: #fff; border-radius: 6px; border: none; font-weight: 600; }
#     .stButton>button:hover { background-color: #00509e; color: #fff; }
#     </style>
# """, unsafe_allow_html=True)

# st.markdown('<div class="main">', unsafe_allow_html=True)

# # Load Chroma vectorstore and convert to retriever
# retriever = get_vectorstore().as_retriever()

# def normalize_query(q):
#     q = q.strip().lower()
#     if "admission" in q:
#         return "What is the admission process and important deadlines?"
#     elif "fee" in q:
#         return "What is the fee structure?"
#     elif "calendar" in q:
#         return "Show the academic calendar and schedule"
#     elif "hostel" in q:
#         return "What are the hostel and transport facilities?"
#     elif "founder" in q:
#         return "Who is the founder of IFHE?"
#     return q

# tab1, tab2, tab3 = st.tabs(["Ask the Chatbot", "Course Recommender", "Employee Details"])

# # Tab 1: Chatbot
# with tab1:
#     question = st.text_input("Enter your question:")
#     if st.button("Ask"):
#         if question:
#             with st.spinner("Reading documents and generating response..."):
#                 query = normalize_query(question)
#                 docs = retriever.get_relevant_documents(query)
#                 context = "\n\n".join([d.page_content for d in docs[:10]])  
#                 prompt = f"""You are an academic assistant for IFHE University. Use the context below to answer the question clearly and helpfully.
#                 List all the courses offered by IFHE University(B.Tech, BBA, BSc, M.Tech, MSc etc) with their specializations.
#                 If the question is about admissions(including Post Gradute) provide details about the process, important dates, eligibility criteria, and required documents.
#                 Provide Urls for more information where relevant. Such as https://ifheindia.org/ or https://ifheindia.org/online-registration/ for admissions.
#                 if the query is about fees, scholarships, placements, campus facilities, faculty, or programs, provide accurate and concise information based on the context.
#                 Provide Urls for more information where relevant. Such as https://ifheindia.org/ or https://ifheindia.org/online-registration/ for admissions.
#                 If information about faculty is asked provide the url https://ifheindia.org/faculty/ for more details. Also mention that Details of faculty members are available on the official website.
#                 Do not give emojis in the answer.

# Context:
# {context}

# Question: {question}

# Answer:"""
#                 answer = ask_ollama(prompt)
#                 st.markdown("### Answer:")
#                 st.success(answer)
#         else:
#             st.warning("Please enter a question.")

# # Tab 2: Course Recommender
# with tab2:
#     st.subheader("Course Recommendations")
#     stream = st.selectbox("Select Your Stream", ["", "Science", "Commerce", "Arts"])
#     interest = st.selectbox("Select Your Area of Interest", ["", "Tech", "Law", "Management"])
#     english = st.selectbox("Are you comfortable in English?", ["", "Yes", "No"])
#     tenth = st.number_input("Enter your 10th percentage", min_value=0.0, max_value=100.0, step=0.1)
#     twelfth = st.number_input("Enter your 12th percentage", min_value=0.0, max_value=100.0, step=0.1)

#     if st.button("Recommend Courses"):
#         if stream and interest and english:
#             if tenth < 60 or twelfth < 60:
#                 st.error("You are not eligible. Minimum 60% required in both 10th and 12th.")
#             else:
#                 profile = {
#                     "stream": stream,
#                     "interest": interest,
#                     "english": english,
#                     "10th": tenth,
#                     "12th": twelfth
#                 }
#                 recs = match_courses(profile)
#                 if recs:
#                     for course in recs:
#                         st.success(f"{course}")
#                     st.markdown(
#                         """
#                         <a href="https://ifheindia.org/online-registration" target="_blank">
#                             <button style="background-color:#003366;color:white;padding:10px 24px;border:none;border-radius:6px;font-size:16px;">
#                                 Apply Now
#                             </button>
#                         </a>
#                         """,
#                         unsafe_allow_html=True
#                     )
#                 else:
#                     st.info("No matching courses found.")

# # Tab 3: Employee Lookup
# with tab3:
#     st.subheader("Employee Details Lookup")
#     try:
#         df = pd.read_csv("employees1.csv")
#         search_type = st.radio("Search by:", ["Employee ID", "Salary ≥", "Experience ≥"])

#         if search_type == "Employee ID":
#             empid_input = st.text_input("Enter Employee ID")
#             if st.button("Get Employee by ID"):
#                 if empid_input.strip():
#                     match = df[df["empid"].astype(str) == empid_input.strip()]
#                     if not match.empty:
#                         st.dataframe(match)
#                     else:
#                         st.error("Employee not found.")
#                 else:
#                     st.warning("Please enter a valid Employee ID.")

#         elif search_type == "Salary ≥":
#             salary_input = st.number_input("Enter Minimum Salary", min_value=0)
#             if st.button("Get Employees by Salary"):
#                 filtered = df[df["salary"] >= salary_input]
#                 if not filtered.empty:
#                     st.dataframe(filtered)
#                 else:
#                     st.warning("No employees found with that salary or more.")

#         elif search_type == "Experience ≥":
#             exp_input = st.number_input("Enter Minimum Experience (in years)", min_value=0)
#             if st.button("Get Employees by Experience"):
#                 filtered = df[df["experience"] >= exp_input]
#                 if not filtered.empty:
#                     st.dataframe(filtered)
#                 else:
#                     st.warning("No employees found with that experience or more.")
#     except FileNotFoundError:
#         st.error("employees.csv not found. Please upload it to use this feature.")
#     except Exception as e:
#         st.error(f"Error reading employee data: {e}")

# st.markdown('</div>', unsafe_allow_html=True)

from fastapi import FastAPI, Request, Form, Cookie
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uuid
import pandas as pd
from llama_api import ask_ollama
from load_docs import get_vectorstore
from course_matcher import match_courses



# -------------------------------------------------
# INIT
# -------------------------------------------------
app = FastAPI(
    title="IFHE Conversational Chatbot",
    description="Context-aware chatbot with conversation memory",
    version="3.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Retriever (for contextual search)
retriever = get_vectorstore().as_retriever()

# Global memory dictionary {session_id: [{"role": "user"/"bot", "content": "..."}]}
conversation_memory = {}

# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def normalize_query(query: str) -> str:
    q = query.strip().lower()
    if "admission" in q:
        return "What is the admission process and important deadlines?"
    elif "fee" in q or "fees" in q:
        return "What is the fee structure?"
    elif "calendar" in q or "schedule" in q:
        return "Show the academic calendar and schedule"
    elif "hostel" in q or "transport" in q:
        return "What are the hostel and transport facilities?"
    elif "faculty" in q or "teacher" in q:
        return "Who are the faculty members at IFHE?"
    elif "placement" in q or "recruiters" in q:
        return "Tell me about placements and top recruiters at IFHE."
    elif "scholarship" in q:
        return "What scholarships are available at IFHE?"
    return q


def build_prompt(history, user_message, context):
    """
    Build a conversation-aware prompt for LLM.
    Includes past turns and relevant retrieved documents.
    """
    history_text = ""
    for turn in history[-5:]:  # last 5 turns
        role = "User" if turn["role"] == "user" else "Assistant"
        history_text += f"{role}: {turn['content']}\n"

    return f"""
You are an academic assistant for IFHE University.
Answer clearly, professionally, and concisely.

Context from documents:
{context}

Conversation so far:
{history_text}

Current user question:
User: {user_message}

Answer:
"""


# -------------------------------------------------
# ROUTES
# -------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request, session_id: str | None = Cookie(default=None)):
    """
    Serve the chatbot UI and assign a unique session ID if missing.
    """
    if not session_id:
        session_id = str(uuid.uuid4())
        response = templates.TemplateResponse("index.html", {"request": request})
        response.set_cookie(key="session_id", value=session_id, httponly=True)
        return response

    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat")
async def chat(request: Request, user_message: str = Form(...)):
    """
    Returns a complete chatbot response (non-streaming).
    """
    try:
        # Normalize and retrieve context
        query = normalize_query(user_message)
        docs = retriever.get_relevant_documents(query)
        context = "\n\n".join([d.page_content for d in docs[:10]])

        # Build the full academic assistant prompt
        prompt = f"""
        You are an academic assistant for IFHE University. Use the context below to answer the question clearly and helpfully.
        The context includes various documents and FAQs related to IFHE University’s programs, admissions, and academic details.

        Instructions:
        - If the question is about **courses**, list all courses offered by IFHE University (B.Tech, BBA, B.Sc, M.Tech, M.Sc, etc.) with their **specializations**.
        - If the question is about **admissions** (including Postgraduate), provide:
          * Admission process
          * Important dates
          * Eligibility criteria
          * Required documents
          * URLs for more information:
            - https://ifheindia.org/
            - https://ifheindia.org/online-registration/
        - If the query is about **fees, scholarships, placements, campus facilities, faculty, or programs**, provide accurate and concise information based on the context.
        - If faculty details are asked, include:
          * URL: https://ifheindia.org/faculty/
          * Mention that details of faculty members are available on the official website.
        - Format the answer in structured sections with headings and bullet points.
        - Avoid emojis. Respond in a formal, academic tone.

        Context:
        {context}

        Question:
        {user_message}

        Answer:
        """

        # Get the complete model response
        response = ask_ollama(prompt)
        return JSONResponse({"answer": response})

    except Exception as e:
        print("⚠️ Chat Error:", e)
        return JSONResponse({"answer": f"⚠️ Error: {str(e)}"})

@app.post("/reset", response_class=JSONResponse)
async def reset_conversation(session_id: str = Form(...)):
    """
    Clears conversation history for a session.
    """
    if session_id in conversation_memory:
        conversation_memory[session_id] = []
    return JSONResponse({"status": "cleared"})

EMPLOYEE_CSV_PATH = "employees1.csv"

try:
    employees_df = pd.read_csv(EMPLOYEE_CSV_PATH)
    print(f"✅ Loaded {len(employees_df)} employee records from {EMPLOYEE_CSV_PATH}")
except Exception as e:
    print("⚠️ Error loading employee CSV:", e)
    employees_df = pd.DataFrame(columns=["id", "name", "role", "salary", "experience", "department"])


@app.post("/employees/search")
async def search_employees(
    request: Request,
    search_type: str = Form(...),
    value: str = Form(...)
):
    try:
        df = employees_df.copy()

        if search_type == "id":
            result = df[pd.to_numeric(df["name"].astype(str).str.lower() == value.lower())]

        elif search_type == "salary":
            result = df[pd.to_numeric(df["salary"], errors="coerce") >= float(value)]

        elif search_type == "experience":
            result = df[pd.to_numeric(df["experience"], errors="coerce") >= float(value)]

        else:
            result = pd.DataFrame()

        if result.empty:
            return {"results": []}
        else:
            return {"results": result.to_dict(orient="records")}

    except Exception as e:
        print("⚠️ Employee search error:", e)
        return {"results": [], "error": str(e)}
    
@app.post("/recommend_courses")
async def recommend_courses(
    request: Request,
    stream: str = Form(...),
    interest: str = Form(...),
    english: str = Form(...),
    tenth: float = Form(...),
    twelfth: float = Form(...),
):
    """
    Recommend courses based on student's profile using the same logic from app1.py.
    """
    try:
        if not (stream and interest and english):
            return {"error": "Please fill all required fields."}

        if tenth < 60 or twelfth < 60:
            return {
                "eligible": False,
                "message": "You are not eligible. Minimum 60% required in both 10th and 12th."
            }

        profile = {
            "stream": stream,
            "interest": interest,
            "english": english,
            "10th": tenth,
            "12th": twelfth
        }

        recs = match_courses(profile)

        if recs:
            return {
                "eligible": True,
                "recommendations": recs,
                "apply_link": "https://ifheindia.org/online-registration"
            }
        else:
            return {"eligible": True, "recommendations": []}

    except Exception as e:
        print("⚠️ Course recommendation error:", e)
        return {"error": str(e)}


# ------------------- PAGE ROUTES -------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/chat", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@app.get("/courses", response_class=HTMLResponse)
async def courses_page(request: Request):
    return templates.TemplateResponse("courses.html", {"request": request})

@app.get("/employees", response_class=HTMLResponse)
async def employees_page(request: Request):
    return templates.TemplateResponse("employees.html", {"request": request})

