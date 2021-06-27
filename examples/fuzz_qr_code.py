"""
Read a QR code from webcam and fuzz with it
"""

from coronacheck_tools import decode_qr, raw_to_qr, encode_dict
from pathlib import Path

import cv2
import tempfile
import copy

WindowName = "Main View"
view_window = cv2.namedWindow(WindowName, cv2.WINDOW_NORMAL)
cv2.setWindowProperty(WindowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.setWindowProperty(WindowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)


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

        wtitle = 'Input'
        cv2.imshow(wtitle, frame)

        c = cv2.waitKey(1)
        if c >= 27:
            raise SystemExit('Exiting: key pressed')

        codes = decode_qr(qr_in_path, 'dict')

        if len(codes) > 0:
            break
    cv2.destroyWindow(wtitle)

    dct = copy.deepcopy(codes[0])
    raw_to_qr(qr_out_path, encode_dict(dct))
    cloned_qr = cv2.imread(str(qr_out_path))
    cloned_qr = cv2.resize(cloned_qr, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    wtitle = 'This one should work'
    cv2.imshow(wtitle, cloned_qr)
    cv2.waitKey(0)
    cv2.destroyWindow(wtitle)

    print(dct)

    for key in dct['aDisclosed'].keys():
        if key in ('CredentialMetadata',):
            print(f'Skipping {key}')
            continue
        dct = copy.deepcopy(codes[0])
        fuzzed = 'A\x00' + dct['aDisclosed'][key]
        print(f"Changing {key} {dct['aDisclosed'][key]} to {fuzzed}")
        dct['aDisclosed'][key] = fuzzed
        raw_to_qr(qr_out_path, encode_dict(dct))

        cloned_qr = cv2.imread(str(qr_out_path))
        cloned_qr = cv2.resize(cloned_qr, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        wtitle = f"Fuzz {key} should not work"
        cv2.imshow(wtitle, cloned_qr)
        cv2.waitKey(0)
        cv2.destroyWindow(wtitle)
