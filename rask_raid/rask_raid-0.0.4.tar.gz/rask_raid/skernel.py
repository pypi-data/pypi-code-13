from rask.base import Base

__all__ = ['SKernel']

class SKernel(Base):
    @property
    def connection(self):
        try:
            assert self.__connection
        except (AssertionError,AttributeError):
            self.__connection = {}
        except:
            raise
        return self.__connection

    def connection_add(self,_):
        self.connection[_.uuid] = _
        return True

    def connection_del(self,_):
        try:
            assert self.connection[_]
        except (AssertionError,KeyError):
            pass
        except:
            raise
        else:
            del self.connection[_]
        return True
