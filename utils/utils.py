import qrcode
import os
import pandas as pd
import numpy as np
import argparse
import hashlib
import time
import cv2
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
from matplotlib import pyplot as plt
import math


def read_template(path, scale=1):
    img = Image.open(path)
    if scale != 1:
        img = img.resize((int(img.size[0] * scale), int(img.size[1] * scale)))
    return img


def extract_words(input_string):
    return input_string.split(' ')


def draw_centered_text(img, text, x, y, font, color):
    draw = ImageDraw.Draw(img)
    draw.multiline_text((x, y), text, font=font, fill=color, align='center', spacing=10, anchor='mm')
    return img


def extract_lines_text(txt, max_chrs):
    words = extract_words(txt)
    lines = []
    line = ''
    for word in words:
        if len(line) + len(word) + 1 <= max_chrs:
            line += word + ' '
        else:
            lines.append(line[:-1])
            line = word + ' '
    lines.append(line[:-1])
    return lines


def draw_text_box(img, text, max_width, max_high, x, y, font, color):
    draw = ImageDraw.Draw(img)
    _, _, w, h = draw.textbbox((0, 0), text, font=font)
    max_lines = max_high // h
    max_chrs_per_line = math.ceil((max_width / w) * len(text))
    lines = math.ceil(len(text) / max_chrs_per_line)
    max_h = lines * h
    lines_text = extract_lines_text(text, max_chrs_per_line)
    draw_centered_text(img, "\n".join(lines_text), x, y, font, color)
    return img