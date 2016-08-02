#!/usr/bin/env python

import hypchat
import socket
import os
import sys
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("roomid", type=int)
parser.add_argument("message", type=str)

hostname = (socket.gethostname())
args = parser.parse_args()

try:
    token= os.environ['HIPCHAT_TOKEN']
except KeyError:
    print ("your HIPCHAT_TOKEN env variable does not exists, exiting...")
    sys.exit(-1)

rid = args.roomid
message = args.message
hc = hypchat.HypChat(token)
hc.get_room(rid)
room = hc.get_room(rid)
room.message(message)
