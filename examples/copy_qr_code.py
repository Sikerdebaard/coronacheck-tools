"""
Read a QR code from webcam and copy it
"""

from coronacheck_tools import decode_qr, raw_to_qr
from pathlib import Path

import cv2
import tempfile


with tempfile.TemporaryDirectory() as tmpdir:
    qr_out_path = Path(tmpdir) / 'qrclone.png'
    qr_in_path = Path(tmpdir) / 'qrorginal.png'

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        raise IOError("Cannot open webcam")

    while True:
        ret_val, img = cam.read()

        cv2.imwrite(str(qr_in_path), img)

        frame = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        cv2.imshow('Input', frame)

        c = cv2.waitKey(1)
        if c >= 27:
            raise SystemExit('Exiting: key pressed')

        codes = decode_qr(qr_in_path, 'raw')

        if len(codes) > 0:
            break


    raw_to_qr(qr_out_path, codes[0])

    cloned_qr = cv2.imread(str(qr_out_path))
    cloned_qr = cv2.resize(cloned_qr, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    cv2.imshow('Cloned QR', cloned_qr)
    cv2.waitKey(0)
