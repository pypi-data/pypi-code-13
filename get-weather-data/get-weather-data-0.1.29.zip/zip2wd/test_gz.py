import gzip
import csv

with gzip.open('data/1900.csv.gz', 'rb') as f:
    file_content = f.read()

print file_content[:200]
