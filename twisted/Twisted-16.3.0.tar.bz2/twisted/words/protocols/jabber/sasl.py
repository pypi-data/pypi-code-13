# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
XMPP-specific SASL profile.
"""

from base64 import b64decode, b64encode
import re
from twisted.internet import defer
from twisted.words.protocols.jabber import sasl_mechanisms, xmlstream
from twisted.words.xish import domish

NS_XMPP_SASL = 'urn:ietf:params:xml:ns:xmpp-sasl'

def get_mechanisms(xs):
    """
    Parse the SASL feature to extract the available mechanism names.
    """
    mechanisms = []
    for element in xs.features[(NS_XMPP_SASL, 'mechanisms')].elements():
        if element.name == 'mechanism':
            mechanisms.append(str(element))

    return mechanisms


class SASLError(Exception):
    """
    SASL base exception.
    """


class SASLNoAcceptableMechanism(SASLError):
    """
    The server did not present an acceptable SASL mechanism.
    """


class SASLAuthError(SASLError):
    """
    SASL Authentication failed.
    """
    def __init__(self, condition=None):
        self.condition = condition


    def __str__(self):
        return "SASLAuthError with condition %r" % self.condition


class SASLIncorrectEncodingError(SASLError):
    """
    SASL base64 encoding was incorrect.

    RFC 3920 specifies that any characters not in the base64 alphabet
    and padding characters present elsewhere than at the end of the string
    MUST be rejected. See also L{fromBase64}.

    This exception is raised whenever the encoded string does not adhere
    to these additional restrictions or when the decoding itself fails.

    The recommended behaviour for so-called receiving entities (like servers in
    client-to-server connections, see RFC 3920 for terminology) is to fail the
    SASL negotiation with a C{'incorrect-encoding'} condition. For initiating
    entities, one should assume the receiving entity to be either buggy or
    malevolent. The stream should be terminated and reconnecting is not
    advised.
    """

base64Pattern = re.compile("^[0-9A-Za-z+/]*[0-9A-Za-z+/=]{,2}$")

def fromBase64(s):
    """
    Decode base64 encoded string.

    This helper performs regular decoding of a base64 encoded string, but also
    rejects any characters that are not in the base64 alphabet and padding
    occurring elsewhere from the last or last two characters, as specified in
    section 14.9 of RFC 3920. This safeguards against various attack vectors
    among which the creation of a covert channel that "leaks" information.
    """

    if base64Pattern.match(s) is None:
        raise SASLIncorrectEncodingError()

    try:
        return b64decode(s)
    except Exception as e:
        raise SASLIncorrectEncodingError(str(e))



class SASLInitiatingInitializer(xmlstream.BaseFeatureInitiatingInitializer):
    """
    Stream initializer that performs SASL authentication.

    The supported mechanisms by this initializer are C{DIGEST-MD5}, C{PLAIN}
    and C{ANONYMOUS}. The C{ANONYMOUS} SASL mechanism is used when the JID, set
    on the authenticator, does not have a localpart (username), requesting an
    anonymous session where the username is generated by the server.
    Otherwise, C{DIGEST-MD5} and C{PLAIN} are attempted, in that order.
    """

    feature = (NS_XMPP_SASL, 'mechanisms')
    _deferred = None

    def setMechanism(self):
        """
        Select and setup authentication mechanism.

        Uses the authenticator's C{jid} and C{password} attribute for the
        authentication credentials. If no supported SASL mechanisms are
        advertized by the receiving party, a failing deferred is returned with
        a L{SASLNoAcceptableMechanism} exception.
        """

        jid = self.xmlstream.authenticator.jid
        password = self.xmlstream.authenticator.password

        mechanisms = get_mechanisms(self.xmlstream)
        if jid.user is not None:
            if 'DIGEST-MD5' in mechanisms:
                self.mechanism = sasl_mechanisms.DigestMD5('xmpp', jid.host, None,
                                                           jid.user, password)
            elif 'PLAIN' in mechanisms:
                self.mechanism = sasl_mechanisms.Plain(None, jid.user, password)
            else:
                raise SASLNoAcceptableMechanism()
        else:
            if 'ANONYMOUS' in mechanisms:
                self.mechanism = sasl_mechanisms.Anonymous()
            else:
                raise SASLNoAcceptableMechanism()


    def start(self):
        """
        Start SASL authentication exchange.
        """

        self.setMechanism()
        self._deferred = defer.Deferred()
        self.xmlstream.addObserver('/challenge', self.onChallenge)
        self.xmlstream.addOnetimeObserver('/success', self.onSuccess)
        self.xmlstream.addOnetimeObserver('/failure', self.onFailure)
        self.sendAuth(self.mechanism.getInitialResponse())
        return self._deferred


    def sendAuth(self, data=None):
        """
        Initiate authentication protocol exchange.

        If an initial client response is given in C{data}, it will be
        sent along.

        @param data: initial client response.
        @type data: C{str} or C{None}.
        """

        auth = domish.Element((NS_XMPP_SASL, 'auth'))
        auth['mechanism'] = self.mechanism.name
        if data is not None:
            auth.addContent(b64encode(data) or '=')
        self.xmlstream.send(auth)


    def sendResponse(self, data=''):
        """
        Send response to a challenge.

        @param data: client response.
        @type data: C{str}.
        """

        response = domish.Element((NS_XMPP_SASL, 'response'))
        if data:
            response.addContent(b64encode(data))
        self.xmlstream.send(response)


    def onChallenge(self, element):
        """
        Parse challenge and send response from the mechanism.

        @param element: the challenge protocol element.
        @type element: L{domish.Element}.
        """

        try:
            challenge = fromBase64(str(element))
        except SASLIncorrectEncodingError:
            self._deferred.errback()
        else:
            self.sendResponse(self.mechanism.getResponse(challenge))


    def onSuccess(self, success):
        """
        Clean up observers, reset the XML stream and send a new header.

        @param success: the success protocol element. For now unused, but
                        could hold additional data.
        @type success: L{domish.Element}
        """

        self.xmlstream.removeObserver('/challenge', self.onChallenge)
        self.xmlstream.removeObserver('/failure', self.onFailure)
        self.xmlstream.reset()
        self.xmlstream.sendHeader()
        self._deferred.callback(xmlstream.Reset)


    def onFailure(self, failure):
        """
        Clean up observers, parse the failure and errback the deferred.

        @param failure: the failure protocol element. Holds details on
                        the error condition.
        @type failure: L{domish.Element}
        """

        self.xmlstream.removeObserver('/challenge', self.onChallenge)
        self.xmlstream.removeObserver('/success', self.onSuccess)
        try:
            condition = failure.firstChildElement().name
        except AttributeError:
            condition = None
        self._deferred.errback(SASLAuthError(condition))
