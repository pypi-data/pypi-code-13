# -*- coding: utf-8 -*-

from __future__ import print_function

b64 = 'YWJjw6bDuMOlw4bDmMOFCg=='
print(b64.decode('base64'))

u1 = u'\u00e6\u00f8\u00e5\u00c6\u00d8\u00c5'
u1 = u'æøå'
print(type(u1), u1)
u1encoded = u1.encode('utf-8').encode('base64')
print(type(u1encoded), "'" + u1encoded + "'")
u2 = u1encoded.decode('base64').decode('utf-8')
print(type(u2), u2)
