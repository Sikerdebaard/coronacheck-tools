import json
import cv2
import functools
import numpy as np


def parse_input(input_format, input_path):
    """
    Some glue-logic for the cli convert tool to read input data in the correct format

    :param input_format: one of (QR, RAW, ASN1, JSON)
    :param input_path: path to the file that needs to be loaded into memory
    :return: the data, either as str, bytes or CV2 image
    """

    readmode = 'r'
    decoder = None
    if input_format == 'ASN1':
        readmode = 'rb'
    elif input_format == 'JSON':
        decoder = json.load
    elif input_format == 'QR':
        decoder = lambda fh: cv2.imdecode(np.frombuffer(fh.read(), dtype='uint8'), flags=cv2.IMREAD_COLOR)
        readmode = 'rb'

    with open(input_path, readmode) as fh:
        if decoder:
            input_data = decoder(fh)
        else:
            input_data = fh.read()

    return input_data


def write_output(data, output_format, output_path):
    mode = 'w'
    encoder = None
    if output_format == 'RAW':
        extension = '.raw'
    elif output_format == 'ASN1':
        extension = '.asn1.der'
        mode = 'wb'
    elif output_format == 'JSON':
        extension = '.json'
        encoder = json.dumps
    elif output_format == 'QR':
        mode = 'wb'
        extension = '.png'
        encoder = lambda imgdata: cv2.imencode('.png', imgdata)[1]

    if not isinstance(data, list):
        data = [data]

    counter = 0
    total_len = len(data)
    for d in data:
        fname = output_path / f'dhc_data_{counter:03}{extension}'
        print(f'Writing output {counter + 1}/{total_len} to {fname}')
        with open(fname, mode) as fh:
            if encoder:
                fh.write(encoder(d))
            else:
                fh.write(d)
        counter += 1
