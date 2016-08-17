# -*- coding: utf-8 -*-

import numpy as np
import logging
from .utils import parse_args, parse_subargs

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
logger.addHandler(handler)


def batch():

    # ------------------
    # parse arguments
    # ------------------

    args = parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)
        handler.setLevel(logging.DEBUG)

    # parse transform subargs like `[name:str, sub_args:list, sub_kwargs:dict]`
    transforms = [parse_subargs(t) for t in args.transforms]

    import wave

    # open target file
    wf = wave.open(args.filepath, 'rb')
    framerate = wf.getframerate()
    channels = wf.getnchannels()
    data = wf.readframes(wf.getnframes())

    # ------------------
    # imports
    # ------------------

    from functools import reduce

    # load each transform modules with parsed *sub_args and **sub_kwargs
    tr_funcs = [
        getattr(__import__('{}.tr.{}'.format(__package__, tr[0]), fromlist=['.']),  # import module
                ''.join(tr[0].title().split('_')) + 'Transform')  # retrieve camel cased class
        (1, framerate, channels, verbose=args.verbose, *tr[1], **tr[2])  # construct
        .transform  # retrieve transform function
        for tr in transforms]  # for each transforms specified by arguments

    # ------------------
    # main
    # ------------------

    transformed = None

    try:
        transformed = reduce(lambda acc, m: m(acc), tr_funcs, data)
    except AttributeError as e:
        logger.error('transform class must have `transform` function')
        raise e

    # output transformed results
    if args.output is not None:
        import pickle
        pickle.dump(np.array(transformed), open(args.output, 'wb'))

    return 0
