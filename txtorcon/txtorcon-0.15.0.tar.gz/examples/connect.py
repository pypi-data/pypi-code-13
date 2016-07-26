#!/usr/bin/env python

from __future__ import print_function
from twisted.internet.task import react
from twisted.internet.defer import inlineCallbacks
from twisted.internet.endpoints import TCP4ClientEndpoint
import txtorcon

@inlineCallbacks
def main(reactor):
    #ep = TCP4ClientEndpoint(reactor, "localhost", 9251)
    ep = TCP4ClientEndpoint(reactor, "localhost", 9051)
    # XXX nicer/better thing than "build_tor_connection" switching
    # between returning two different objects depending on kwarg?
    tor_protocol = yield txtorcon.connect(ep)
    print(
        "Connected to Tor {version}".format(
            version=tor_protocol.version,
        )
    )
    state = yield txtorcon.TorState.from_protocol(tor_protocol)
    print("Tor state created. Circuits:")
    for circuit in state.circuits.values():
        print("  {circuit.id}: {circuit.path}".format(circuit=circuit))


react(main)
