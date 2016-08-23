#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import re
import sys
import time
from datetime import datetime
from io import BytesIO

import click
from PIL import Image, ImageColor
from selenium import webdriver


def valid_filename(value):
    value = value.strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', value)


def take_screenshot(url, sleep=0, width=1280):
    browser = webdriver.PhantomJS()
    browser.set_window_size(width, 1200)  # phantomJs height doesn't really matter - it screenshots the full page
    browser.get(url)

    if sleep:
        print('Taking a nap, see you in {} seconds'.format(sleep))
        time.sleep(sleep)

    screenshot_from_selenium = BytesIO(browser.get_screenshot_as_png())
    browser.quit()

    screenshot = Image.open(screenshot_from_selenium)

    # paste the screenshot onto white, since it's possible the website had a transparent background
    white_background = Image.new('RGBA', (screenshot.width, screenshot.height), color=ImageColor.getrgb('white'))
    white_background.paste(screenshot, mask=screenshot.split()[3])
    return white_background


@click.command()
@click.argument('url')
@click.option('--output', help="Filename for the screenshot (defaults to the domain name)")
@click.option('--sleep', default=0, help="Wait before taking the screenshot to allow asynchronous scripts to load")
@click.option('--width', default=1280, help="Specify the width of the browser window")
def mkscreenshot(url, output, sleep, width):
    if not url.startswith('http://') and not url.startswith('https://'):
        sys.exit('URL must start with http:// or https://')

    if not output:
        filename = valid_filename(url.split('://')[-1])
        filename += datetime.now().strftime('-%Y%m%d-%H%M%S')
    else:
        # remove the .png if it's there so we don't get .png.png
        filename = output.replace('.png', '')

    image = take_screenshot(url, int(sleep), width)
    image.save(filename + '.png')


if __name__ == '__main__':
    mkscreenshot()
