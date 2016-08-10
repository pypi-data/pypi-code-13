from obspy import read
from eqcorrscan.core.match_filter import normxcorr2
from eqcorrscan.utils.plotting import triple_plot
st = read()
template = st[0].copy().trim(st[0].stats.starttime + 8,
                           st[0].stats.starttime + 12)
tr = st[0]
ccc = normxcorr2(template=template.data, image=tr.data)
tr.data = tr.data[0:len(ccc[0])]
triple_plot(cccsum=ccc[0], cccsum_hist=ccc[0], trace=tr, threshold=0.8)