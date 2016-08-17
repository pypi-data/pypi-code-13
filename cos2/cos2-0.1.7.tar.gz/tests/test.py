__author__ = 'miya'


import os
import cos2
import hashlib

filename = "my.txt"
num_to_upload=2

total_size = os.path.getsize(filename)
print total_size

with open(filename, 'rb') as fileobj:
    offset = 0
    while offset < total_size:
        part_data=cos2.SizedFileAdapter(fileobj, num_to_upload)
        hash = hashlib.md5()
        part_md5=hash.update(str(part_data))
        part_md5=hash.hexdigest()
        print (part_md5)
        offset += num_to_upload
        print offset

