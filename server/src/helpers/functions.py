import base64
import io
from PIL import Image


def unnormalize_box(bbox, width, height):
    return [
        width * (bbox[0] / 1000),
        height * (bbox[1] / 1000),
        width * (bbox[2] / 1000),
        height * (bbox[3] / 1000),
    ]


def image_to_base64_data_uri(file_path, quality=85, max_size=(400, 400)):
    with Image.open(file_path) as img:
        img.thumbnail(max_size)  # Resize the image
        buffered = io.BytesIO()
        img.convert("RGB").save(buffered, format="JPEG", quality=quality)
        base64_data = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return f"data:image/jpeg;base64,{base64_data}"