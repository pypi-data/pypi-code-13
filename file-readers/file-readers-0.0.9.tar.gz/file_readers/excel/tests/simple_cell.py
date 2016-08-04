
class SimpleCell(object):
    # TODO: Figure out how to use openpyxl Cell objects instead. Could not create a Cell object with a value..
    def __init__(self, coordinate, value):
        self.coordinate = coordinate
        self.value = value
