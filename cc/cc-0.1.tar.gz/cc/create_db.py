import datetime
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base


db = create_engine('sqlite:///words.db')
Base = declarative_base()


class Record(Base):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True)
    word = Column(String, unique=True)
    means = Column(String(256))
    number = Column(Integer, default=1)
    uptime = Column(DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return str(self.id) + "\t" + self.word + "\t" + str(self.number)


Base.metadata.create_all(db)
