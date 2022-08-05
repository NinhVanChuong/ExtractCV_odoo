import torch
import numpy as np
import cv2
from time import time
from pdfminer.high_level import extract_text
import os
from pytesseract import Output
import pytesseract
import re

class MugDetection:
    """
    Class implements Yolo5 model to make inferences on a youtube video using Opencv2.
    """

    def __init__(self, model_name='best.pt'):
        """
        Initializes the class with youtube url and output file.
        :param url: Has to be as youtube URL,on which prediction is made.
        :param out_file: A valid output file name.
        """
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
        self.infor={}
        for i in range(n):
            row = cord[i]
            if row[4] >= 0.5:
                x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                bgr = (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                cv2.putText(frame, self.class_to_label(labels[i]), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 2, bgr, 2)
                image_crop = frame[y1:y2, x1:x2]
                cv2.imwrite('a.png', image_crop)
                image=cv2.imread('a.png')
                os.remove('a.png')
                if self.class_to_label(labels[i]) != 'face':
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    binary = cv2.threshold(gray, 127, 255,
                            cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
                    text = pytesseract.image_to_string(binary,lang='vie')
                    text = re.sub(r"[&#%]","",text)
                    text = text.strip(' \n')
                    text = text.replace('\n','')
                    self.infor[self.class_to_label(labels[i])] = text
        print(self.infor)
        return frame
    def __call__(self):
        """
        This function is called when class is executed, it runs the loop to read the video frame by frame,
        and write the output into a new file.
        :return: void
        """
        frame = cv2.imread('CV4.jpg')
        results = self.score_frame(frame)
        frame = self.plot_boxes(results, frame)
        cv2.imshow('YOLOv5 Detection', frame)
        cv2.waitKey(0)
        return self.infor
# Create a new object and execute.
detector = MugDetection(model_name='best.pt')
detector()