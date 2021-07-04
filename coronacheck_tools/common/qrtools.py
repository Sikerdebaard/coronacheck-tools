import cv2
import qrcode
import numpy as np

from PIL import Image
from pyzbar.pyzbar import decode


def raw_to_qr(output_file, raw):
    qr = qrcode.QRCode()

    qr.add_data(raw)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    img.save(output_file)


def raw_to_pil_qr(raw):
    qr = qrcode.QRCode()

    qr.add_data(raw)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")

    return img


def raw_to_cv2_qr(raw):
    return pil_to_cv2(raw_to_pil_qr(raw))


def cv2_read_qr(cv2img):
    return pil_read_qr(cv2_to_pil(cv2img))


def pil_read_qr(pil_img):
    codes = decode(pil_img)  # auto detect code type

    all_codes = []

    if codes:
        for code in codes:
            all_codes.append(code.data.decode("utf-8"))

    return all_codes


def read_qr(imgpath):
    im = cv2.imread(imgpath)

    codes = decode(cv2_to_pil(im))  # auto detect code type

    all_codes = []

    if codes:
        for code in codes:
            all_codes.append(code.data.decode("utf-8"))

    return all_codes


def cv2_to_pil(cv2img):
    img = cv2.cvtColor(cv2img, cv2.COLOR_BGR2RGB)
    return Image.fromarray(img)


def pil_to_cv2(pilimg):
    img = pilimg.convert('RGB')
    cv2img = np.array(img)
    return cv2img[:, :, ::-1].copy()  # RGB to BGR
