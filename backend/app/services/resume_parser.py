import io
import docx2txt
import pdfplumber


def extract_text_from_pdf(file_bytes):
    text = ""

    pdf_file = io.BytesIO(file_bytes)

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text


def extract_text_from_docx(file_bytes):
    file_stream = io.BytesIO(file_bytes)
    return docx2txt.process(file_stream)


def parse_resume(file_bytes, file_type):

    if file_type == "application/pdf":
        return extract_text_from_pdf(file_bytes)

    elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(file_bytes)

    return "Unsupported file type"
