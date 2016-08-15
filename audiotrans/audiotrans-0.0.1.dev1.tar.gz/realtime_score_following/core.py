# -*- coding: utf-8 -*-

import sys
import numpy as np
from logging import getLogger, StreamHandler, Formatter, DEBUG
import traceback

from .utils import parse_args, parse_subargs

logger = getLogger(__name__)
handler = StreamHandler()
handler.setFormatter(Formatter('[%(asctime)s %(levelname)s %(module)s] %(message)s'))
logger.addHandler(handler)


def main():

    # ------------------
    # parse arguments
    # ------------------

    args = parse_args()

    if args.batch:
        from .batch import batch
        sys.exit(batch())

    if args.verbose:
        logger.setLevel(DEBUG)
        handler.setLevel(DEBUG)

    # parse transform subargs to like `[name:str, sub_args:list, sub_kwargs:dict]`
    transforms = [parse_subargs(t) for t in args.transforms]
    bufsize = int(args.bufsize)
    chart_type = args.chart_type

    import wave

    # open target file
    wf = wave.open(args.filepath, 'rb')
    framerate = wf.getframerate()
    channels = wf.getnchannels()
    init_frame_count = int(float(args.start_from) / 1000 * framerate)
    wf.readframes(init_frame_count)

    # ------------------
    # imports
    # ------------------

    import array
    from functools import reduce
    import time
    import threading
    import pyaudio
    import matplotlib
    import matplotlib.pyplot as plt
    matplotlib.use('TkAgg')

    # load each transform modules with parsed *sub_args and **sub_kwargs
    try:
        tr_funcs = [
            getattr(__import__('{}.tr.{}'.format(__package__, tr[0]), fromlist=['.']),  # import
                    ''.join(tr[0].title().split('_')) + 'Transform')  # retrieve camel cased class
            (bufsize, framerate, channels, verbose=args.verbose, *tr[1], **tr[2])  # construct
            .transform  # retrieve transform function
            for tr in transforms]  # for each transforms specified by arguments
    except AttributeError as e:
        logger.error(e)
        if str(e).find("object has no attribute 'transform'") > 0:
            logger.error('transform class must have `transform` function')
        raise e

    # ------------------
    # main
    # ------------------

    total_frame_count = init_frame_count
    transformed = None
    results = None

    def analyze():
        logger.debug('#analyze')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=channels,
                        rate=framerate,
                        output=True,
                        frames_per_buffer=bufsize,
                        stream_callback=callback)

        logger.debug('opening stream...')
        stream.start_stream()

        while stream.is_active():
            time.sleep(0.1)

        logger.debug('closing stream...')
        stream.stop_stream()
        stream.close()
        wf.close()
        p.terminate()

        # output transformed results
        if args.output is not None:
            nonlocal results
            import pickle
            pickle.dump(np.array(results), open(args.output, 'wb'))

    def callback(in_data, frame_count, time_info, status):
        nonlocal transformed, total_frame_count
        data = wf.readframes(frame_count)
        logger.info('loaded audio at {:.0f}ms'.format(total_frame_count / framerate * 1000))

        total_frame_count += frame_count

        try:
            logger.debug('start transform with transform modules...')
            transformed = reduce(lambda acc, m: m(acc), tr_funcs, data)

        except Exception as e:
            logger.error(e)
            traceback.print_exc()

        else:
            logger.info('transform finished')

            # preserve transformed results
            if args.output is not None:
                nonlocal results
                if results is None:
                    results = transformed
                else:
                    results = np.append(results, transformed, axis=0)

        # output transformed audio
        def is_audio(data):
            dim_data = len(np.shape(data))
            return hasattr(data, 'dtype') and data.dtype == 'float64' and dim_data == 1

        if is_audio(transformed):
            t = (transformed * 10000).astype(int)
            if channels == 2:
                t = np.concatenate((t, t)).reshape(2, -1).T.reshape(1, -1)[0]
            ndata = array.array('h', t).tostring()
            if len(data) == len(ndata):
                data = ndata

        return (data, pyaudio.paContinue)

    # start analyze with sub-thread
    th_analyze = threading.Thread(target=analyze)
    logger.debug('start analyzing thread...')
    th_analyze.start()

    # ------------------
    # visualization
    # ------------------

    if chart_type not in ['freq', 'spectrum']:
        # done without visualization
        return

    # setup canvas
    fig = plt.figure()

    # to use shape of transformed data for axis of plot, wait to end first transform
    while transformed is None:
        pass

    if chart_type == 'freq':
        gen_axis = gen_axes_for_freq
        draw = draw_line_for_freq
        xhop = 50  # to preventing bad performance
        pass

    elif chart_type == 'spectrum':
        gen_axis = gen_axes_for_spectrum
        draw = draw_line_for_spectrum
        xhop = 1
        pass

    # create axes
    axes = gen_axis(fig, transformed, framerate, channels, xhop)
    fig.show()

    # cache background after `.show()`
    background = fig.canvas.copy_from_bbox(axes.bbox)

    # create line object after cache background
    xmax = int(axes.get_xlim()[1])
    line = axes.plot(np.arange(0, xmax), np.zeros(xmax))[0]

    while True:
        # draw...
        if transformed is None:
            continue
        time.sleep(0.01)
        fig.canvas.restore_region(background)
        draw(axes, line, transformed, xhop)
        fig.canvas.blit(axes.bbox)


# =======================
# draw functions
# =======================

def gen_axes_for_freq(fig, wave_array, framerate, channels, xhop):
    axes = fig.add_subplot(1, 1, 1)
    axes.set_aspect('auto')
    axes.set_xlim(0, int(framerate / xhop))
    axes.set_ylim(-1, 1)
    return axes


def gen_axes_for_spectrum(fig, data, framerate, channels, xhop):
    axes = fig.add_subplot(1, 1, 1)
    axes.set_aspect('auto')
    xmax = int(np.shape(data)[1] / xhop)
    axes.set_xlim(0, xmax)
    axes.set_xticks(np.linspace(0, xmax, 5))  # fold less than nyquist
    axes.set_xticklabels(np.linspace(0, framerate / 2, 5))
    axes.set_yticks(np.linspace(0, 100, 5))
    axes.set_ylim(0, 100)
    return axes


def draw_line_for_freq(axes, line, wave_array, xhop):
    d = wave_array[::xhop]
    prev_x, prev_y = line.get_data()
    line.set_data(prev_x, np.append(prev_y[len(d):], d))
    axes.draw_artist(line)


def draw_line_for_spectrum(axes, line, data, xhop):
    dim = len(np.shape(data))
    if dim == 1:
        d = data[::xhop]
    elif dim == 2:
        d = data[0][::xhop]

    line.set_data(np.arange(len(d)), d)
    axes.draw_artist(line)
