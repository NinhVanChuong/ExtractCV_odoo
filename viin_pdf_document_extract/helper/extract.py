import pytesseract
import os
import cv2
from PIL import Image
from pdf2image import convert_from_path
from pytesseract import Output
import re
from stdnum.cz import dic

class ExtractPDF():
    
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        
    def extract_text(self):
        self.text=[]
        images = convert_from_path(self.pdf_path,dpi=500)
        for i in range(len(images)):
            images[i].save('page'+ str(i) +'.jpg','JPEG')
            image = cv2.imread('page'+ str(i) +'.jpg')
            # image = cv2.imread('demo.png')
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            binary = cv2.threshold(gray, 127, 255,
                                cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            self.text = pytesseract.image_to_string(binary,lang='vie')
            os.remove('page'+ str(i) +'.jpg')
            return self.text
    def extract_dic(self):
        self.dic={}
        print(self.text)
        email_pattern = '([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
        if(re.search(email_pattern,self.text)):
            self.dic['email']=re.search(email_pattern,self.text)[0]
        phone_pattern='(?:\+\d{2})?\d{3,4}\D?\d{3}\D?\d{3}'
        if(re.search(phone_pattern,self.text)):
            self.dic['phone']=re.search(phone_pattern,self.text)[0]
        dob_pattern = '[\d]{1,2}/[\d]{1,2}/[\d]{4}'
        if(re.search(dob_pattern,self.text)):
            self.dic['dob']=re.search(dob_pattern,self.text)[0]
        print(self.dic)
            # #thu nghiem từng text ở từng vị trí
            # d = pytesseract.image_to_data(binary,lang='vie',output_type=Output.DICT)
            #
            # n_boxes = len(d['text'])
            # email_pattern = '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
            # re.match(email_pattern, d['text']
            #
            # for i in range(n_boxes):
            #     if float(d['conf'][i]) > 60.0:
            #         if re.match(email_pattern, d['text'][i]):
            #             (x, y, w, h) = d["left"][i], d["top"][i], d["width"][i], d["height"][i] 
            #             image = cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2) #Plotting bounding box
            #             print(f"Email: {d['text'][i]}")
            #             print(d['text'][i])
            # cv2.imshow('',image)
            # cv2.waitKey(0)
a=ExtractPDF('CV7.pdf')
a.extract_text()
a.extract_dic()