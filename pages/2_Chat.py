import streamlit as st

from services.llm_service import call_llm
from services.rag_service import search_document

st.title("AI Chat")

if "current_document" not in st.session_state:
    st.session_state["current_document"] = ""

if "messages" not in st.session_state:
    st.session_state["messages"] = []

document_text = st.session_state["current_document"]

if document_text:

    st.success(
        "Document Context Active"
    )

else:

    st.info(
        "General AI Chat Mode"
    )

for message in st.session_state["messages"]:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

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

    with st.chat_message(
        "user"
    ):

        st.markdown(
            question
        )

    if document_text:

        try:

            relevant_chunks = search_document(
                question
            )

            context = "\n\n".join(
                relevant_chunks
            )

            context = context[:5000]

            with st.sidebar:

                st.caption(
                    f"Chunks: {len(relevant_chunks)}"
                )

                st.caption(
                    f"Context Size: {len(context):,}"
                )

            prompt = f"""
You are MIDA.

DOCUMENT CONTEXT:

{context}

QUESTION:

{question}

Instructions:

- Answer using the document context.
- If the answer is not present,
  say so.
- Be concise.
- Do not invent information.
"""

        except Exception as e:

            prompt = f"""
You are MIDA.

QUESTION:

{question}

Document retrieval failed.

Error:
{str(e)}
"""

    else:

        prompt = f"""
You are MIDA.

QUESTION:

{question}

Provide a helpful answer.
"""

    st.sidebar.write(
    "Prompt Length:",
    len(prompt)
)

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

with st.sidebar:

    st.title(
        "MIDA"
    )

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