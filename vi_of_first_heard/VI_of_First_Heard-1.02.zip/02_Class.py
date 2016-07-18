class Athlete:
    def __init__(self,value = ''):
        self.thing = value
    def big(self):
        return len(self.thing)
z = Athlete()
print(z.big())
