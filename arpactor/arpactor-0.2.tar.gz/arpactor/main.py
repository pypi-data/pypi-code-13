from importlib import import_module
from optparse import OptionParser
import os
import pkgutil
import sys

from actor import Actor
from arp import ARPPacketSniffer


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARPACTOR_ACTORS_PATH = os.getenv('ARPACTOR_ACTORS_PATH',
                                 os.path.sep.join([BASE_DIR, 'actors']))


def on_arp_packet(arp_packet):
    """
    Triggers all Actors that got registered for the MAC address.
    """
    [AClass().act() for AClass in Actor.get_for_mac(arp_packet.arp_src_mac)]


def import_actors(actors_path):
    """
    Imports all Actor subclasses. That's important for the registry.
    """
    if actors_path not in sys.path:
        sys.path.append(actors_path)

    [import_module(name) for _, name, _ in pkgutil.iter_modules([actors_path])]


def main(actors_path, quiet=False):
    import_actors(actors_path=actors_path)

    print("Arpactor started sniffing [Active actors at %s] ..." % actors_path)

    sniffer = ARPPacketSniffer(on_arp_packet, quiet=quiet)
    sniffer.loop_forever()


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-a", "--actors_path", dest="actors_path",
                      help="the path where the actors are located")
    parser.add_option("-q", "--quiet", action="store_true", dest="quiet",
                      default=False, help="print out only necessary output")

    (options, args) = parser.parse_args()
    actors_path = options.actors_path or \
        os.getenv('ARPACTOR_ACTORS_PATH') or \
        ARPACTOR_ACTORS_PATH

    main(actors_path=actors_path, quiet=options.quiet)
