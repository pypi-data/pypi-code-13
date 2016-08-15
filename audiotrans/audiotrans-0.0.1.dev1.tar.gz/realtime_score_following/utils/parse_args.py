# -*- coding: utf-8 -*-


def parse_args():

    from argparse import ArgumentParser, RawTextHelpFormatter

    parser = ArgumentParser(
        description="""Realtime audio transform tool with transform modules""",
        formatter_class=RawTextHelpFormatter)

    parser.add_argument('filepath', nargs='?',
                        help="""File path to read as stream and transform.
                        """)
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help="""Run as verbose mode
                        """)
    parser.add_argument('-t', '--transform', dest='transforms', default=[], action='append',
                        help="""Transform module to apply.
Specify only module name like:

  -t stft

or, with options using sub-arguments like:

  -t '[ stft --n_fft 1024 --n_hop 256 ]'
                        """)
    parser.add_argument('-b', '--bufsize', dest='bufsize', default=1024,
                        help="""Number of samples to read stream per iteration.
                        """)
    parser.add_argument('-c', '--chart-type', dest='chart_type', default=None,
                        help="""Chart type to data visualization.
Valid chart type are 'freq', 'spectrum',
or if not specified, no chart appears.
                        """)
    parser.add_argument('-B', '--batch', action='store_true', default=False,
                        help="""Run as batch mode.
                        """)
    parser.add_argument('-o', '--output', default=None,
                        help="""Destination filename for transformed results
as python serialized object (pickle).
If not specified, no results would be outputed.
                        """)
    parser.add_argument('-s', '--start_from', default=0,
                        help="""Start to load from specific position of audio.
                        """)

    return parser.parse_args()
