import requests
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import os


def get_sentence_info(df):
    
    judge_id = []
    headquarters = []
    
    for index, row in df.iterrows():
        #if(index < 10):

        # Get url and sentence id
        url = row['URL']
        sentence_id = row['ID']

        # Download the pdf from the url
        save_path = dowload_pdf_from_url(url, sentence_id)

        # Extract text
        text = convert_pdf_to_txt(save_path)

        # Convert text to dict
        dict1 = convert_text_to_dict(text)

        # Get info
        judge_id.append(dict1["Ponente"])
        headquarters.append(dict1["Sede"])

        # Delete the file
        os.remove(save_path)
            
    return judge_id, headquarters

def dowload_pdf_from_url(url, sentence_id):
    
    response = requests.get(url)
    save_path = "..\output\\" + str(sentence_id) + ".pdf"
    
    with open(save_path, 'wb') as f: #open the file in binary format for writing
        f.write(response.content)
        
    return save_path

def convert_pdf_to_txt(path):
    
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    
    return text

def convert_text_to_dict(text):
    
    # Create a dict where the desired information will be stored
    sentence_info = {}

    while True:
        # Read one line
        line, text = text.split("\n", 1) 
        
        # Split the line between key and description if possible (first part of the sentence)
        try:
            key, description = line.strip().split(":", 1)
        except:
            continue
        
        #Add the information to the dictionary
        sentence_info[key] = description.strip()
        
        #Stop reading when we reach the desired part of the document
        if(key.strip() == "Tipo de Resolución"):
            break
    
    return sentence_info


