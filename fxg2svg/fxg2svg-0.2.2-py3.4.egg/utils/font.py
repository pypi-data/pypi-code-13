import logging
import os
from PIL import ImageFont


logger = logging.getLogger(__name__)


FONTDIRS = (
    '/usr/share/fonts',
    '/home/hus/.fonts',
)


class FontNotFoundError(Exception):
    pass


def get_filepaths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  
    return file_paths


def _getfontname(filepath):
    if not filepath.lower().endswith('ttf'):
        return None
    try:
        f = ImageFont.truetype(filepath)
        return f.font.family
    except OSError:
        logger.debug('%s is not a true type font' % filepath)
        return None


def _getfontfile(font_family, f, dirs=FONTDIRS):
    for d in dirs:
        for filepath in get_filepaths(d):
            if _getfontname(filepath) == font_family:
                return filepath


def get_font(name, f='ttf', dirs=FONTDIRS, size=None):
    fontpath = _getfontfile(name, f, dirs)
    if fontpath is None:
        raise FontNotFoundError("Font '%s' not found." % name)
    if size is None:
        font = ImageFont.truetype(fontpath)
    else:
        font = ImageFont.truetype(fontpath, size=size)
    return font
