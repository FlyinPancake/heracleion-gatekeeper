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
    image = cv2.threshold(image,150,255,cv2.THRESH_TRUNC)[1]
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.convertScaleAbs(image, alpha=2.3, beta=0)
    return image

def read_str(img_cv):
    columns = []
    base_skip = 150
    defs = [210, 210, 210, 210, 210]
    skips = [base_skip, base_skip, base_skip, base_skip, base_skip]
    shp = img_cv.shape

    skip_top = 50
    at = 80
    for kk in range(0, len(defs)):
        ii =defs[kk]
        subi = img_cv[skip_top:shp[0], at:(at+ii)]
        #cv2.imshow('ff', subi)
        #cv2.waitKey(0)
        img_rgb = cv2.cvtColor(subi, cv2.COLOR_BGR2RGB)
        txt = pytesseract.image_to_string(img_rgb, config='-c preserve_interword_spaces=1x1 --psm 1 --oem 3')
        txt = [ii.strip() for ii in txt.split('\n')]
        res = []
        for rt in txt:
            if len(rt) != 0:
                res.append(rt)

        columns.append(res)  
        at += ii + skips[kk]

    return columns

def get_names_from_cols(cols):
    flat = []
    for ii in cols:
        for el in ii:
            if len(el) >= 5:
                flat.append(el)

    return flat

def get_names_from_image(img_src):
    img = filter_image(img_src)
    cols = read_str(img)
    names = get_names_from_cols(cols)
    return names