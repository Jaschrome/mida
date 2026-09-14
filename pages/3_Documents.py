import streamlit as st

from services.llm_service import call_llm

st.title("AI Chat")

# ==========================
# Session State
# ==========================

if "current_document" not in st.session_state:
    st.session_state["current_document"] = ""

if "messages" not in st.session_state:
    st.session_state["messages"] = []

document_text = st.session_state["current_document"]

# ==========================
# Status
# ==========================

if document_text:

    st.success(
        "Document Context Active"
    )

else:

    st.info(
        "General AI Chat Mode"
    )

# ==========================
# Chat History
# ==========================

for message in st.session_state["messages"]:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

# ==========================
# Chat Input
# ==========================

question = st.chat_input(
    "Ask a question..."
)

if question:

    st.session_state["messages"].append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    # ==========================
    # Prompt Creation
    # ==========================

    if document_text:

        prompt = f"""
You are MIDA, an AI research assistant.

DOCUMENT:

{document_text[:100000]}

USER QUESTION:

{question}

Instructions:

- Use document information whenever relevant.
- If the question is unrelated to the document, answer normally.
- If both are useful, combine them.
- Be concise and accurate.
"""

    else:

        prompt = f"""
You are MIDA, an AI research assistant.

QUESTION:

{question}

Provide a helpful answer.
"""

    # ==========================
    # Generate Response
    # ==========================

    with st.spinner(
        "Generating response..."
    ):

        answer = call_llm(
            prompt
        )

    with st.chat_message(
        "assistant"
    ):

        st.markdown(
            answer
        )

    st.session_state["messages"].append(
        {
            "role": "assistant",
            "content": answer
        }
    )

# ==========================
# Sidebar
# ==========================

with st.sidebar:

    st.title("MIDA")

    st.caption(
        "Multi-document Intelligence & Discovery Assistant"
    )

    st.markdown("---")

    if document_text:

        st.caption(
            "Document Loaded"
        )

        st.write(
            f"{len(document_text):,} characters"
        )

    else:

        st.caption(
            "No Document Loaded"
        )

    st.markdown("---")

    if st.button(
        "Clear Chat"
    ):

        st.session_state["messages"] = []

        st.rerun()