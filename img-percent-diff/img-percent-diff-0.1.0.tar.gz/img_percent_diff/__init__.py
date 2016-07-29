# Import built-in packages
import sys
import os

# Import third-party packages
from PIL import Image


def img_percent_diff(image1, image2):
    """
    Calculates the percent area where two images differ

    This code was found on [Rosetta Code](
    https://rosettacode.org/wiki/Percentage_difference_between_images#Python)

    ### Parameters

    - image1 (*string*): First image to compare
    - image2 (*string*): Second image to compare

    ### Returns

    - Percent area where images differ
    """
    i1 = Image.open(image1)
    i2 = Image.open(image2)
    assert i1.mode == i2.mode, "Different kinds of images."
    assert i1.size == i2.size, "Different sizes."

    pairs = zip(i1.getdata(), i2.getdata())
    if len(i1.getbands()) == 1:
        # for gray-scale jpegs
        dif = sum(abs(p1 - p2) for p1, p2 in pairs)
    else:
        dif = sum(abs(c1 - c2) for p1, p2 in pairs for c1, c2 in zip(p1, p2))

    ncomponents = i1.size[0] * i1.size[1] * 3

    return (dif / 255.0 * 100) / ncomponents


def main(argv=None):
    if len(sys.argv) - 1 != 2:
        script_name = os.path.basename(sys.argv[0])
        print('Usage: {} <IMAGE1> <IMAGE2>'.format(script_name))
        sys.exit(1)
    else:
        return img_percent_diff(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main(sys.argv[1:])
