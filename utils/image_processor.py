import io

from PIL import Image


def resize_image(file: bytes, width: int, height: int) -> bytes:
    """
    Resizes image to given width and height
    """

    img = Image.open(io.BytesIO(file))
    img = img.convert('RGB')
    img = img.resize((width, height), Image.ANTIALIAS)

    img_byte_array = io.BytesIO()
    img.save(img_byte_array, format='JPEG', optimize=True, quality=75)

    return img_byte_array.getvalue()
