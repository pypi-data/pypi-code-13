from binascii import hexlify
from collections import namedtuple
import socket
import struct


ARPPacket = namedtuple('ARPPacket', [
    'eth_dest_mac',
    'eth_src_mac',
    'eth_type',
    'arp_hw_type',
    'arp_proto_type',
    'arp_hw_size',
    'arp_proto_size',
    'arp_opcode',
    'arp_src_mac',
    'arp_src_ip',
    'arp_dest_mac',
    'arp_dest_ip',
])


class ARPPacketSniffer(object):

    def __init__(self, on_arp_packet, quiet=False):
        """
        Takes a callback function to be called on arp packets.
        If you wish to get only necessary output printed, set quiet to True.
        """
        self.on_arp_packet = on_arp_packet
        self.quiet = quiet

    def loop_forever(self):
        """
        Sniffs for ARP packets and triggers the callback.

        Thank you for the ARP magic at http://goo.gl/3DQJtK, Rad Lexus!
        """
        raw_socket = socket.socket(
            socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003)
        )

        eth_src_macs = set()

        while True:
            bufsize = 2048
            frame, address = raw_socket.recvfrom(bufsize)

            mac_header = frame[0:14]
            eth_dest_mac, eth_src_mac, eth_type = map(
                hexlify,
                struct.unpack("!6s6s2s", mac_header)
            )

            arp_eth_type = "0806"
            if eth_type != arp_eth_type:
                continue

            arp_header = frame[14:42]
            arp_header_fields = struct.unpack("2s2s1s1s2s6s4s6s4s", arp_header)

            arp_packet = ARPPacket(
                eth_dest_mac=eth_dest_mac,
                eth_src_mac=eth_src_mac,
                eth_type=eth_type,
                arp_hw_type=hexlify(arp_header_fields[0]),
                arp_proto_type=hexlify(arp_header_fields[1]),
                arp_hw_size=hexlify(arp_header_fields[2]),
                arp_proto_size=hexlify(arp_header_fields[3]),
                arp_opcode=hexlify(arp_header_fields[4]),
                arp_src_mac=hexlify(arp_header_fields[5]),
                arp_src_ip=socket.inet_ntoa(arp_header_fields[6]),
                arp_dest_mac=hexlify(arp_header_fields[7]),
                arp_dest_ip=socket.inet_ntoa(arp_header_fields[8]),
            )

            if eth_src_mac not in eth_src_macs:
                eth_src_macs.add(eth_src_mac)
                if not self.quiet:
                    print(
                        "Discovered MAC address %s (IP: %s)" % (
                            eth_src_mac, arp_packet.arp_src_ip
                        )
                    )

            self.on_arp_packet(arp_packet)
