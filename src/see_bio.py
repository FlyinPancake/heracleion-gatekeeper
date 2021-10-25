import cv2
import pytesseract
from pytesseract import Output
import numpy as np
import simplejson
from datetime import datetime

SC_IMG = "test/sc.png"

def filter_image(img_file):
    org = cv2.imread(img_file)
    image = org
    image = cv2.resize(image, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.bitwise_not(image)
    
    #image = cv2.threshold(image,150,255,cv2.THRESH_TRUNC)[1]
    
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.convertScaleAbs(image, alpha=2.3, beta=0)
    return image


def process_bio_image(img_src):
    img = filter_image(img_src)
    
    cv2.imshow("1", img)
    cv2.waitKey(0)