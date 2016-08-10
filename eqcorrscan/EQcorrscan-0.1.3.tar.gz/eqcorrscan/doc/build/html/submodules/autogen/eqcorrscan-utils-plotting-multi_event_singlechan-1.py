from obspy import read, Catalog
from eqcorrscan.utils.sfile_util import read_event, readwavename
from eqcorrscan.utils.plotting import multi_event_singlechan
import glob, os
sfiles = glob.glob(os.path.
                   realpath('../../../tests/test_data/REA/TEST_') +
                   os.sep + '*')
catalog = Catalog()
streams = []
for sfile in sfiles:
    catalog.append(read_event(sfile))
    stream_path = os.path.                realpath('../../../tests/test_data/WAV/TEST_/' +                 readwavename(sfile)[0])
    stream = read(stream_path)
    # Annoting coping with seisan 2 letter channels
    for tr in stream:
        tr.stats.channel = tr.stats.channel[0] + tr.stats.channel[-1]
    streams.append(stream)
multi_event_singlechan(streams=streams, catalog=catalog,
                       station='GCSZ', channel='EZ')