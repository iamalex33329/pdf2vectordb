import PyPDF2


def extract_pdf_content(pdf_path):
    content = []
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            content.append(page.extract_text())
    return content
