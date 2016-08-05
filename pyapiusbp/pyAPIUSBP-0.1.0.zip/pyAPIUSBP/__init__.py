__version__ = '0.1.0'

import pyAPIUSBP.DIO
import pyAPIUSBP.AIO

def dec2bitlist(val,fill=8):
    """
    Convert decimal value to a list of I/O status.
    See also :func:`~pyAPIUSBP.bitlist2dec`.
    
    Example:
    dec2bitlist(1,8) -> [1, 0, 0, 0, 0, 0, 0, 0]
    dec2bitlist(21,8) -> [1, 0, 1, 0, 1, 0, 0, 0]
    
    :param int val:
        Logical output bit number.
    :param int fill:
        Length of the returned list. Default value is 8.
    :return:
        List of I/O status.
    """
    binString = bin(val)
    bitlist = [1 if binString[i+2]=='1' else 0  for i in range(len(binString)-2)]
    bitlist.reverse()
    if len(bitlist)<fill:
        bitlist.extend([0 for i in range(fill-len(bitlist))])
    return bitlist

def bitlist2dec(bitlist):
    """
    Convert list of I/O status to decimal value.
    See also :func:`~pyAPIUSBP.dec2bitlist`.
    
    Example:
    pyAPIUSBP.bitlist2dec([1,0,0,0,0,0,0,0]) -> 1
    pyAPIUSBP.bitlist2dec([1,0,1,0,1,0,0,0]) -> 21

    :param int val:
        A list of I/O status.
    :return:
        Integer
    """
    val = 0
    for i in range(len(bitlist)):
        val += (2**i)*bitlist[i]
    return val

