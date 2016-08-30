import uuid

from gym_vnc.vncdriver.vendor import pydes

# Password is padded with nulls to 0 bytes
PASSWORD = 'openai\0\0'

class RFBDes(pydes.des):
    def setKey(self, key):
        newkey = []
        for ki in range(len(key)):
            bsrc = ord(key[ki])
            btgt = 0
            for i in range(8):
                if bsrc & (1 << i):
                    btgt = btgt | (1 << 7-i)
            newkey.append(chr(btgt))
        super(RFBDes, self).setKey(newkey)

def challenge():
    length = 16
    buf = []
    while len(buf) < length:
        entropy = uuid.uuid4().bytes
        bytes = [c for c in entropy]
        buf += bytes
    return ''.join(buf[:length])

def challenge_response(challenge, password=PASSWORD):
    des = RFBDes(password)
    return des.encrypt(challenge)
