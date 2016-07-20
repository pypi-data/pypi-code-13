import logging
import os
from PIL import ImageFont
import re


logger = logging.getLogger(__name__)
insensitive_re = re.compile(re.escape(' Regular'), re.IGNORECASE)


class FontNotFoundError(Exception):
    pass


def get_filepaths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  
    return file_paths


def get_font_alias(font):
    return insensitive_re.sub("", " ".join(font.getname())).replace(" ", "")


def get_font_file(name, f, fontdir):
    for filepath in get_filepaths(fontdir):
        try:
            font = ImageFont.truetype(filepath)
        except OSError:
            logger.debug('%s is not a font' % filepath)
        else:
            if get_font_alias(font).lower() == name.replace(" ", "").lower():
                return filepath
        finally:
            del font


def get_font(name, f='ttf', fontdir=None, size=None):
    if fontdir is None:
        raise FontNotFoundError("Font '%s' not found." % name)
    fontpath = get_font_file(name, f, fontdir)
    if fontpath is None:
        raise FontNotFoundError("Font '%s' not found." % name)
    if size is None:
        font = ImageFont.truetype(fontpath)
    else:
        font = ImageFont.truetype(fontpath, size=size)
    return font
