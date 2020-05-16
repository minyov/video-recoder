import os
import cv2
import tempfile

from django.db.models.fields.files import FieldFile


def get_preview(file: FieldFile) -> bytes:
    temp_filename = os.path.join(tempfile.gettempdir(), file.name.split('/')[-1])
    with open(temp_filename, "wb") as _file:
        file.seek(0)
        _file.write(file.read())

    capture = cv2.VideoCapture(temp_filename)
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    capture.set(cv2.CAP_PROP_POS_FRAMES, round(frame_count / 2))

    capture.grab()
    retval, img = capture.retrieve(0)

    image_bytes = cv2.imencode("temp/preview.jpg", img)[1].tobytes()

    capture.release()

    os.remove(temp_filename)

    return image_bytes
