#unicoding utf-8
class account:
    def __init__(self, name, num, year):
        self.name = name
        self.num = num
        self.year = year
    def nameReturn(self):
        return self.name
    def plusNum(self, val):
        self.num += val