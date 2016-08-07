import argparse
import os
import struct
from PIL import Image
import numpy as np
from vec2img import __version__, __description__

def convert(file, width, height, dir, ext='png'):
    if not os.path.isdir(dir): os.mkdir(dir)
    
    with open(file, 'rb') as f:
        count, size, _, _ = struct.unpack('<iihh', f.read(12))
        for i in range(count):
            f.read(1)
            img  = np.fromfile(f, '<h', size).reshape(height, width)
            path = os.path.join(dir, "%d.%s" % (i+1, ext))
            Image.fromarray(img).convert('RGB').save(path)

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=__description__, add_help=False)
    parser.add_argument('vec', type=str, help='vec file')
    parser.add_argument('-o', '--out', type=str, required=True, help='output path')
    parser.add_argument('-w', '--width', type=int, default=24, help='image width')
    parser.add_argument('-h', '--height', type=int, default=24, help='image height')
    parser.add_argument('-e', '--ext', type=str, default='png', help='image extension')
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('--help', action='help', help='show this help message and exit')
    args = parser.parse_args()
    
    convert(args.vec, args.width, args.height, args.out, args.ext)
