class PairList(list, object):
  def __init__(self, size):
    # super(PairList, self).__init__([[0, 0]] * size)
    super(PairList, self).__init__((0, 0) for _ in range(size))
    self.front = 0

  def pull_front(self):
    i = self.front
    self.front = (self.front + 1) % len(self)
    return self[i]

  def front(self):
    return self[self.front]

  def __lt__(self, nt):
    self[self.front] = nt

d = PairList(2)

z, _ = d.pull_front()
print z
d < (1, 2)
print d

ot = d.pull_front()
print ot
d < (3, 4)
print d
