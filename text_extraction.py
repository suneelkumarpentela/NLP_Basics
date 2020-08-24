import os
import sys
import re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO


#PDF to text Function. 
def pdf_to_text(path):
    manager = PDFResourceManager()
    retstr = BytesIO()
    layout = LAParams(all_texts=True)
    device = TextConverter(manager, retstr, laparams=layout)
    filepath = open(path, 'rb')
    interpreter = PDFPageInterpreter(manager, device)

    for page in PDFPage.get_pages(filepath, check_extractable=True):
        interpreter.process_page(page)
    
    text = retstr.getvalue()
    filepath.close()
    device.close()
    retstr.close()
    return text


if __name__ == "__main__":

    directory = r"C:\Users\sunee\OneDrive\Desktop\Workspace\Code_Vector Screening\codevector_screening\Linkedin_Profiles"
    fname = os.listdir(directory) 

    text_from_pdf = pdf_to_text(os.path.join(directory,fname[0])) #Extract text with PDF_to_text Function call
    decoded_text = text_from_pdf.decode("utf-8")     #Decode result fromf bytes to text
    print(decoded_text)
