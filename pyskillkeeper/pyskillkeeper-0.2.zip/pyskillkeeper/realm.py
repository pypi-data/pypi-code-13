from collections import namedtuple
from pyskillkeeper.matches import Match, Tournament

Player = namedtuple('Player', ['name', 'team', 'invisible', 'characters'])
Settings = namedtuple('Settings', ['multiplier', 'min_matches', 'decay', 'decay_value'])


def load_realm(file_path):
    return Realm.from_xml(open(file_path, 'rb').read())


class Realm(object):

    def __init__(self, players, matches, settings):
        self.players = players
        self.matches = matches
        self.settings = settings
        self.tournaments = {}
        self.create_tournaments(matches)

    def create_tournaments(self, matches):
        for match in matches:
            if match.tournament not in self.tournaments:
                self.tournaments[match.tournament] = Tournament(match.tournament)
            self.tournaments[match.tournament].matches.append(match)

    @classmethod
    def from_xml(cls, xml_file):
        """
        Creates a Realm object from a SkillKeeper XML file.

        :param xml_file Either an XML file object or XML string data.
        """
        if hasattr(xml_file, 'read'):
            xml_file = xml_file.read()
        import xml.etree.ElementTree as ET
        et = ET.parse(xml_file)
        settings, players, matches = et.getroot().getchildren()
        return Realm([Player(name=player.get('Name'), team=player.get('Team'),
                             invisible=player.get('Invisible'), characters=player.get('Characters'))
                      for player in players],
                     [Match(id=match.get('ID'), time=match.get('Timestamp'),
                            order=int(match.get('Order')), tournament=match.get('Description'),
                            player1=match.get('Player1'), player2=match.get('Player2'),
                            winner=int(match.get('Winner'))) for match in matches],
                     Settings(multiplier=int(settings.get('Multiplier')),
                              min_matches=int(settings.get('MinMatches')),
                              decay=int(settings.get('Decay')),
                              decay_value=int(settings.get('DecayValue'))))
