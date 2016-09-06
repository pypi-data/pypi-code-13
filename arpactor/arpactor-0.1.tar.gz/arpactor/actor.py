class ActorRegistry(type):
    """
    A registry for Actors.
    """
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, "actors"):
            cls.actors = {}
        else:  # Register subclasses
            mac = attrs.get("MAC", None)
            if mac is not None:
                cls.register_for_mac(cls, mac)

    def register_for_mac(self, cls, mac):
        """
        Register an Actor subclass for a MAC address.
        """
        actors = self.get_for_mac(mac)
        actors.append(cls)
        self.actors[mac] = actors
        return actors

    def get_for_mac(self, mac):
        """
        Returns a list of Actor subclasses that got registered for the given
        MAC address.
        """
        return self.actors.get(mac, [])


class Actor(object):
    """
    The base class for actors. Subclasses must override the MAC class constant
    and override the act method.
    """
    MAC = None  # The MAC address that the Actor should respond to.

    __metaclass__ = ActorRegistry

    def act(self):
        """
        Override this on subclasses.
        """
        raise NotImplementedError()
