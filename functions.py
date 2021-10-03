import numpy as np
import cv2
from PIL import Image
import pytesseract as tess
import pandas as pd
from skimage.io import imread, imshow
from skimage.segmentation import clear_border
import imutils
import os

def test_func():
    print('Functions are ready!')

def blackhat_morph(gray_img):
    rectKern = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
    blackhat = cv2.morphologyEx(gray_img, cv2.MORPH_BLACKHAT, rectKern)

    return rectKern, blackhat


def create_new_folder(name):

    new_folder = './' + name
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)


def save_files(destination_path, list_of_files):
    os.chdir(destination_path)
    for file in list_of_files:
        cv2.imwrite(file[0], file[1])

    os.chdir('..')


def find_light_mask(gray_img):
    squareKern = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    light = cv2.morphologyEx(gray_img, cv2.MORPH_CLOSE, squareKern)
    light = cv2.threshold(light, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    return light


def find_potential_regions(blackhat, rectKern, light_mask):
    gradX = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    gradX = np.absolute(gradX)
    (minVal, maxVal) = (np.min(gradX), np.max(gradX))
    gradX = 255 * ((gradX - minVal) / (maxVal - minVal))
    gradX = gradX.astype("uint8")

    gradX = cv2.GaussianBlur(gradX, (5, 5), 0)
    gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKern)
    thresh = cv2.threshold(gradX, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)

    thresh = cv2.bitwise_and(thresh, thresh, mask=light_mask)

    thresh = cv2.dilate(thresh, None, iterations=2)
    thresh = cv2.erode(thresh, None, iterations=1)

    return thresh


def potential_cnts(thresh_img, keep):
    cnts = cv2.findContours(thresh_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:keep]

    return cnts


def choose_and_draw(origin_img, cnts):
    minAR = 4
    maxAR = 5

    for cnt in cnts:
        (x, y, w, h) = cv2.boundingRect(cnt)
        ar = w / float(h)

        if ar >= minAR and ar <= maxAR:
            cv2.drawContours(origin_img, [cnt], -1, (0, 255, 0), 4)


def crop_license_plate(gray, cnts):
    minAR = 4
    maxAR = 5
    clearBorder = True

    LP_cnt = None
    LP_bitwise = None

    for cnt in cnts:
        (x, y, w, h) = cv2.boundingRect(cnt)
        ar = w / float(h)

        if ar >= minAR and ar <= maxAR:
            LP_cnt = cnt
            LP_gray = gray[y:y + h, x:x + w]
            LP_bitwise = cv2.threshold(LP_gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

            if clearBorder:
                LP_bitwise = clear_border(LP_bitwise)

            return LP_bitwise


def calc_points(text):
    summ = 0
    for char in text:
        if char.isdigit():
            summ += int(char)

    return summ % 10


def check_lucky(text):
    num = [int(i) for i in text if i.isdigit()]

    for i in range(len(num) - 1):
        if num[i] > num[i + 1]:
            return False

    return True


