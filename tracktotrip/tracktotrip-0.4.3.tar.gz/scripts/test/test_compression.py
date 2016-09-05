from tracktotrip import Track
import numpy as np
import matplotlib.pyplot as plt

temp_trk = [
    Track.from_gpx('/Users/ruipgil/Downloads/20160830.gpx')[0],
    # Track.from_gpx('/Users/ruipgil/Downloads/20160830.gpx')[0],
]

segs = []
for trke in temp_trk:
    segs.extend(trke.segments)
trk = Track("", segs)
trk.compute_metrics()
# trk.to_trip('', 0, 5.0, 0.15, 80, 0.3, '%Y-%m-%d')
plt.axis('equal')
plt.axis('off')
for segment in trk.segments:
    plt.plot([p.lon for p in segment.points], [p.lat for p in segment.points], 'o-')

plt.savefig('compression_baseline.pdf')
plt.clf()
plt.axis('equal')
plt.axis('off')

n_points = sum([len(s.points) for s in trk.segments])
trk2 = trk.copy()
trk.simplify(0.000015, 2.0, 1.0)
for segment in trk.segments:
    plt.plot([p.lon for p in segment.points], [p.lat for p in segment.points], 'o-')
result = sum([len(s.points) for s in trk.segments])
print("From %d to %d points" % (n_points, result))
print("Compression: %f" % (n_points/float(result)))

plt.savefig('compression_spt.pdf')
plt.clf()
plt.axis('equal')
plt.axis('off')

trk = trk2
trk.simplify(0.000015, 2.0, 1.0, True)
for segment in trk.segments:
    plt.plot([p.lon for p in segment.points], [p.lat for p in segment.points], 'o-')
result = sum([len(s.points) for s in trk.segments])
print("From %d to %d points" % (n_points, result))
print("Compression: %f" % (n_points/float(result)))

plt.savefig('compression_drp.pdf')

# plt.show()
