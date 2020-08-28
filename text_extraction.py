import os,sys
import re,csv
import pandas as pd
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO,StringIO


#To write into text file from an object.
def writelines(self, lines):
    self._checkClosed()
    for line in lines:
       self.write(line)

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

#Init the files to store output
def initiate_output_files(fname,t_address,c_address):
    with open(t_address, "w", encoding="utf-8") as text_file, open(c_address,"w",newline='') as csv_file:
        text_file.truncate(0)
        csv_file.truncate(0)
        writer = csv.writer(csv_file,delimiter=' ', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Linkedin_Profile_Text"])   

#Extract text from PDF file
def generate_output(directory,fname,t_address,c_address):
    for i in range(len(fname)): #Repeat each operation for each document.
        text_from_pdf = pdf_to_text(os.path.join(directory,fname[i])) #Extract text with PDF_to_text Function call
        decoded_text = text_from_pdf.decode("utf-8")     #Decode result from bytes to text

        s = decoded_text
        s = s.lower().strip()
        lines = s.split("\n")
        non_empty_lines = [line for line in lines if line.strip() != ""]

        s = ""
        for line in non_empty_lines:
            s += line + " "
        #s = s[:-2]
        with open(t_address, "a", encoding="utf-8",newline='\n') as text_file:
            text_file.truncate(0)
            text_file.writelines(s)

        with open(t_address, "r",newline='\n') as text_file, open(c_address,"a",newline='') as csv_file:
            writer = csv.writer(csv_file,delimiter=' ', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(text_file)

if __name__ == "__main__":

    directory = r"C:\Users\sunee\OneDrive\Desktop\Workspace\Code_Vector Screening\codevector_screening\Linkedin_Profiles"
    fname = os.listdir(directory) 
    fname.sort(key=lambda f: int(re.sub('\D', '', f)))
 
    (text_file,csv_file) = ("output.txt","output1.csv")

    initiate_output_files(fname,text_file,csv_file)

    generate_output(directory,fname,text_file,csv_file)


 


    



         




