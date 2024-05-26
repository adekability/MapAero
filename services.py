import io
import zipfile
import random

import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    """base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)"""
    return relative_path

def get_zipfile(records):
    b = io.BytesIO()
    zf = zipfile.ZipFile(b, mode='w')
    for record in records:
        zf.writestr(record[0], record[-2])
    zf.close()
    b.seek(0)
    return b


def generate_color():
    color = str(tuple([random.randint(0, 255) for _ in range(3)]))
    color = color.replace(" ", "")
    return f"rgb{color}"
