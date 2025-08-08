!pip install pytesseract
!pip install pdf2image
!pip install PIL
!sudo apt-get update
!sudo apt-get install poppler-utils
!sudo apt install tesseract-ocr-ita
!export TESSDATA_PREFIX="/usr/share/tesseract-ocr/4.00/tessdata/"



from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import os

pdf_path = '/content/bolletta-luce-fac-simile.pdf'
out_path = '/content/output/bolletta-luce-fac-simile.txt'
with open(os.path.join(out_path), 'w') as f:
  try:
      text = ""
      images = convert_from_path(pdf_path)

      for img in images:
          f.write("##########NEW PAGE###########")
          text = pytesseract.image_to_string(img, lang='ita')
          f.write(text)
      
  except Exception as e:
      print(f"An error occurred: {e}")