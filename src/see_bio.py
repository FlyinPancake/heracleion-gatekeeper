import cv2
import pytesseract
from pytesseract import Output
import numpy as np
import simplejson
from datetime import datetime

BASE_X=1920
BASE_Y=1080

LOGO = 'temp/logo.png'

def ratio(org, base, actual):
    return int((float(org)/base) * actual)

def crop(img, skip, size):
    shp = img.shape
    x = ratio(skip[1], BASE_X, shp[1])
    xdif = ratio(size[1], BASE_X, shp[1])
    y = ratio(skip[0], BASE_Y, shp[0])
    ydif = ratio(size[0], BASE_Y, shp[0])
    a = x
    ato = x + xdif
    b = y
    bto = y + ydif

    cropped = img[a:ato, b:bto]
    return cropped

def read_img(image):
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    txt = pytesseract.image_to_string(img_rgb, config='-c preserve_interword_spaces=1x1 --psm 1 --oem 3')
    txt = [ii.strip() for ii in txt.split('\n')]
    return  txt[0] or ''

def filter_image(image):
    image = cv2.resize(image, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.bitwise_not(image)
    
    #image = cv2.threshold(image,150,255,cv2.THRESH_TRUNC)[1]
    
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.convertScaleAbs(image, alpha=1.2, beta=0)
    return image

def get_name(img_src):
    org = cv2.imread(img_src)
    cropped = crop(org, [700, 300], [300, 45])
    cropped = filter_image(cropped)
    name = read_img(cropped)

    return name

def get_company(img_src):
    org = cv2.imread(img_src)
    cropped = crop(org, [700, 765], [300, 45])
    cropped = filter_image(cropped)
    company = read_img(cropped)

    return company

def does_match_logo(img_src):
    img_rgb = cv2.imread(img_src)
    img_rgb = cv2.resize(img_rgb, (1920, 1080), interpolation =cv2.INTER_AREA)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(LOGO,0)
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where( res >= threshold)

    for pt in zip(*loc[::-1]):
        return True

    return False

def process_bio_image(img_src):
    name = get_name(img_src)
    company = get_company(img_src)
    matches = does_match_logo(img_src)

    return {
        "name" : name,
        "company": company,
        "matches": matches,
    }