import os
import pdfplumber


files = [f for f in os.listdir() if os.path.isfile(f) and f.lower().endswith('.pdf')]
if not files:
    print("No PDF files found in the current directory.")
    exit()

file = os.path.join(os.getcwd(), files[0])

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += "\n\n############NEW PAGE##############\n"
                text += page_text
            else:
                text += "\n[No text found on this page]\n"
    return text

with open(os.path.join(os.getcwd(),"out.txt"), 'w') as out_file:
    pdf_text = extract_text_from_pdf(file)
    out_file.write(pdf_text)