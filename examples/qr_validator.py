from coronacheck_tools import decode_qr
from coronacheck_tools.verification.verifier import validate_raw
from pathlib import Path

import cv2
import tempfile


with tempfile.TemporaryDirectory() as tmpdir:
    qr_out_path = Path(tmpdir) / 'qrclone.png'
    qr_in_path = Path(tmpdir) / 'qrorginal.png'

    # Use first webcam. If there are multiple you probably want to change this.
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

        results = [validate_raw(x) for x in codes]

        for result in results:
            if result[0]:
                print("🥳 Code is valid", result[1])
            else:
                print("😭 Code invalid", result[1])
