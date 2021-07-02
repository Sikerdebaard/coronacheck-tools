import cv2
from pyzbar.pyzbar import decode


def cv2_read_qr(cv2img):
    codes = decode(cv2img)  # auto detect code type

    all_codes = []

    if codes:
        for code in codes:
            all_codes.append(code.data.decode("utf-8"))

    return all_codes


def read_qr(imgpath):
    im = cv2.imread(imgpath)

    codes = decode(im)  # auto detect code type

    all_codes = []

    if codes:
        for code in codes:
            all_codes.append(code.data.decode("utf-8"))

    return all_codes
