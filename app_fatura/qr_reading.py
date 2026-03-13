import cv2
import numpy as np
from pyzbar.pyzbar import decode

def read_qr(image_bytes:bytes):

    # Convert bytes to numpy array.
    bytes_to_np_array = np.frombuffer(image_bytes, np.uint8)

    # Decode image.
    image = cv2.imdecode(bytes_to_np_array, cv2.IMREAD_COLOR)

    # Decode QR
    decode_objects = decode(image)

    if decode_objects:
        return decode_objects[0].data.decode("utf-8")

    return None
