import torch
import numpy as np
import cv2
from time import time
from pdfminer.high_level import extract_text
import os
import pytesseract
import re
from odoo.modules.module import get_module_resource

class MugDetection:
    """
    Class implements Yolo5 model to make inferences on a youtube video using Opencv2.
    """

    def __init__(self, model_name=None):
        """
        Initializes the class with youtube url and output file.
        :param url: Has to be as youtube URL,on which prediction is made.
        :param out_file: A valid output file name.
        """
        if not model_name:
            model_name = get_module_resource('viin_extract_cv','wizard/tool','best.pt')# odoo đọc file từ máy chủ
        self.model = self.load_model(model_name)
        self.classes = self.model.names
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("Using Device: ", self.device)

    def load_model(self, model_name):
        """
        Loads Yolo5 model from pytorch hub.
        :return: Trained Pytorch model.
        """
        if model_name:
            model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_name, force_reload=True)
        else:
            model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        return model

    def score_frame(self, frame):
        """
        Takes a single frame as input, and scores the frame using yolo5 model.
        :param frame: input frame in numpy/list/tuple format.
        :return: Labels and Coordinates of objects detected by model in the frame.
        """
        self.model.to(self.device)
        frame = [frame]
        results = self.model(frame)
        labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        return labels, cord

    def class_to_label(self, x):
        """
        For a given label value, return corresponding string label.
        :param x: numeric label
        :return: corresponding string label
        """
        return self.classes[int(x)]

    def plot_boxes(self, results, frame):
        """
        Takes a frame and its results as input, and plots the bounding boxes and label on to the frame.
        :param results: contains labels and coordinates predicted by model on the given frame.
        :param frame: Frame which has been scored.
        :return: Frame with bounding boxes and labels ploted on it.
        """
        labels, cord = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        self.infor = {}
        self.face = None
        for i in range(n):
            row = cord[i]
            if row[4] >= 0.5:
                x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                bgr = (0, 255, 0)
                image_crop = self.image[y1:y2, x1:x2]
                img = image_crop
                binary = img
                # cv2.imwrite('/Users/vanchuong/Desktop/LreanPython/{}.png'.format(str(i)), image_crop)
                # img=cv2.imread('/Users/vanchuong/Desktop/LreanPython/{}.png'.format(str(i)))
                # os.remove('a.png')
                if self.class_to_label(labels[i]) != 'face':
                    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    # binary = cv2.threshold(gray, 127, 255,
                    #         cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
                    pytesseract.pytesseract.tesseract_cmd = r"/opt/homebrew/Cellar/tesseract/5.2.0/bin/tesseract"
                    text = pytesseract.image_to_string(binary, lang = 'vie')# sua duong dan cmd tesseract
                    text = text.strip(' \n')
                    if self.class_to_label(labels[i]) != 'name':
                        text = text.split(' ')[-1]
                        text = re.sub(r"[^a-zA-Z0-9@/]","",text)
                        text = text.replace('Email','')
                        text = text.replace('Gender','')
                    if self.class_to_label(labels[i]) == 'name':
                        text = text.replace('ĐÔ','ĐỖ')
                        text = text.replace('NGUYÊN','NGUYỄN')
                    elif self.class_to_label(labels[i]) == 'phone':
                        text = text.replace('/','7')
                        text = text.replace('Phone','')
                    elif self.class_to_label(labels[i]) == 'dob':
                        text = text.replace('Date of birth','')
                        text = text.replace('birth','')
                    text = text.strip(' \n')
                    self.infor[self.class_to_label(labels[i])] = text
                    # cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                    # cv2.putText(frame, self.class_to_label(labels[i]), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 2, bgr, 2)
                else:
                    self.face=img
        return frame
    def convert_to_record(self, path):
        """
        This function is called when class is executed, it runs the loop to read the video frame by frame,
        and write the output into a new file.
        :return: void
        """
        self.image = cv2.imread(path)
        
        frame = self.image.copy()
        results = self.score_frame(frame)
        frame = self.plot_boxes(results, frame)
        return self.infor,self.face