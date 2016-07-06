# -*- test-case-name: twisted.conch.test.test_keys -*-
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
Data used by test_keys as well as others.
"""

from __future__ import absolute_import, division

from base64 import decodestring

from twisted.python.compat import long

RSAData = {
    'n': long('106248668575524741116943830949539894737212779118943280948138'
              '20729711061576321820845393835692814935201176341295575504152775'
              '16685881326038852354459895734875625093273594925884531272867425'
              '864910490065695876046999646807138717162833156501'),
    'e': long(35),
    'd': long('667848773903298372735075508825679338348194611604786337388297'
              '30301040958479737159599618395783408164121679859572188879144827'
              '13602371850869127033494910375212470664166001439410214474266799'
              '85974425203903884190893469297150446322896587555'),
    'q': long('3395694744258061291019136154000709371890447462086362702627'
              '9704149412726577280741108645721676968699696898960891593323'),
    'p': long('3128922844292337321766351031842562691837301298995834258844'
              '4720539204069737532863831050930719431498338835415515173887'),
    'u': long('2777403202132551568802514199893235993376771442611051821485'
              '0278129927603609294283482712900532542110958095343012272938')
}

DSAData = {
    'g': long("10253261326864117157640690761723586967382334319435778695"
              "29171533815411392477819921538350732400350395446211982054"
              "96512489289702949127531056893725702005035043292195216541"
              "11525058911428414042792836395195432445511200566318251789"
              "10575695836669396181746841141924498545494149998282951407"
              "18645344764026044855941864175"),
    'p': long("10292031726231756443208850082191198787792966516790381991"
              "77502076899763751166291092085666022362525614129374702633"
              "26262930887668422949051881895212412718444016917144560705"
              "45675251775747156453237145919794089496168502517202869160"
              "78674893099371444940800865897607102159386345313384716752"
              "18590012064772045092956919481"),
    'q': long(1393384845225358996250882900535419012502712821577),
    'x': long(1220877188542930584999385210465204342686893855021),
    'y': long("14604423062661947579790240720337570315008549983452208015"
              "39426429789435409684914513123700756086453120500041882809"
              "10283610277194188071619191739512379408443695946763554493"
              "86398594314468629823767964702559709430618263927529765769"
              "10270265745700231533660131769648708944711006508965764877"
              "684264272082256183140297951")
}

publicRSA_openssh = (b"ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAGEArzJx8OYOnJmzf4tfBE"
b"vLi8DVPrJ3/c9k2I/Az64fxjHf9imyRJbixtQhlH9lfNjUIx+4LmrJH5QNRsFporcHDKOTwTTYL"
b"h5KmRpslkYHRivcJSkbh/C+BR3utDS555mV comment")

privateRSA_openssh = b"""-----BEGIN RSA PRIVATE KEY-----
MIIByAIBAAJhAK8ycfDmDpyZs3+LXwRLy4vA1T6yd/3PZNiPwM+uH8Yx3/YpskSW
4sbUIZR/ZXzY1CMfuC5qyR+UDUbBaaK3Bwyjk8E02C4eSpkabJZGB0Yr3CUpG4fw
vgUd7rQ0ueeZlQIBIwJgbh+1VZfr7WftK5lu7MHtqE1S1vPWZQYE3+VUn8yJADyb
Z4fsZaCrzW9lkIqXkE3GIY+ojdhZhkO1gbG0118sIgphwSWKRxK0mvh6ERxKqIt1
xJEJO74EykXZV4oNJ8sjAjEA3J9r2ZghVhGN6V8DnQrTk24Td0E8hU8AcP0FVP+8
PQm/g/aXf2QQkQT+omdHVEJrAjEAy0pL0EBH6EVS98evDCBtQw22OZT52qXlAwZ2
gyTriKFVoqjeEjt3SZKKqXHSApP/AjBLpF99zcJJZRq2abgYlf9lv1chkrWqDHUu
DZttmYJeEfiFBBavVYIF1dOlZT0G8jMCMBc7sOSZodFnAiryP+Qg9otSBjJ3bQML
pSTqy7c3a2AScC/YyOwkDaICHnnD3XyjMwIxALRzl0tQEKMXs6hH8ToUdlLROCrP
EhQ0wahUTCk1gKA4uPD6TMTChavbh4K63OvbKg==
-----END RSA PRIVATE KEY-----"""

# Some versions of OpenSSH generate these (slightly different keys)
privateRSA_openssh_alternate = b"""-----BEGIN RSA PRIVATE KEY-----
MIIBzjCCAcgCAQACYQCvMnHw5g6cmbN/i18ES8uLwNU+snf9z2TYj8DPrh/GMd/2
KbJEluLG1CGUf2V82NQjH7guaskflA1GwWmitwcMo5PBNNguHkqZGmyWRgdGK9wl
KRuH8L4FHe60NLnnmZUCASMCYG4ftVWX6+1n7SuZbuzB7ahNUtbz1mUGBN/lVJ/M
iQA8m2eH7GWgq81vZZCKl5BNxiGPqI3YWYZDtYGxtNdfLCIKYcElikcStJr4ehEc
SqiLdcSRCTu+BMpF2VeKDSfLIwIxANyfa9mYIVYRjelfA50K05NuE3dBPIVPAHD9
BVT/vD0Jv4P2l39kEJEE/qJnR1RCawIxAMtKS9BAR+hFUvfHrwwgbUMNtjmU+dql
5QMGdoMk64ihVaKo3hI7d0mSiqlx0gKT/wIwS6Rffc3CSWUatmm4GJX/Zb9XIZK1
qgx1Lg2bbZmCXhH4hQQWr1WCBdXTpWU9BvIzAjAXO7DkmaHRZwIq8j/kIPaLUgYy
d20DC6Uk6su3N2tgEnAv2MjsJA2iAh55w918ozMCMQC0c5dLUBCjF7OoR/E6FHZS
0TgqzxIUNMGoVEwpNYCgOLjw+kzEwoWr24eCutzr2yowAA==
------END RSA PRIVATE KEY------"""

# Encrypted with the passphrase 'encrypted'
privateRSA_openssh_encrypted = b"""-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: DES-EDE3-CBC,FFFFFFFFFFFFFFFF

30qUR7DYY/rpVJu159paRM1mUqt/IMibfEMTKWSjNhCVD21hskftZCJROw/WgIFt
ncusHpJMkjgwEpho0KyKilcC7zxjpunTex24Meb5pCdXCrYft8AyUkRdq3dugMqT
4nuWuWxziluBhKQ2M9tPGcEOeulU4vVjceZt2pZhZQVBf08o3XUv5/7RYd24M9md
WIo+5zdj2YQkI6xMFTP954O/X32ME1KQt98wgNEy6mxhItbvf00mH3woALwEKP3v
PSMxxtx3VKeDKd9YTOm1giKkXZUf91vZWs0378tUBrU4U5qJxgryTjvvVKOtofj6
4qQy6+r6M6wtwVlXBgeRm2gBPvL3nv6MsROp3E6ztBd/e7A8fSec+UTq3ko/EbGP
0QG+IG5tg8FsdITxQ9WAIITZL3Rc6hA5Ymx1VNhySp3iSiso8Jof27lku4pyuvRV
ko/B3N2H7LnQrGV0GyrjeYocW/qZh/PCsY48JBFhlNQexn2mn44AJW3y5xgbhvKA
3mrmMD1hD17ZvZxi4fPHjbuAyM1vFqhQx63eT9ijbwJ91svKJl5O5MIv41mCRonm
hxvOXw8S0mjSasyofptzzQCtXxFLQigXbpQBltII+Ys=
-----END RSA PRIVATE KEY-----"""

# Encrypted with the passphrase 'testxp'. NB: this key was generated by
# OpenSSH, so it doesn't use the same key data as the other keys here.
privateRSA_openssh_encrypted_aes = b"""-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,0673309A6ACCAB4B77DEE1C1E536AC26

4Ed/a9OgJWHJsne7yOGWeWMzHYKsxuP9w1v0aYcp+puS75wvhHLiUnNwxz0KDi6n
T3YkKLBsoCWS68ApR2J9yeQ6R+EyS+UQDrO9nwqo3DB5BT3Ggt8S1wE7vjNLQD0H
g/SJnlqwsECNhh8aAx+Ag0m3ZKOZiRD5mCkcDQsZET7URSmFytDKOjhFn3u6ZFVB
sXrfpYc6TJtOQlHd/52JB6aAbjt6afSv955Z7enIi+5yEJ5y7oYQTaE5zrFMP7N5
9LbfJFlKXxEddy/DErRLxEjmC+t4svHesoJKc2jjjyNPiOoGGF3kJXea62vsjdNV
gMK5Eged3TBVIk2dv8rtJUvyFeCUtjQ1UJZIebScRR47KrbsIpCmU8I4/uHWm5hW
0mOwvdx1L/mqx/BHqVU9Dw2COhOdLbFxlFI92chkovkmNk4P48ziyVnpm7ME22sE
vfCMsyirdqB1mrL4CSM7FXONv+CgfBfeYVkYW8RfJac9U1L/O+JNn7yee414O/rS
hRYw4UdWnH6Gg6niklVKWNY0ZwUZC8zgm2iqy8YCYuneS37jC+OEKP+/s6HSKuqk
2bzcl3/TcZXNSM815hnFRpz0anuyAsvwPNRyvxG2/DacJHL1f6luV4B0o6W410yf
qXQx01DLo7nuyhJqoH3UGCyyXB+/QUs0mbG2PAEn3f5dVs31JMdbt+PrxURXXjKk
4cexpUcIpqqlfpIRe3RD0sDVbH4OXsGhi2kiTfPZu7mgyFxKopRbn1KwU1qKinfY
EU9O4PoTak/tPT+5jFNhaP+HrURoi/pU8EAUNSktl7xAkHYwkN/9Cm7DeBghgf3n
8+tyCGYDsB5utPD0/Xe9yx0Qhc/kMm4xIyQDyA937dk3mUvLC9vulnAP8I+Izim0
fZ182+D1bWwykoD0997mUHG/AUChWR01V1OLwRyPv2wUtiS8VNG76Y2aqKlgqP1P
V+IvIEqR4ERvSBVFzXNF8Y6j/sVxo8+aZw+d0L1Ns/R55deErGg3B8i/2EqGd3r+
0jps9BqFHHWW87n3VyEB3jWCMj8Vi2EJIfa/7pSaViFIQn8LiBLf+zxG5LTOToK5
xkN42fReDcqi3UNfKNGnv4dsplyTR2hyx65lsj4bRKDGLKOuB1y7iB0AGb0LtcAI
dcsVlcCeUquDXtqKvRnwfIMg+ZunyjqHBhj3qgRgbXbT6zjaSdNnih569aTg0Vup
VykzZ7+n/KVcGLmvX0NesdoI7TKbq4TnEIOynuG5Sf+2GpARO5bjcWKSZeN/Ybgk
gccf8Cqf6XWqiwlWd0B7BR3SymeHIaSymC45wmbgdstrbk7Ppa2Tp9AZku8M2Y7c
8mY9b+onK075/ypiwBm4L4GRNTFLnoNQJXx0OSl4FNRWsn6ztbD+jZhu8Seu10Jw
SEJVJ+gmTKdRLYORJKyqhDet6g7kAxs4EoJ25WsOnX5nNr00rit+NkMPA7xbJT+7
CfI51GQLw7pUPeO2WNt6yZO/YkzZrqvTj5FEwybkUyBv7L0gkqu9wjfDdUw0fVHE
xEm4DxjEoaIp8dW/JOzXQ2EF+WaSOgdYsw3Ac+rnnjnNptCdOEDGP6QBkt+oXj4P
-----END RSA PRIVATE KEY-----"""

publicRSA_lsh = (b"{KDEwOnB1YmxpYy1rZXkoMTQ6cnNhLXBrY3MxLXNoYTEoMTpuOTc6AK8yc"
b"fDmDpyZs3+LXwRLy4vA1T6yd/3PZNiPwM+uH8Yx3/YpskSW4sbUIZR/ZXzY1CMfuC5qyR+UDUbB"
b"aaK3Bwyjk8E02C4eSpkabJZGB0Yr3CUpG4fwvgUd7rQ0ueeZlSkoMTplMTojKSkp}")

privateRSA_lsh = (b"(11:private-key(9:rsa-pkcs1(1:n97:\x00\xaf2q\xf0\xe6\x0e"
b"\x9c\x99\xb3\x7f\x8b_\x04K\xcb\x8b\xc0\xd5>\xb2w\xfd\xcfd\xd8\x8f\xc0\xcf"
b"\xae\x1f\xc61\xdf\xf6)\xb2D\x96\xe2\xc6\xd4!\x94\x7fe|\xd8\xd4#\x1f\xb8.j"
b"\xc9\x1f\x94\rF\xc1i\xa2\xb7\x07\x0c\xa3\x93\xc14\xd8.\x1eJ\x99\x1al\x96F"
b"\x07F+\xdc%)\x1b\x87\xf0\xbe\x05\x1d\xee\xb44\xb9\xe7\x99\x95)(1:e1:#)(1:d9"
b"6:n\x1f\xb5U\x97\xeb\xedg\xed+\x99n\xec\xc1\xed\xa8MR\xd6\xf3\xd6e\x06\x04"
b"\xdf\xe5T\x9f\xcc\x89\x00<\x9bg\x87\xece\xa0\xab\xcdoe\x90\x8a\x97\x90M\xc6"
b'!\x8f\xa8\x8d\xd8Y\x86C\xb5\x81\xb1\xb4\xd7_,"\na\xc1%\x8aG\x12\xb4\x9a\xf8'
b"z\x11\x1cJ\xa8\x8bu\xc4\x91\t;\xbe\x04\xcaE\xd9W\x8a\r\'\xcb#)(1:p49:\x00"
b"\xdc\x9fk\xd9\x98!V\x11\x8d\xe9_\x03\x9d\n\xd3\x93n\x13wA<\x85O\x00p\xfd"
b"\x05T\xff\xbc=\t\xbf\x83\xf6\x97\x7fd\x10\x91\x04\xfe\xa2gGTBk)(1:q49:\x00"
b"\xcbJK\xd0@G\xe8ER\xf7\xc7\xaf\x0c mC\r\xb69\x94\xf9\xda\xa5\xe5\x03\x06v"
b"\x83$\xeb\x88\xa1U\xa2\xa8\xde\x12;wI\x92\x8a\xa9q\xd2\x02\x93\xff)(1:a48:K"
b"\xa4_}\xcd\xc2Ie\x1a\xb6i\xb8\x18\x95\xffe\xbfW!\x92\xb5\xaa\x0cu.\r\x9bm"
b"\x99\x82^\x11\xf8\x85\x04\x16\xafU\x82\x05\xd5\xd3\xa5e=\x06\xf23)(1:b48:"
b"\x17;\xb0\xe4\x99\xa1\xd1g\x02*\xf2?\xe4 \xf6\x8bR\x062wm\x03\x0b\xa5$\xea"
b"\xcb\xb77k`\x12p/\xd8\xc8\xec$\r\xa2\x02\x1ey\xc3\xdd|\xa33)(1:c49:\x00\xb4"
b"s\x97KP\x10\xa3\x17\xb3\xa8G\xf1:\x14vR\xd18*\xcf\x12\x144\xc1\xa8TL)5\x80"
b"\xa08\xb8\xf0\xfaL\xc4\xc2\x85\xab\xdb\x87\x82\xba\xdc\xeb\xdb*)))")

privateRSA_agentv3 = (b"\x00\x00\x00\x07ssh-rsa\x00\x00\x00\x01#\x00\x00\x00`"
b"n\x1f\xb5U\x97\xeb\xedg\xed+\x99n\xec\xc1\xed\xa8MR\xd6\xf3\xd6e\x06\x04"
b"\xdf\xe5T\x9f\xcc\x89\x00<\x9bg\x87\xece\xa0\xab\xcdoe\x90\x8a\x97\x90M\xc6"
b'!\x8f\xa8\x8d\xd8Y\x86C\xb5\x81\xb1\xb4\xd7_,"\na\xc1%\x8aG\x12\xb4\x9a\xf8'
b"z\x11\x1cJ\xa8\x8bu\xc4\x91\t;\xbe\x04\xcaE\xd9W\x8a\r\'\xcb#\x00\x00\x00a"
b"\x00\xaf2q\xf0\xe6\x0e\x9c\x99\xb3\x7f\x8b_\x04K\xcb\x8b\xc0\xd5>\xb2w\xfd"
b"\xcfd\xd8\x8f\xc0\xcf\xae\x1f\xc61\xdf\xf6)\xb2D\x96\xe2\xc6\xd4!\x94\x7fe|"
b"\xd8\xd4#\x1f\xb8.j\xc9\x1f\x94\rF\xc1i\xa2\xb7\x07\x0c\xa3\x93\xc14\xd8."
b"\x1eJ\x99\x1al\x96F\x07F+\xdc%)\x1b\x87\xf0\xbe\x05\x1d\xee\xb44\xb9\xe7"
b"\x99\x95\x00\x00\x001\x00\xb4s\x97KP\x10\xa3\x17\xb3\xa8G\xf1:\x14vR\xd18*"
b"\xcf\x12\x144\xc1\xa8TL)5\x80\xa08\xb8\xf0\xfaL\xc4\xc2\x85\xab\xdb\x87\x82"
b"\xba\xdc\xeb\xdb*\x00\x00\x001\x00\xcbJK\xd0@G\xe8ER\xf7\xc7\xaf\x0c mC\r"
b"\xb69\x94\xf9\xda\xa5\xe5\x03\x06v\x83$\xeb\x88\xa1U\xa2\xa8\xde\x12;wI\x92"
b"\x8a\xa9q\xd2\x02\x93\xff\x00\x00\x001\x00\xdc\x9fk\xd9\x98!V\x11\x8d\xe9_"
b"\x03\x9d\n\xd3\x93n\x13wA<\x85O\x00p\xfd\x05T\xff\xbc=\t\xbf\x83\xf6\x97"
b"\x7fd\x10\x91\x04\xfe\xa2gGTBk")

publicDSA_openssh = b"""\
ssh-dss AAAAB3NzaC1kc3MAAACBAJKQOsVERVDQIpANHH+JAAylo9\
LvFYmFFVMIuHFGlZpIL7sh3IMkqy+cssINM/lnHD3fmsAyLlUXZtt6PD9LgZRazsPOgptuH+Gu48G\
+yFuE8l0fVVUivos/MmYVJ66qT99htcZKatrTWZnpVW7gFABoqw+he2LZ0gkeU0+Sx9a5AAAAFQD0\
EYmTNaFJ8CS0+vFSF4nYcyEnSQAAAIEAkgLjxHJAE7qFWdTqf7EZngu7jAGmdB9k3YzMHe1ldMxEB\
7zNw5aOnxjhoYLtiHeoEcOk2XOyvnE+VfhIWwWAdOiKRTEZlmizkvhGbq0DCe2EPMXirjqWACI5nD\
ioQX1oEMonR8N3AEO5v9SfBqS2Q9R6OBr6lf04RvwpHZ0UGu8AAACAAhRpxGMIWEyaEh8YnjiazQT\
NEpklRZqeBGo1gotJggNmVaIQNIClGlLyCi359efEUuQcZ9SXxM59P+hecc/GU/GHakW5YWE4dP2G\
gdgMQWC7S6WFIXePGGXqNQDdWxlX8umhenvQqa1PnKrFRhDrJw8Z7GjdHxflsxCEmXPoLN8= \
comment\
"""

privateDSA_openssh = b"""\
-----BEGIN DSA PRIVATE KEY-----
MIIBvAIBAAKBgQCSkDrFREVQ0CKQDRx/iQAMpaPS7xWJhRVTCLhxRpWaSC+7IdyD
JKsvnLLCDTP5Zxw935rAMi5VF2bbejw/S4GUWs7DzoKbbh/hruPBvshbhPJdH1VV
Ir6LPzJmFSeuqk/fYbXGSmra01mZ6VVu4BQAaKsPoXti2dIJHlNPksfWuQIVAPQR
iZM1oUnwJLT68VIXidhzISdJAoGBAJIC48RyQBO6hVnU6n+xGZ4Lu4wBpnQfZN2M
zB3tZXTMRAe8zcOWjp8Y4aGC7Yh3qBHDpNlzsr5xPlX4SFsFgHToikUxGZZos5L4
Rm6tAwnthDzF4q46lgAiOZw4qEF9aBDKJ0fDdwBDub/UnwaktkPUejga+pX9OEb8
KR2dFBrvAoGAAhRpxGMIWEyaEh8YnjiazQTNEpklRZqeBGo1gotJggNmVaIQNICl
GlLyCi359efEUuQcZ9SXxM59P+hecc/GU/GHakW5YWE4dP2GgdgMQWC7S6WFIXeP
GGXqNQDdWxlX8umhenvQqa1PnKrFRhDrJw8Z7GjdHxflsxCEmXPoLN8CFQDV2gbL
czUdxCus0pfEP1bddaXRLQ==
-----END DSA PRIVATE KEY-----\
"""

publicDSA_lsh = decodestring(b"""\
e0tERXdPbkIxWW14cFl5MXJaWGtvTXpwa2MyRW9NVHB3TVRJNU9nQ1NrRHJGUkVWUTBDS1FEUngv
aVFBTXBhUFM3eFdKaFJWVENMaHhScFdhU0MrN0lkeURKS3N2bkxMQ0RUUDVaeHc5MzVyQU1pNVZG
MmJiZWp3L1M0R1VXczdEem9LYmJoL2hydVBCdnNoYmhQSmRIMVZWSXI2TFB6Sm1GU2V1cWsvZlli
WEdTbXJhMDFtWjZWVnU0QlFBYUtzUG9YdGkyZElKSGxOUGtzZld1U2tvTVRweE1qRTZBUFFSaVpN
MW9VbndKTFQ2OFZJWGlkaHpJU2RKS1NneE9tY3hNams2QUpJQzQ4UnlRQk82aFZuVTZuK3hHWjRM
dTR3QnBuUWZaTjJNekIzdFpYVE1SQWU4emNPV2pwOFk0YUdDN1loM3FCSERwTmx6c3I1eFBsWDRT
RnNGZ0hUb2lrVXhHWlpvczVMNFJtNnRBd250aER6RjRxNDZsZ0FpT1p3NHFFRjlhQkRLSjBmRGR3
QkR1Yi9Vbndha3RrUFVlamdhK3BYOU9FYjhLUjJkRkJydktTZ3hPbmt4TWpnNkFoUnB4R01JV0V5
YUVoOFluamlhelFUTkVwa2xSWnFlQkdvMWdvdEpnZ05tVmFJUU5JQ2xHbEx5Q2kzNTllZkVVdVFj
WjlTWHhNNTlQK2hlY2MvR1UvR0hha1c1WVdFNGRQMkdnZGdNUVdDN1M2V0ZJWGVQR0dYcU5RRGRX
eGxYOHVtaGVudlFxYTFQbktyRlJoRHJKdzhaN0dqZEh4ZmxzeENFbVhQb0xOOHBLU2s9fQ==
""")

privateDSA_lsh = decodestring(b"""\
KDExOnByaXZhdGUta2V5KDM6ZHNhKDE6cDEyOToAkpA6xURFUNAikA0cf4kADKWj0u8ViYUVUwi4
cUaVmkgvuyHcgySrL5yywg0z+WccPd+awDIuVRdm23o8P0uBlFrOw86Cm24f4a7jwb7IW4TyXR9V
VSK+iz8yZhUnrqpP32G1xkpq2tNZmelVbuAUAGirD6F7YtnSCR5TT5LH1rkpKDE6cTIxOgD0EYmT
NaFJ8CS0+vFSF4nYcyEnSSkoMTpnMTI5OgCSAuPEckATuoVZ1Op/sRmeC7uMAaZ0H2TdjMwd7WV0
zEQHvM3Dlo6fGOGhgu2Id6gRw6TZc7K+cT5V+EhbBYB06IpFMRmWaLOS+EZurQMJ7YQ8xeKuOpYA
IjmcOKhBfWgQyidHw3cAQ7m/1J8GpLZD1Ho4GvqV/ThG/CkdnRQa7ykoMTp5MTI4OgIUacRjCFhM
mhIfGJ44ms0EzRKZJUWangRqNYKLSYIDZlWiEDSApRpS8got+fXnxFLkHGfUl8TOfT/oXnHPxlPx
h2pFuWFhOHT9hoHYDEFgu0ulhSF3jxhl6jUA3VsZV/LpoXp70KmtT5yqxUYQ6ycPGexo3R8X5bMQ
hJlz6CzfKSgxOngyMToA1doGy3M1HcQrrNKXxD9W3XWl0S0pKSk=
""")

privateDSA_agentv3 = decodestring(b"""\
AAAAB3NzaC1kc3MAAACBAJKQOsVERVDQIpANHH+JAAylo9LvFYmFFVMIuHFGlZpIL7sh3IMkqy+c
ssINM/lnHD3fmsAyLlUXZtt6PD9LgZRazsPOgptuH+Gu48G+yFuE8l0fVVUivos/MmYVJ66qT99h
tcZKatrTWZnpVW7gFABoqw+he2LZ0gkeU0+Sx9a5AAAAFQD0EYmTNaFJ8CS0+vFSF4nYcyEnSQAA
AIEAkgLjxHJAE7qFWdTqf7EZngu7jAGmdB9k3YzMHe1ldMxEB7zNw5aOnxjhoYLtiHeoEcOk2XOy
vnE+VfhIWwWAdOiKRTEZlmizkvhGbq0DCe2EPMXirjqWACI5nDioQX1oEMonR8N3AEO5v9SfBqS2
Q9R6OBr6lf04RvwpHZ0UGu8AAACAAhRpxGMIWEyaEh8YnjiazQTNEpklRZqeBGo1gotJggNmVaIQ
NIClGlLyCi359efEUuQcZ9SXxM59P+hecc/GU/GHakW5YWE4dP2GgdgMQWC7S6WFIXePGGXqNQDd
WxlX8umhenvQqa1PnKrFRhDrJw8Z7GjdHxflsxCEmXPoLN8AAAAVANXaBstzNR3EK6zSl8Q/Vt11
pdEt
""")

__all__ = ['DSAData', 'RSAData', 'privateDSA_agentv3', 'privateDSA_lsh',
        'privateDSA_openssh', 'privateRSA_agentv3', 'privateRSA_lsh',
        'privateRSA_openssh', 'publicDSA_lsh', 'publicDSA_openssh',
        'publicRSA_lsh', 'publicRSA_openssh', 'privateRSA_openssh_alternate']
