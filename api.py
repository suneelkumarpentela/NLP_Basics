import os,sys,re,csv,json
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import pandas as pd
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO
from io import StringIO

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloads/'
ALLOWED_EXTENSIONS = {'pdf', 'txt'}

app = Flask(__name__, static_url_path="/static")
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
# limit upload size upto 8mb
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            process_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename)
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('index.html')


def process_file(path, filename):
    text_extract(path, filename)


def text_extract(path, filename):
    #input_file = PdfFileReader(open(path, 'rb'))
    #output = PdfFileWriter()
    text_from_pdf = pdf_to_text(path) #Extract text with PDF_to_text Function call
    decoded_text = text_from_pdf.decode("utf-8")     #Decode result fromf bytes to text
    s = decoded_text
    s = s.lower().strip()
    lines = s.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != ""]

    s = ""
    for line in non_empty_lines:
        s += line + " "
    s = s[:-2]
    with open(filename + ".txt", "a", encoding="utf-8",newline='\n') as text_file:
        text_file.truncate(0)

        for line in s:
            text_file.write(line) 
        text_file.save(os.path.join(app.config['DOWNLOAD_FOLDER'] + filename + ".txt"))
        
    #output_stream = open(app.config['DOWNLOAD_FOLDER'] + filename + ".txt", 'w')
    
    #text_file.write(output_stream)

    # with open("output.txt", "r",newline='\n') as text_file, open(app.config['DOWNLOAD_FOLDER'] + "output.json","w") as output_file:
    #         json.dump(text_file,output_file)

    # output_stream = open(app.config['DOWNLOAD_FOLDER'] + filename, 'wb')
    # output.write(output_stream)

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


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename + ".txt", as_attachment=True)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)