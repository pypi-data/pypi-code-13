from collections import namedtuple
import socket
import struct
import binascii


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

    def __init__(self, on_arp_packet):
        """
        Takes a callback function to be called on arp packets.
        """
        self.on_arp_packet = on_arp_packet

    def loop_forever(self):
        """
        Sniffs for ARP packets and triggers the callback.

        Thank you for the ARP magic at http://goo.gl/3DQJtK, Rad Lexus!
        """
        raw_socket = socket.socket(
            socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003)
        )

        while True:
            packet = raw_socket.recvfrom(2048)

            ethernet_header = packet[0][0:14]
            ethernet_detailed = struct.unpack("!6s6s2s", ethernet_header)

            arp_header = packet[0][14:42]
            arp_detailed = struct.unpack("2s2s1s1s2s6s4s6s4s", arp_header)

            # skip non-ARP packets
            ethertype = ethernet_detailed[2]
            if ethertype != '\x08\x06':
                continue

            arp_packet = ARPPacket(
                eth_dest_mac=binascii.hexlify(ethernet_detailed[0]),
                eth_src_mac=binascii.hexlify(ethernet_detailed[1]),
                eth_type=binascii.hexlify(ethertype),
                arp_hw_type=binascii.hexlify(arp_detailed[0]),
                arp_proto_type=binascii.hexlify(arp_detailed[1]),
                arp_hw_size=binascii.hexlify(arp_detailed[2]),
                arp_proto_size=binascii.hexlify(arp_detailed[3]),
                arp_opcode=binascii.hexlify(arp_detailed[4]),
                arp_src_mac=binascii.hexlify(arp_detailed[5]),
                arp_src_ip=socket.inet_ntoa(arp_detailed[6]),
                arp_dest_mac=binascii.hexlify(arp_detailed[7]),
                arp_dest_ip=socket.inet_ntoa(arp_detailed[8])
            )
            self.on_arp_packet(arp_packet)
