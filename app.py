import streamlit as st

st.set_page_config(
    page_title="MIDA",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "current_document" not in st.session_state:
    st.session_state["current_document"] = ""

if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.title("MIDA")

st.caption(
    "Multi-document Intelligence & Discovery Assistant"
)

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Platform",
        "Online"
    )

with col2:
    st.metric(
        "Model",
        "Llama 3.3 70B"
    )

with col3:
    st.metric(
        "Provider",
        "Groq"
    )

st.markdown("""
### Overview

MIDA is an AI-powered document intelligence platform designed for:

- Document Summarization
- Multi-format File Analysis
- Website Content Analysis
- Conversational Question Answering
- Research Assistance

### Features

- Upload PDF, DOCX, and TXT files
- Analyze website content
- Generate AI-powered summaries
- Ask questions about uploaded documents
- General-purpose AI chat
- Persistent document storage

Use the navigation menu on the left to begin.
""")

st.markdown("---")

st.subheader("Current Status")

if st.session_state["current_document"]:

    st.success(
        "Document Loaded"
    )

    st.write(
        f"Loaded document size: "
        f"{len(st.session_state['current_document']):,} characters"
    )

else:

    st.info(
        "No document currently loaded"
    )