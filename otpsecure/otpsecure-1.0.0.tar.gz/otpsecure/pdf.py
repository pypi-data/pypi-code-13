from otpsecure.base import Base

class Pdf(Base):
  def __init__(self):
    self.filename		= None
    self.content		= None