#!/usr/bin/env python

# filter image files
# resize image to the output size
# set pixel peek pot
# read pixel and find top black border and bottom black border height
# full-image vs subtitle-only merge
# output the final image file

import sys
import const
from PIL import Image

def scale_image(output_width, image):
    width, height = image.size
    output_height = int(round(height * (output_width * 1.0 / width)))
    return image.resize((output_width, output_height), Image.ANTIALIAS)

def scale_image(output_width, subtitle_height, image):
    width, height = image.size
    ratio = output_width * 1.0 / width
    output_height = int(round(height * ratio)
    subtitle_height = int(round(subtitle_height * ratio))
    resized = image.resize((output_width, output_height), Image.ANTIALIAS)
    return subtitle_height, resized

def crop_image_border(image):
    width, height = image.size
    top_border = find_top_border(image)
    bottom_border = find_bottom_border(image)
    output_height = bottom_border - top_border
    crop = image.crop((0, top_border, width, bottom_border))
    return output_height, crop

def find_top_border(image):
    peek = []
    width, height = image.size
    width_step = width / 10
    height_step = 16
    for i in range(0, width, width_step):
        peek.append(i)

    border_height = height_step
    while(True):
        for p in peek:
            r, g, b = image.getpixel((p, border_height))
            # print height_step, h, border_height, (r, g, b)
            if r == g == b == 0:
                continue
            else:
                border_height -= height_step
                if height_step == 1:
                    return border_height
                else:
                    height_step = height_step >> 1
                    break
        border_height += height_step

def find_bottom_border(image):
    peek = []
    width, height = image.size
    width_step = width / 10
    height_step = 16
    for i in range(0, width, width_step):
        peek.append(i)

    border_height = height - 1
    while(True):
        for p in peek:
            r, g, b = image.getpixel((p, border_height))
            # print height_step, h, border_height, (r, g, b)
            if r == g == b == 0:
                continue
            else:
                border_height += height_step
                if height_step == 1:
                    return border_height
                else:
                    height_step = height_step >> 1
                    break
        border_height -= height_step

def process_images(output_width, output, files):
    output_image = None

    for index, f in enumerate(files):
        if not f.endswith(tuple(const.EXTENSIONS)):
            continue

        try:
            image = Image.open(f)
            resize_image = scale_image(output_width, image)
            rgb_image = resize_image.convert('RGB')
            output_height, crop = crop_image_border(rgb_image)

            # TODO: it'll fail to create a correct image if input images have different size
            if output_image is None:
                total_height = output_height * len(files)
                output_image = Image.new("RGB", (output_width, total_height))
            output_image.paste(crop, (0,
                                      index * output_height,
                                      output_width,
                                      (index + 1) * output_height))

        except IOError:
            print "IOError: cannot open image file"

    if output_image is not None:
        output_image.save(output)


def process_subtitle_only(output_width, output, subtitle_height, files):
    output_image = None

    prepared_images = []
    for index, f in enumerate(files):
        if not f.endswith(tuple(const.EXTENSIONS)):
            continue

        try:
            image = Image.open(f)
            subtitle_height, resize_image = scale_image(output_width, subtitle_height, image)
            rgb_image = resize_image.convert('RGB')
            output_height, crop = crop_image_border(rgb_image)
            prepared_images.append((index, output_height, crop))

            if output_image is None:
                total_height = output_height + subtitle_height * (len(files) - 1)
                output_image = Image.new("RGB", (output_width, total_height))

        except IOError:
            print "IOError: cannot open image file"

    for index, output_height, crop in reversed(prepared_images):
        if output_image is not None:
            output_image.paste(crop, (0,
                                      index * subtitle_height,
                                      output_width,
                                      output_height + index * subtitle_height))

    if output_image is not None:
        output_image.save(output)


def main(sysargs=sys.argv[1:]):
    from cli import parser
    args = parser.parse_args(sysargs)
    if args.action == const.MERGE_ACTIONS[1]:
        process_images(args.output_width, args.output, args.files)
    elif args.action == const.MERGE_ACTIONS[0]:
        process_subtitle_only(args.output_width, args.output, args.subtitle_height, args.files)
    else:
        print "Error: Unknown merge action."
