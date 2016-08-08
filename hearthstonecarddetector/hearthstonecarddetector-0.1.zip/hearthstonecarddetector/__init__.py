from imagehash import ImageHash, phash

import json
import numpy
import os


class ErrorThresholdReachedException(Exception):
    pass


# thanks to https://github.com/JohannesBuchner/imagehash/issues/20
def _hex_to_hash(hexstr):
    """
    Convert a stored hash (hex, as retrieved from str(Imagehash))
    back to a Imagehash object.
    """
    l = []
    if len(hexstr) != 2*(16*16)/8:
        raise ValueError('The hex string has the wrong length')
    for i in range(0, int(16*16/8)):
        h = hexstr[i*2:i*2+2]
        v = int("0x" + h, 16)
        l.append([v & 2**i > 0 for i in range(8)])
    return ImageHash(numpy.array(l).reshape((16,16)))


def card_image_to_id(card_image, preferred_hash=phash, max_error=None):
    """
    given a PIL Image object, find the closest Hearthstone card match and return its card id.
    :param card_image: PIL Image object
    :param preferred_hash: one of imagehash's phash, dhash, whash, or average_hash
    :param max_error: percent error calculated by (diff(input, closest) / diff(input, furthest)). if exceeded,
        raise ErrorThresholdReachedException
    :return: card id of closest match found
    """
    card_image_hash = preferred_hash(card_image, 16)

    sort = sorted(db["cards"], key=lambda x: card_image_hash - _hex_to_hash(x[preferred_hash.__name__]))

    if max_error is not None:
        percent_error = (abs(card_image_hash - _hex_to_hash(sort[0][preferred_hash.__name__])) /
                         (abs(card_image_hash - _hex_to_hash(sort[-1][preferred_hash.__name__]))))

        if percent_error > max_error:
            raise ErrorThresholdReachedException

    return sort[0]['card_id']

"""
when the module is loaded, load our database file into memory. the database is essential because it contains the
different hash values for each card.
"""
try:
    with open(os.path.join(os.path.dirname(__file__), 'db.json'), "r") as handle:
        db = json.load(handle)
        # print("HearthstoneCardDetector: Loaded database file!")
except:
    print("HearthstoneCardDetector fatal error: Unable to load database file!")
    raise

