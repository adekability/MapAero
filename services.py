import io
import zipfile
import random

import sys
import os

from PIL import Image

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    """base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)"""
    return relative_path

def get_zipfile(records):
    b = io.BytesIO()
    zf = zipfile.ZipFile(b, mode='w')
    for record in records:
        zf.writestr(record[0], record[3])
    zf.close()
    b.seek(0)
    return b


def generate_color():
    color = tuple([random.randint(0, 255) for _ in range(3)])
    color_str = str(color)
    color_str = color_str.replace(" ", "")
    return f"rgb{color_str}", color


def generate_color_str(taken_colors: list):
    taken_colors = [color[0] for color in taken_colors]
    colors = ['red', 'darkred', 'orange', 'green', 'darkgreen', 'blue', 'purple', 'darkpurple', 'cadetblue']
    for color in colors:
        if color not in taken_colors: return color


def convert_color(color: str, target_color: tuple):
    input_path = 'static/images/vector.png'
    file_path = color.replace("rgb(", "").replace(",", "").replace(")", "")
    output_path = f'static/images/{file_path}.png'
    img = Image.open(input_path).convert("RGBA")
    data = img.getdata()

    new_data = []
    for item in data:
        # Check if the pixel color is black
        if item[:3] == (0, 0, 0):
            # Change black pixels to the target color
            new_data.append((*target_color, item[3]))  # Keep the alpha channel unchanged
        else:
            new_data.append(item)

    # Update image data
    img.putdata(new_data)

    # Save image
    img.save(output_path, "PNG")
