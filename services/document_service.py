import os

from parsers.pdf_parser import extract_pdf_text
from parsers.docx_parser import extract_docx_text
from parsers.txt_parser import extract_txt_text


def load_document(filepath):

    extension = filepath.split(
        "."
    )[-1].lower()

    if extension == "pdf":

        with open(
            filepath,
            "rb"
        ) as f:

            return extract_pdf_text(f)

    elif extension == "docx":

        with open(
            filepath,
            "rb"
        ) as f:

            return extract_docx_text(f)

    elif extension == "txt":

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as f:

            return f.read()

    return ""