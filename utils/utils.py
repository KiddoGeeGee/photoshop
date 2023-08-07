import io
import cv2
import base64
import numpy as np


def decode_base64_to_image(encoding):
    image = np.frombuffer(base64.b64decode(encoding), np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


def convert_to_b64_list(images):
    base64images = []
    for image in images:
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        byte_im = base64.b64encode(buf.getvalue())
        base64images.append(byte_im)
    return base64images