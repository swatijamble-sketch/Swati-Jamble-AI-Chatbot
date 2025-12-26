from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq

# ---------------------------------------------------
# Load environment variables (GROQ_API_KEY)
# ---------------------------------------------------
load_dotenv()

# ---------------------------------------------------
# Streamlit Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Swati Jamble-AI Academic Assistant",
    page_icon="🎓",
    layout="centered",
)

# ---------------------------------------------------
# App Title & Disclaimer
# ---------------------------------------------------
st.title("🎓 Swati Jamble – AI Academic Assistant")

st.info(
    "This AI assistant is for academic support only. "
    "It is intended to help students understand concepts, "
    "prepare for exams, and support learning. "
    "It should not be used as a replacement for classroom teaching, "
    "assignments, or examinations."
)

st.caption("Supported Domains: BSc(CS),BSc(AI & ML),BSc(Data Science),BCom(CA),BCom(BM),MSc(CS),MSc(Data Science)")

# ---------------------------------------------------
# Mode Selection (Student / Faculty)
# ---------------------------------------------------
mode = st.selectbox(
    "Select Usage Mode",
    ["Student Mode", "Faculty Mode"]
)

# ---------------------------------------------------
# Clear Chat Button
# ---------------------------------------------------
if st.button("🔄 Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()

# ---------------------------------------------------
# Example Academic Questions
# ---------------------------------------------------
with st.expander("📘 Example Academic Questions"):
    st.markdown("""
    - Explain Python lists and tuples with examples  
    - What is SQL JOIN? Explain all types  
    - What is Power BI and where is it used?  
    - Difference between supervised and unsupervised learning  
    - What is ETL in Data Analytics?  
    - Write a Python program to find factorial of a number  
    """)

# ---------------------------------------------------
# Initialize Chat History
# ---------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------------------------------------------
# Display Chat History
# ---------------------------------------------------
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------------------------
# Initialize LLM
# ---------------------------------------------------
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.2,
)

# ---------------------------------------------------
# User Input
# ---------------------------------------------------
user_prompt = st.chat_input("Ask your academic question here...")

if user_prompt:
    # Display and store user message
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append(
        {"role": "user", "content": user_prompt}
    )

    # ---------------------------------------------------
    # Dynamic System Prompt Based on Mode
    # ---------------------------------------------------
    if mode == "Faculty Mode":
        role_instruction = (
            "Provide detailed explanations, structured teaching notes, "
            "examples, and points that can help in classroom instruction."
        )
    else:
        role_instruction = (
            "Explain concepts in simple, student-friendly language "
            "with short examples and exam-oriented points."
        )

    system_prompt = {
        "role": "system",
        "content": (
            "You are an AI Academic Assistant for ATSS College. "
            "Your role is to assist students and faculty with academic concepts "
            "related to Python, SQL, Power BI, Data Analytics, and Artificial Intelligence. "
            "Avoid non-academic, inappropriate, or irrelevant responses. "
            "Keep answers concise (5–10 bullet points or short paragraphs). "
            f"{role_instruction}"
        ),
    }

    # ---------------------------------------------------
    # Invoke LLM
    # ---------------------------------------------------
    response = llm.invoke(
        input=[system_prompt] + st.session_state.chat_history
    )

    assistant_response = response.content

    # Store assistant response
    st.session_state.chat_history.append(
        {"role": "assistant", "content": assistant_response}
    )

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

# ---------------------------------------------------
# Footer
# ---------------------------------------------------
st.markdown("---")
st.caption(
    "© ATSS College | AI Academic Assistant | "
    "For internal academic use only"
)