from colorama import Back, init, Style
import psutil
import math
import humanize


def print_bar(label, value, max, labelwidth):
    colors = ([Back.GREEN] * 15) + ([Back.YELLOW] * 3) + ([Back.RED] * 2)

    filled = '▓'
    empty = '░'

    filled_count = math.ceil((value / max) * 20)

    print('{}{}'.format(label, ' ' * ((labelwidth + 1) - len(label))), end='')
    print('[', end='')
    for i in range(0, 20):
        if i > filled_count:
            char = empty
        else:
            char = filled
        color = colors[i]
        print(color + char, end='')

    print(Style.RESET_ALL + '] ', end='')
    print('{} / {} ({:0.1f}%, {} free)'.format(humanize.naturalsize(value, binary=True),
                                               humanize.naturalsize(max, binary=True),
                                               (value / max) * 100, humanize.naturalsize(max - value, binary=True)))


def main():
    init()

    bars = []
    labelwidth = 0
    for partition in psutil.disk_partitions():
        usage = psutil.disk_usage(partition.mountpoint)
        label = partition.mountpoint

        if len(label) > labelwidth:
            labelwidth = len(label)

        bars.append((label, usage.total, usage.used))

    for label, total, used in bars:
        print_bar(label, used, total, labelwidth)