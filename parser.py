import PyPDF2

def extract_text(file):
    text = ""
    if file.name.endswith(".pdf"):
        pdf = PyPDF2.PdfReader(file)
        for page in pdf.pages:
            text += page.extract_text()
    else:
        text = file.read().decode("utf-8")
    return text