# Copyright (C) Ivo Slanina <ivo.slanina@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""!
Module with data containers.
"""

class DataIdentifier:
    """!
    Wrapper object to convert broker and topic into uniquie identification key
    """

    ## @var broker
    # Broker object.

    ## @var topic
    # Topic object.

    def __init__(self, broker, topic):
        """!
        Initiate DataIdentifier object.

        @param broker Broker object.
        @param topic Topic object.
        """
        self.broker = broker
        self.topic = topic

    def __hash__(self):
        """!
        Calculate hash of DataIdentifier object.

        @return Hash.
        """
        return hash((self.broker, self.topic))

    def __str__(self):
        """!
        Convert object to string.

        @return String.
        """
        return "{}: {}".format(self.broker, self.topic)

    def __repr__(self):
        """!
        Convert object to representation string.

        @return representation string.
        """
        return "<{}>".format(self.__str__())

    def __eq__(self, other):
        """!
        Check if DataIdentifier object is equal to another.

        @param other Other object.
        @return True if other object is instance of DataIdentifier and contains same values, False otherwise.
        """
        if not isinstance(other, self.__class__):
            return False
        return self.broker == other.broker and self.topic == other.topic
