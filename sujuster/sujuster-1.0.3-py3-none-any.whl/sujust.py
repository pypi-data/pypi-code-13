from argparse import ArgumentParser
from datetime import datetime, timedelta
from sys import stdout

config = None


def parse_args():
    global config
    parser = ArgumentParser()
    parser.add_argument("srt_file",
                        help="The subtitle file to adjust")
    parser.add_argument("offset",
                        type=float,
                        help="The offset of all subtitles. A positive number "
                             "means that the subtitle will be later, a "
                             "negative number that it will appear earlier. The "
                             "number is a floating point number (1.3) "
                             "representing seconds.")
    parser.add_argument("-o", "--outfile",
                        help="specify the output file. Default: output "
                             "to stdout",
                        default=None)
    config = parser.parse_args()


def get_subtitles(infile):
    """
    Generator which returns subtitles from a given already opened input file.

    :param infile: The opened file-handle (or file-like object)
    :return: A generator
    """
    line = "start"
    while line:
        line = infile.readline()
        if not line.strip(): continue
        st = [line.strip(), infile.readline().strip()]
        line = infile.readline()
        while line.strip():
            st.append(line.strip())
            line = infile.readline()
        yield st


def adjust_subtitle(st, td):
    # we only know microseconds, though the timestamp has milliseconds ...
    markers = [x + "000" for x in st[1].split(" --> ")]
    marker_objs = [datetime.strptime(x, "%H:%M:%S,%f") + td for x in markers]
    st[1] = "{} --> {}".format(
        marker_objs[0].strftime("%H:%M:%S,%f")[:-3],
        marker_objs[1].strftime("%H:%M:%S,%f")[:-3]
    )
    return st


def adjust_subtitles(outfile):
    # see http://stackoverflow.com/a/2459793/902327
    td = timedelta(seconds=config.offset)
    with open(config.srt_file, "r", encoding='utf-8-sig') as infile:
        for num, st in enumerate(get_subtitles(infile)):
            adjust_subtitle(st, td)
            st_text = "\n".join(st) + "\n\n"
            outfile.write(st_text)


def start():
    parse_args()
    if config.outfile:
        with open(config.outfile, "w", encoding="utf-8") as outfile:
            adjust_subtitles(outfile)
    else:
        adjust_subtitles(stdout)
