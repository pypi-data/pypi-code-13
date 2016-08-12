import struct

HEADER_SIZE_IN_BYTES = 1024

## Code for setting up the IMM header was taken from some dev code 
#  Written By Tim Madden APS/XSD-DET.  Many thanks for working out these 
#  details.
imm_headformat = "ii32s16si16siiiiiiiiiiiiiddiiIiiI40sf40sf40sf40sf40sf40sf40sf40sf40sf40sfffiiifc295s84s12s"

imm_fieldnames = [
'mode',
'compression',
'date',
'prefix',
'number',
'suffix',
'monitor',
'shutter',
'row_beg',
'row_end',
'col_beg',
'col_end',
'row_bin',
'col_bin',
'rows',
'cols',
'bytes',
'kinetics',
'kinwinsize',
'elapsed',
'preset',
'topup',
'inject',
'dlen',
'roi_number',
'buffer_number',
'systick',
'pv1',
'pv1VAL',
'pv2',
'pv2VAL',
'pv3',
'pv3VAL',
'pv4',
'pv4VAL',
'pv5',
'pv5VAL',
'pv6',
'pv6VAL',
'pv7',
'pv7VAL',
'pv8',
'pv8VAL',
'pv9',
'pv9VAL',
'pv10',
'pv10VAL',
'imageserver',
'CPUspeed',
'immversion',
'corecotick',
'cameratype',
'threshhold',
'byte632',
'empty_space',
'ZZZZ',
'FFFF'

]

def readHeader(fp, offset=0):
    fp.seek(offset)
    bindata = fp.read(1024)
    if bindata=='':
        return('eof')

    imm_headerdat = struct.unpack(imm_headformat,bindata)
    imm_header ={}
    for k in range(len(imm_headerdat)):
        imm_header[imm_fieldnames[k]]=imm_headerdat[k]
    return(imm_header)

def offsetToNextHeader(header, offsetToThisHeader):
    offset = -1
    compressed = isCompressed(header)
    
    bytesPerPixel = header['bytes']
    dataLength = header['dlen']
    if not compressed:
        offset = offsetToThisHeader + 1024 + dataLength*bytesPerPixel
    else:
        offset = offsetToThisHeader + 1024 + dataLength*(4+bytesPerPixel)
    return offset

def isCompressed(header):
    if header['compression'] == 6:
        return True
    else:
        return False
    
def getNumberOfImages(fp):
    header = readHeader(fp, offset=0)
    numImages = 1
    offsetToNext =offsetToNextHeader(header, 0)
    while readHeader(fp, offset=offsetToNext) != 'eof':
        offsetToThisHeader = offsetToNext
        numImages += 1
        offsetToNext = \
            offsetToNextHeader(header, offsetToThisHeader)
    return numImages
