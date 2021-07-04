#
# Required libs before use:
# apt install libzbar-dev libopencv-dev
# pip install coronacheck-tools>=1.1.1
#
from coronacheck_tools import cv2img_decode_qr
from coronacheck_tools import validate_raw
from PIL import Image

import cv2


# Use first webcam. If there are multiple you probably want to change this.
cam = cv2.VideoCapture(0)
if not cam.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret_val, img = cam.read()

    img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    cv2.imshow('Input', img)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    im_pil = Image.fromarray(img)

    c = cv2.waitKey(1)
    if c >= 27:
        raise SystemExit('Exiting: key pressed')

    codes = cv2img_decode_qr(im_pil, 'raw')

    # Allow international EHC qr codes?
    allow_international = True
    results = [validate_raw(x, allow_international=allow_international) for x in codes]

    for result in results:
        if result[0]:
            print("🥳 Code is valid", result[1])
        else:
            print("😭 Code invalid", result[1])
