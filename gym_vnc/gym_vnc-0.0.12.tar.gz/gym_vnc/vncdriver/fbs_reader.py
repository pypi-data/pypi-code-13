import json
import os
import struct

from gym_vnc import error

def find_footer(file):
    null = '\0\0\0\0'

    part = []
    for block in reversed_blocks(file):
        try:
            idx = block.rindex(null)
        except ValueError:
            part.append(block)
            continue
        else:
            part.append(block[idx+len(null):])
            part.reverse()
            return ''.join(part)

def reversed_blocks(file, blocksize=4096):
    "Generate blocks of file's contents in reverse order."
    file.seek(0, os.SEEK_END)
    here = file.tell()
    while 0 < here:
        delta = min(blocksize, here)
        here -= delta
        file.seek(here, os.SEEK_SET)
        yield file.read(delta)

class FBSReader(object):
    def __init__(self, path):
        self.file = open(path)
        version = self.file.read(12)
        if version != 'FBS 001.002\n':
            raise error.Error('Unrecognized FBS version: {}'.format(version))

        header = self.file.readline()
        pos = self.file.tell()
        footer = find_footer(self.file)
        self.file.seek(pos, os.SEEK_SET)

        header = json.loads(header)
        self.start = header['start']

        # TODO: Do we need the footer for something?
        try:
            footer = json.loads(footer)
            self.stop = footer['stop']
        except ValueError:
            pass

    def __iter__(self):
        return self

    def read_safe(self, size=None):
        """
        We currently close our fbs files by killing them, so sometimes they end
        up with bad data at the end. Close our reader if we expect `size` bytes
        and get fewer.

        This is a hack and should be removed when we cleanly close our
        connections in fbs_writer.

        https://github.com/openai/gym-vnc-envs/issues/41
        """
        bytes = self.file.read(size)
        if len(bytes) != size:
            # We unexpectedly got to the end of the file
            self.close()
            raise StopIteration
        return bytes

    def next(self):
        length_str = self.read_safe(4)
        if length_str == '':
            # Indicates a file with no trailer
            self.close()
            raise StopIteration
        (length,) = struct.unpack('!I', length_str)

        if length == 0:
            # Reached the trailer!
            self.close()
            raise StopIteration()

        data = self.read_safe(length)
        timestamp_str = self.read_safe(4)
        (timestamp,) = struct.unpack('!I', timestamp_str)

        return data, self.start + timestamp/1000.

    def close(self):
        self.file.close()
