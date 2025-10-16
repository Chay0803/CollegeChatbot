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


import streamlit as st
import pandas as pd
from llama_api import ask_ollama
from course_matcher import match_courses
from load_docs import get_vectorstore

st.set_page_config(page_title="IFHE Chatbot", layout="wide")

st.markdown(
    """
    <div style="background-color:#003366; padding: 18px 0; border-radius: 10px; text-align: center; margin-bottom: 30px;">
        <span style="color: white; font-size: 2.2rem; font-weight: bold; letter-spacing: 1px;">
            IFHE Assitance 
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <style>
    body { background-color: #f4f8fb; }
    .stTabs [data-baseweb="tab-list"] { background: #e6eef7; border-radius: 8px; border: 1px solid #003366; padding: 4px; }
    .stTabs [data-baseweb="tab"] { color: #003366; font-weight: 600; }
    .stTabs [aria-selected="true"] { background: #003366 !important; color: #fff !important; border-radius: 6px 6px 0 0; }
    h1, .stMarkdown h1 { color: #003366; }
    .stButton>button { background-color: #003366; color: #fff; border-radius: 6px; border: none; font-weight: 600; }
    .stButton>button:hover { background-color: #00509e; color: #fff; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main">', unsafe_allow_html=True)

# Load Chroma vectorstore and convert to retriever
retriever = get_vectorstore().as_retriever()

def normalize_query(q):
    q = q.strip().lower()
    if "admission" in q:
        return "What is the admission process and important deadlines?"
    elif "fee" in q:
        return "What is the fee structure?"
    elif "calendar" in q:
        return "Show the academic calendar and schedule"
    elif "hostel" in q:
        return "What are the hostel and transport facilities?"
    elif "founder" in q:
        return "Who is the founder of IFHE?"
    return q

tab1, tab2, tab3 = st.tabs(["Ask the Chatbot", "Course Recommender", "Employee Details"])

# Tab 1: Chatbot
with tab1:
    question = st.text_input("Enter your question:")
    if st.button("Ask"):
        if question:
            with st.spinner("Reading documents and generating response..."):
                query = normalize_query(question)
                docs = retriever.get_relevant_documents(query)
                context = "\n\n".join([d.page_content for d in docs[:10]])  
                prompt = f"""You are an academic assistant for IFHE University. Use the context below to answer the question clearly and helpfully.
                List all the courses offered by IFHE University(B.Tech, BBA, BSc, M.Tech, MSc etc) with their specializations.
                If the question is about admissions(including Post Gradute) provide details about the process, important dates, eligibility criteria, and required documents.
                Provide Urls for more information where relevant. Such as https://ifheindia.org/ or https://ifheindia.org/online-registration/ for admissions.
                if the query is about fees, scholarships, placements, campus facilities, faculty, or programs, provide accurate and concise information based on the context.
                Provide Urls for more information where relevant. Such as https://ifheindia.org/ or https://ifheindia.org/online-registration/ for admissions.
                If information about faculty is asked provide the url https://ifheindia.org/faculty/ for more details. Also mention that Details of faculty members are available on the official website.
                Do not give emojis in the answer.

Context:
{context}

Question: {question}

Answer:"""
                answer = ask_ollama(prompt)
                st.markdown("### Answer:")
                st.success(answer)
        else:
            st.warning("Please enter a question.")

# Tab 2: Course Recommender
with tab2:
    st.subheader("Course Recommendations")
    stream = st.selectbox("Select Your Stream", ["", "Science", "Commerce", "Arts"])
    interest = st.selectbox("Select Your Area of Interest", ["", "Tech", "Law", "Management"])
    english = st.selectbox("Are you comfortable in English?", ["", "Yes", "No"])
    tenth = st.number_input("Enter your 10th percentage", min_value=0.0, max_value=100.0, step=0.1)
    twelfth = st.number_input("Enter your 12th percentage", min_value=0.0, max_value=100.0, step=0.1)

    if st.button("Recommend Courses"):
        if stream and interest and english:
            if tenth < 60 or twelfth < 60:
                st.error("You are not eligible. Minimum 60% required in both 10th and 12th.")
            else:
                profile = {
                    "stream": stream,
                    "interest": interest,
                    "english": english,
                    "10th": tenth,
                    "12th": twelfth
                }
                recs = match_courses(profile)
                if recs:
                    for course in recs:
                        st.success(f"{course}")
                    st.markdown(
                        """
                        <a href="https://ifheindia.org/online-registration" target="_blank">
                            <button style="background-color:#003366;color:white;padding:10px 24px;border:none;border-radius:6px;font-size:16px;">
                                Apply Now
                            </button>
                        </a>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.info("No matching courses found.")

# Tab 3: Employee Lookup
with tab3:
    st.subheader("Employee Details Lookup")
    try:
        df = pd.read_csv("employees1.csv")
        search_type = st.radio("Search by:", ["Employee ID", "Salary ≥", "Experience ≥"])

        if search_type == "Employee ID":
            empid_input = st.text_input("Enter Employee ID")
            if st.button("Get Employee by ID"):
                if empid_input.strip():
                    match = df[df["empid"].astype(str) == empid_input.strip()]
                    if not match.empty:
                        st.dataframe(match)
                    else:
                        st.error("Employee not found.")
                else:
                    st.warning("Please enter a valid Employee ID.")

        elif search_type == "Salary ≥":
            salary_input = st.number_input("Enter Minimum Salary", min_value=0)
            if st.button("Get Employees by Salary"):
                filtered = df[df["salary"] >= salary_input]
                if not filtered.empty:
                    st.dataframe(filtered)
                else:
                    st.warning("No employees found with that salary or more.")

        elif search_type == "Experience ≥":
            exp_input = st.number_input("Enter Minimum Experience (in years)", min_value=0)
            if st.button("Get Employees by Experience"):
                filtered = df[df["experience"] >= exp_input]
                if not filtered.empty:
                    st.dataframe(filtered)
                else:
                    st.warning("No employees found with that experience or more.")
    except FileNotFoundError:
        st.error("employees.csv not found. Please upload it to use this feature.")
    except Exception as e:
        st.error(f"Error reading employee data: {e}")

st.markdown('</div>', unsafe_allow_html=True)
import os
import streamlit as st

st.write("🔑 API key exists:", bool(os.getenv("OPENROUTER_API_KEY")))
