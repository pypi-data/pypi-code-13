import emoji
import csv


emoji_sent = dict()
with open('/Volumes/cchen224/emoji.csv', 'r') as i:
    csvreader = csv.reader(i)
    for row in csvreader:
        strs = ':' + '_'.join(row[2].split()).lower() + ':'
        uni = emoji.emojize(strs)
        if not uni.endswith(':'):
            emoji_sent[uni] = float(row[1])

with open('/Users/cchen224/Downloads/data/face', 'r') as i:
    face = dict(map(lambda (w,m): (w, float(m) / 4.), [wmsr.strip().split('\t')[0:2] for wmsr in i ]))

emoji_sent.update(face)