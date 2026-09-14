import streamlit as st
import os

from parsers.pdf_parser import extract_pdf_text
from parsers.docx_parser import extract_docx_text
from parsers.txt_parser import extract_txt_text
from parsers.web_parser import extract_web_text

from services.summary_service import summarize_document
from services.document_service import load_document
from services.rag_service import index_document

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

st.title("Document Analysis")

if "current_document" not in st.session_state:
    st.session_state["current_document"] = ""

if "messages" not in st.session_state:
    st.session_state["messages"] = []

text = ""

# ==========================
# Load document selected from
# Documents page
# ==========================

if "selected_file" in st.session_state:

    try:

        filepath = os.path.join(
            UPLOAD_DIR,
            st.session_state["selected_file"]
        )

        text = load_document(
            filepath
        )

        st.session_state["current_document"] = text

        st.success(
            f"Loaded: {st.session_state['selected_file']}"
        )

    except Exception as e:

        st.error(str(e))

# ==========================
# File Upload
# ==========================

uploaded_file = st.file_uploader(
    "Upload Document",
    type=["pdf", "docx", "txt"]
)

if uploaded_file:

    try:

        save_path = os.path.join(
            UPLOAD_DIR,
            uploaded_file.name
        )

        with open(
            save_path,
            "wb"
        ) as f:

            f.write(
                uploaded_file.getbuffer()
            )

        extension = uploaded_file.name.split(
            "."
        )[-1].lower()

        if extension == "pdf":

            text = extract_pdf_text(
                uploaded_file
            )

        elif extension == "docx":

            text = extract_docx_text(
                uploaded_file
            )

        elif extension == "txt":

            text = extract_txt_text(
                uploaded_file
            )

        st.session_state["current_document"] = text
        st.session_state["messages"] = []

        with st.spinner(
            "Indexing document..."
        ):
            index_document(
                text,
                uploaded_file.name
            )

        st.success(
            f"Loaded and indexed {len(text):,} characters"
        )

    except Exception as e:

        st.error(str(e))

# ==========================
# Website Analysis
# ==========================

st.markdown("---")

url = st.text_input(
    "Analyze Website URL"
)

if url:

    try:

        with st.spinner(
            "Fetching website..."
        ):

            text = extract_web_text(
                url
            )

        st.session_state["current_document"] = text
        st.session_state["messages"] = []

        with st.spinner(
            "Indexing website..."
        ):
            index_document(
                text,
                "website"
            )

        st.success(
            f"Loaded and indexed {len(text):,} characters"
        )

    except Exception as e:

        st.error(str(e))

# ==========================
# Preview + Summary
# ==========================

document_text = st.session_state.get(
    "current_document",
    ""
)

if document_text:

    st.subheader(
        "Document Preview"
    )

    st.text_area(
        "Content",
        document_text[:5000],
        height=300
    )

    if st.button(
        "Generate Summary"
    ):

        with st.spinner(
            "Generating summary..."
        ):

            summary = summarize_document(
                document_text
            )

        st.subheader(
            "Summary"
        )

        st.markdown(summary)