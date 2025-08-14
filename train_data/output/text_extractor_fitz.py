#!pip install pymupdf

import fitz # PyMuPDF
import os

pdf_path = '/content/GUIDA_ALLA_BOLLETTA.pdf'
out_path = '/content/output/GUIDA_ALLA_BOLLETTA.txt'
extracted_text= ""

# Ensure the output directory exists
os.makedirs(os.path.dirname(out_path), exist_ok=True)

with open(out_path, 'w', encoding='utf-8') as f: # Specify encoding for text files
  try:
      with fitz.open(pdf_path) as doc:
          for page in doc:
              extracted_text += "##########NEW PAGE###########\n"
              extracted_text += page.get_text()

      # Write the extracted text to the output file
      f.write(extracted_text)

  except Exception as e:
      print(f"An error occurred: {e}")