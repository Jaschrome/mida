from docx import Document


def extract_docx_text(uploaded_file):

    doc = Document(uploaded_file)

    text = ""

    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"

    return text