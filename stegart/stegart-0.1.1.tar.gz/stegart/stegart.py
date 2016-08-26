import binascii
import cv2 as cv
import numpy as np
import argparse


def horizontal_line(canvas, hexdata, barheight):
    height, width = np.shape(canvas)[:2]
    bartop = height / 2 - barheight / 2
    barbottom = bartop + barheight
    barwidth = width / (len(hexdata) / 6)
    if barheight < 0 or barheight > height:
        raise ValueError("Invalid bar height specified")
    if barwidth < 1:
        raise ValueError("Image not wide enough for input data")
    for x in range(0, len(hexdata), 6):
        blue = int(hexdata[x:x+2], 16)
        green = int(hexdata[x+2:x+4], 16)
        red = int(hexdata[x+4:x+6], 16)
        barleft = barwidth * (x / 6)
        if x + 6 == len(hexdata):
            barright = width - 1
        else:
            barright = barleft + barwidth - 1
        cv.rectangle(canvas, (barleft, bartop), (barright, barbottom),
                     (blue, green, red), -1)

shapes = {
    'horizontal': horizontal_line,
}


def parse_input(input_string):
    try:
        int(input_string, 16)
        hexinput = input_string
    except:
        hexinput = binascii.hexlify(input_string)
    finally:
        hexoutput = hexinput
        while len(hexoutput) % 6 != 0:
            hexoutput = hexoutput + hexinput
        return hexoutput


def generate_image(input_string, height=512, width=512, background='FFFFFF',
                   shape='horizontal', modifier=25, output_file='stegart.png'):
    hexdata = parse_input(input_string)
    input_string.replace('#', '')
    canvas = np.empty((height, width, 3))
    canvas[:][:] = (int(background[4:6], 16),
                    int(background[2:4], 16),
                    int(background[0:2], 16))
    shapes[shape](canvas, hexdata, height / 10)
    cv.imwrite(output_file, canvas)


def main():
    parser = argparse.ArgumentParser(prog='stegart',
                                     description='Generate an image '
                                     'representing the given input')
    parser.add_argument('--height', default=512, type=int,
                        help='Height of the rendered image')
    parser.add_argument('--width', default=512, type=int,
                        help='Width of the rendered image')
    parser.add_argument('-b', '--background', default='FFFFFF', type=str,
                        help='The hex background color of the rendered image')
    parser.add_argument('-s', '--shape', help='Shape of the rendered image',
                        choices=shapes.keys(), type=str, default='horizontal')
    parser.add_argument('-o', '--output', default='stegart.png', type=str,
                        dest='output_file',
                        help='Output name of the rendered image')
    parser.add_argument('-m', '--modifier', default=25, type=int,
                        help='Shape size modifier')
    parser.add_argument('input_string', metavar='input', type=str,
                        help='The input data to render the image from')
    args = parser.parse_args()
    print "Input String" + args.input_string
    generate_image(args.input_string, args.height, args.width, args.background,
                   args.shape, args.modifier, args.output_file)

if __name__ == '__main__':
    main()
