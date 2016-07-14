"""
CLI arguments definition

"""

import argparse

import const
from help_formatter import SingleMetavarHelpFormatter

parser = argparse.ArgumentParser(
    formatter_class=SingleMetavarHelpFormatter,
    prog='SubtitleJoiner',
    description="%(prog)s merge multiple images into one image.",
    epilog="""
    Suggestions and bug reports are appreciated:

        https://github.com/TreyCai/SubtitleJoiner/issues

    """
)

################################################################################
# Positional arguments
################################################################################
parser.add_argument(
    'files',
    type=str,
    nargs='+',
    help="""
    the image files that need to be merged

    """
)

################################################################################
# Optional arguments.
################################################################################
parser.add_argument(
    '-w', '--width',
    type=int,
    default=const.DEFAULT_OUTPUT_WIDTH,
    metavar='',
    dest='output_width',
    help="""
    the width of the output image

    """
)
## Deprecated
# parser.add_argument(
#     '-f', '--format',
#     type=str,
#     choices=['jpg', 'jpeg', 'png'],
#     default='png',
#     metavar='',
#     help="""
#     The format of the output image
#
#     """
# )
# TODO: not support yet
# parser.add_argument(
#     '-p', '--top-border',
#     type=int,
#     default=const.DEFAULT_BORDER,
#     metavar='',
#     dest='top',
#     help="""
#     the top border of each image
#
#     """
# )
# TODO: not support yet
# parser.add_argument(
#     '-b', '--bottom-border',
#     type=int,
#     default=const.DEFAULT_BORDER,
#     metavar='',
#     dest='bottom',
#     help="""
#     the bottom border of each image
#
#     """
# )
# TODO: not support yet
# parser.add_argument(
#     '-c', '--border-color',
#     type=int,
#     default=0x000000,
#     metavar='',
#     dest='border_color',
#     help="""
#     input the border color between images(hexadecimal)
#
#     """
# )
parser.add_argument(
    '-a', '--action',
    type=str,
    choices=const.MERGE_ACTIONS,
    default=const.MERGE_ACTIONS[0],
    metavar='',
    dest='action',
    help="""
    the type of the merge action.
    'subtitle' only keeps subtitle except the first image.
    'image' keeps all images

    """
)
parser.add_argument(
    '-s', '--subtitle-height',
    type=int,
    default=const.DEFAULT_SUBTITLE_HEIGHT,
    metavar='',
    dest='subtitle_height',
    help="""
    the distance between the top of the subtitle and
    the bottom of the image

    """
)
parser.add_argument(
    '-o', '--output',
    type=str,
    metavar='',
    dest='output',
    help="""
    the final output image file

    """
)
parser.add_argument(
    '-v', '--version',
    action='version',
    version='%(prog)s 0.1'
)
