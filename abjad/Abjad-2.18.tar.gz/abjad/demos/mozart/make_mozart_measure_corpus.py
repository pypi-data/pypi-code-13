# -*- coding: utf-8 -*-


def make_mozart_measure_corpus():
    r'''Makes Mozart measure corpus.
    '''

    return [
        [
            {'b': 'c4 r8', 't': "e''8 c''8 g'8"},
            {'b': '<c e>4 r8', 't': "g'8 c''8 e''8"},
            {'b': '<c e>4 r8', 't': "g''8 ( e''8 c''8 )"},
            {'b': '<c e>4 r8', 't': "c''16 b'16 c''16 e''16 g'16 c''16"},
            {'b': '<c e>4 r8', 't': "c'''16 b''16 c'''16 g''16 e''16 c''16"},
            {'b': 'c4 r8', 't': "e''16 d''16 e''16 g''16 c'''16 g''16"},
            {'b': '<c e>4 r8', 't': "g''8 f''16 e''16 d''16 c''16"},
            {'b': '<c e>4 r8', 't': "e''16 c''16 g''16 e''16 c'''16 g''16"},
            {'b': '<c e>16 g16 <c e>16 g16 <c e>16 g16', 't': "c''8 g'8 e''8"},
            {'b': '<c e>4 r8', 't': "g''8 c''8 e''8"},
            {'b': 'c8 c8 c8', 't': "<e' c''>8 <e' c''>8 <e' c''>8"},
        ],
        [
            {'b': 'c4 r8', 't': "e''8 c''8 g'8"},
            {'b': '<c e>4 r8', 't': "g'8 c''8 e''8"},
            {'b': '<c e>4 r8', 't': "g''8 e''8 c''8"},
            {'b': '<e g>4 r8', 't': "c''16 g'16 c''16 e''16 g'16 c''16"},
            {'b': '<c e>4 r8', 't': "c'''16 b''16 c'''16 g''16 e''16 c''16"},
            {'b': 'c4 r8', 't': "e''16 d''16 e''16 g''16 c'''16 g''16"},
            {'b': '<c e>4 r8', 't': "g''8 f''16 e''16 d''16 c''16"},
            {'b': '<c e>4 r8', 't': "c''16 g'16 e''16 c''16 g''16 e''16"},
            {'b': '<c e>4 r8', 't': "c''8 g'8 e''8"},
            {'b': '<c e>4 <c g>8', 't': "g''8 c''8 e''8"},
            {'b': 'c8 c8 c8', 't': "<e' c''>8 <e' c''>8 <e' c''>8"},
        ],
        [
            {'b': '<b, g>4 g,8', 't': "d''16 e''16 f''16 d''16 c''16 b'16"},
            {'b': 'g,4 r8', 't': "b'8 d''8 g''8"},
            {'b': 'g,4 r8', 't': "b'8 d''16 b'16 a'16 g'16"},
            {'b': '<g b>4 r8', 't': "f''8 d''8 b'8"},
            {'b': '<b, d>4 r8', 't': "g''16 fs''16 g''16 d''16 b'16 g'16"},
            {'b': '<g b>4 r8', 't': "f''16 e''16 f''16 d''16 c''16 b'16"},
            {'b': '<g, g>4 <b, g>8',
                't': "b'16 c''16 d''16 e''16 f''16 d''16"},
            {'b': 'g8 g8 g8', 't': "<b' d''>8 <b' d''>8 <b' d''>8"},
            {'b': 'g,4 r8', 't': "b'16 c''16 d''16 b'16 a'16 g'16"},
            {'b': 'b,4 r8', 't': "d''8 ( b'8 g'8 )"},
            {'b': 'g4 r8', 't': "b'16 a'16 b'16 c''16 d''16 b'16"},
        ],
        [
            {'b': '<c e>4 r8', 't': "c''16 b'16 c''16 e''16 g'8"},
            {'b': 'c4 r8', 't': "e''16 c''16 b'16 c''16 g'8"},
            {'b': '<e g>4 r8', 't': "c''8 ( g'8 e'8 )"},
            {'b': '<e g>4 r8', 't': "c''8 e''8 g'8"},
            {'b': '<e g>4 r8', 't': "c''16 b'16 c''16 g'16 e'16 c'16"},
            {'b': '<c e>4 r8', 't': "c''8 c''16 d''16 e''8"},
            {'b': 'c4 r8',
                't': "<c'' e''>8 <c'' e''>16 <d'' f''>16 <e'' g''>8"},
            {'b': '<e g>4 r8', 't': "c''8 e''16 c''16 g'8"},
            {'b': '<e g>4 r8', 't': "c''16 g'16 e''16 c''16 g''8"},
            {'b': '<e g>4 r8', 't': "c''8 e''16 c''16 g''8"},
            {'b': '<e g>4 r8', 't': "c''16 e''16 c''16 g'16 e'8"},
        ],
        [
            {'b': 'c4 r8', 't': "fs''8 a''16 fs''16 d''16 fs''16"},
            {'b': 'c8 c8 c8', 't': "<fs' d''>8 <d'' fs''>8 <fs'' a''>8"},
            {'b': 'c4 r8', 't': "d''16 a'16 fs''16 d''16 a''16 fs''16"},
            {'b': 'c8 c8 c8', 't': "<fs' d''>8 <fs' d''>8 <fs' d''>8"},
            {'b': 'c4 r8', 't': "d''8 a'8 ^\\turn fs''8"},
            {'b': 'c4 r8', 't': "d''16 cs''16 d''16 fs''16 a''16 fs''16"},
            {'b': '<c a>4 <c a>8', 't': "fs''8 a''8 d''8"},
            {'b': '<c fs>8 <c fs>8 <c a>8', 't': "a'8 a'16 d''16 fs''8"},
            {'b': 'c8 c8 c8', 't': "<d'' fs''>8 <d'' fs''>8 <d'' fs''>8"},
            {'b': '<c d>8 <c d>8 <c d>8', 't': "fs''8 fs''16 d''16 a''8"},
            {'b': '<c a>4 r8', 't': "fs''16 d''16 a'16 a''16 fs''16 d''16"},
        ],
        [
            {'b': '<b, d>8 <b, d>8 <b, d>8',
                't': "g''16 fs''16 g''16 b''16 d''8"},
            {'b': '<b, d>4 r8', 't': "g''8 b''16 g''16 d''16 b'16"},
            {'b': '<b, d>4 r8', 't': "g''8 b''8 d''8"},
            {'b': '<b, g>4 r8', 't': "a'8 fs'16 g'16 b'16 g''16"},
            {'b': '<b, d>4 <b, g>8',
                't': "g''16 fs''16 g''16 d''16 b'16 g'16"},
            {'b': 'b,4 r8', 't': "g''8 b''16 g''16 d''16 g''16"},
            {'b': '<b, g>4 r8', 't': "d''8 g''16 d''16 b'16 d''16"},
            {'b': '<b, g>4 r8', 't': "d''8 d''16 g''16 b''8"},
            {'b': '<b, d>8 <b, d>8 <b, g>8',
                't': "a''16 g''16 fs''16 g''16 d''8"},
            {'b': '<b, d>4 r8', 't': "g''8 g''16 d''16 b''8"},
            {'b': '<b, d>4 r8', 't': "g''16 b''16 g''16 d''16 b'8"},
        ],
        [
            {'b': 'c8 d8 d,8', 't': "e''16 c''16 b'16 a'16 g'16 fs'16"},
            {'b': 'c8 d8 d,8',
                't': "a'16 e''16 <b' d''>16 <a' c''>16 <g' b'>16 <fs' a'>16"},
            {'b': 'c8 d8 d,8',
                't': "<b' d''>16 ( <a' c''>16 ) <a' c''>16 ( <g' b'>16 ) "
                    "<g' b'>16 ( <fs' a'>16 )"},
            {'b': 'c8 d8 d,8', 't': "e''16 g''16 d''16 c''16 b'16 a'16"},
            {'b': 'c8 d8 d,8', 't': "a'16 e''16 d''16 g''16 fs''16 a''16"},
            {'b': 'c8 d8 d,8', 't': "e''16 a''16 g''16 b''16 fs''16 a''16"},
            {'b': 'c8 d8 d,8', 't': "c''16 e''16 g''16 d''16 a'16 fs''16"},
            {'b': 'c8 d8 d,8', 't': "e''16 g''16 d''16 g''16 a'16 fs''16"},
            {'b': 'c8 d8 d,8', 't': "e''16 c''16 b'16 g'16 a'16 fs'16"},
            {'b': 'c8 d8 d,8', 't': "e''16 c'''16 b''16 g''16 a''16 fs''16"},
            {'b': 'c8 d8 d,8', 't': "a'8 d''16 c''16 b'16 a'16"},
        ],
        [
            {'b': 'g,8 g16 f16 e16 d16', 't': "<g' b' d'' g''>4 r8"},
            {'b': 'g,8 b16 g16 fs16 e16', 't': "<g' b' d'' g''>4 r8"},
        ],
        [
            {'b': 'd4 c8', 't': "fs''8 a''16 fs''16 d''16 fs''16"},
            {'b': '<d fs>4 r8', 't': "d''16 a'16 d''16 fs''16 a''16 fs''16"},
            {'b': '<d a>8 <d fs>8 <c d>8', 't': "fs''8 a''8 fs''8"},
            {'b': '<c a>4 <c a>8',
                't': "fs''16 a''16 d'''16 a''16 fs''16 a''16"},
            {'b': 'd4 c8', 't': "d'16 fs'16 a'16 d''16 fs''16 a''16"},
            {'b': 'd,16 d16 cs16 d16 c16 d16',
                't': "<a' d'' fs''>8 fs''4 ^\\trill"},
            {'b': '<d fs>4 <c fs>8', 't': "a''8 ( fs''8 d''8 )"},
            {'b': '<d fs>4 <c fs>8', 't': "d'''8 a''16 fs''16 d''16 a'16"},
            {'b': '<d fs>4 r8', 't': "d''16 a'16 d''8 fs''8"},
            {'b': '<c a>4 <c a>8', 't': "fs''16 d''16 a'8 fs''8"},
            {'b': '<d fs>4 <c a>8', 't': "a'8 d''8 fs''8"},
        ],
        [
            {'b': '<b, g>4 r8', 't': "g''8 b''16 g''16 d''8"},
            {'b': 'b,16 d16 g16 d16 b,16 g,16', 't': "g''8 g'8 g'8"},
            {'b': 'b,4 r8', 't': "g''16 b''16 g''16 b''16 d''8"},
            {'b': '<b, d>4 <b, d>8',
                't': "a''16 g''16 b''16 g''16 d''16 g''16"},
            {'b': '<b, d>4 <b, d>8', 't': "g''8 d''16 b'16 g'8"},
            {'b': '<b, d>4 <b, d>8', 't': "g''16 b''16 d'''16 b''16 g''8"},
            {'b': '<b, d>4 r8', 't': "g''16 b''16 g''16 d''16 b'16 g'16"},
            {'b': '<b, d>4 <b, d>8',
                't': "g''16 d''16 g''16 b''16 g''16 d''16"},
            {'b': '<b, d>4 <b, g>8', 't': "g''16 b''16 g''8 d''8"},
            {'b': 'g,16 b,16 g8 b,8', 't': "g''8 d''4 ^\\trill"},
            {'b': 'b,4 r8', 't': "g''8 b''16 d'''16 d''8"},
        ],
        [
            {'b': "c16 e16 g16 e16 c'16 c16",
                't': "<c'' e''>8 <c'' e''>8 <c'' e''>8"},
            {'b': 'e4 e16 c16',
                't': "c''16 g'16 c''16 e''16 g''16 <c'' e''>16"},
            {'b': '<c g>4 <c e>8', 't': "e''8 g''16 e''16 c''8"},
            {'b': '<c g>4 r8', 't': "e''16 c''16 e''16 g''16 c'''16 g''16"},
            {'b': '<c g>4 <c g>8',
                't': "e''16 g''16 c'''16 g''16 e''16 c''16"},
            {'b': 'c16 b,16 c16 d16 e16 fs16',
                't': "<g' c'' e''>8 e''4 ^\\trill"},
            {'b': '<c e>16 g16 <c e>16 g16 <c e>16 g16', 't': "e''8 c''8 g'8"},
            {'b': '<c g>4 <c e>8', 't': "e''8 c''16 e''16 g''16 c'''16"},
            {'b': '<c g>4 <c e>8', 't': "e''16 c''16 e''8 g''8"},
            {'b': '<c g>4 <c g>8', 't': "e''16 c''16 g'8 e''8"},
            {'b': '<c g>4 <c e>8', 't': "e''8 ( g''8 c'''8 )"},
        ],
        [
            {'b': 'g4 g,8', 't': "<c'' e''>8 <b' d''>8 r8"},
            {'b': '<g, g>4 g8', 't': "d''16 b'16 g'8 r8"},
            {'b': 'g8 g,8 r8', 't': "<c'' e''>8 <b' d''>16 <g' b'>16 g'8"},
            {'b': 'g4 r8', 't': "e''16 c''16 d''16 b'16 g'8"},
            {'b': 'g8 g,8 r8', 't': "g''16 e''16 d''16 b'16 g'8"},
            {'b': 'g4 g,8', 't': "b'16 d''16 g''16 d''16 b'8"},
            {'b': 'g8 g,8 r8', 't': "e''16 c''16 b'16 d''16 g''8"},
            {'b': '<g b>4 r8', 't': "d''16 b''16 g''16 d''16 b'8"},
            {'b': '<b, g>4 <b, d>8', 't': "d''16 b'16 g'8 g''8"},
            {'b': 'g16 fs16 g16 d16 b,16 g,16', 't': "d''8 g'4"},
        ],
        [
            {'b': '<c e>16 g16 <c e>16 g16 <c e>16 g16', 't': "e''8 c''8 g'8"},
            {'b': '<c e>16 g16 <c e>16 g16 <c e>16 g16', 't': "g'8 c''8 e''8"},
            {'b': '<c e>16 g16 <c e>16 g16 <c e>16 g16',
                't': "g''8 e''8 c''8"},
            {'b': '<c e>4 <e g>8', 't': "c''16 b'16 c''16 e''16 g'16 c''16"},
            {'b': '<c e>4 <c g>8',
                't': "c'''16 b''16 c'''16 g''16 e''16 c''16"},
            {'b': '<c g>4 <c e>8',
                't': "e''16 d''16 e''16 g''16 c'''16 g''16"},
            {'b': '<c e>4 r8', 't': "g''8 f''16 e''16 d''16 c''16"},
            {'b': '<c e>4 r8', 't': "c''16 g'16 e''16 c''16 g''16 e''16"},
            {'b': '<c e>16 g16 <c e>16 g16 <c e>16 g16', 't': "c''8 g'8 e''8"},
            {'b': '<c e>16 g16 <c e>16 g16 <c e>16 g16',
                't': "g''8 c''8 e''8"},
            {'b': 'c8 c8 c8', 't': "<e' c''>8 <e' c''>8 <e' c''>8"},
        ],
        [
            {'b': '<c e>16 g16 <c e>16 g16 <c e>16 g16',
                't': "e''8 ( c''8 g'8 )"},
            {'b': '<c e>4 <c g>8', 't': "g'8 ( c''8 e''8 )"},
            {'b': '<c e>16 g16 <c e>16 g16 <c e>16 g16',
                't': "g''8 e''8 c''8"},
            {'b': '<c e>4 <c e>8', 't': "c''16 b'16 c''16 e''16 g'16 c''16"},
            {'b': '<c e>4 r8', 't': "c'''16 b''16 c'''16 g''16 e''16 c''16"},
            {'b': '<c g>4 <c e>8',
                't': "e''16 d''16 e''16 g''16 c'''16 g''16"},
            {'b': '<c e>4 <e g>8', 't': "g''8 f''16 e''16 d''16 c''16"},
            {'b': '<c e>4 r8', 't': "c''16 g'16 e''16 c''16 g''16 e''16"},
            {'b': '<c e>16 g16 <c e>16 g16 <c e>16 g16', 't': "c''8 g'8 e''8"},
            {'b': '<c e>16 g16 <c e>16 g16 <c e>16 g16',
                't': "g''8 c''8 e''8"},
            {'b': 'c8 c8 c8', 't': "<e' c''>8 <e' c''>8 <e' c''>8"},
        ],
        [
            {'b': "<f a>4 <g d'>8", 't': "d''16 f''16 d''16 f''16 b'16 d''16"},
            {'b': 'f4 g8', 't': "d''16 f''16 a''16 f''16 d''16 b'16"},
            {'b': 'f4 g8', 't': "d''16 f''16 a'16 d''16 b'16 d''16"},
            {'b': 'f4 g8', 't': "d''16 ( cs''16 ) d''16 f''16 g'16 b'16"},
            {'b': 'f8 d8 g8', 't': "f''8 d''8 g''8"},
            {'b': 'f16 e16 d16 e16 f16 g16',
                't': "f''16 e''16 d''16 e''16 f''16 g''16"},
            {'b': 'f16 e16 d8 g8', 't': "f''16 e''16 d''8 g''8"},
            {'b': 'f4 g8', 't': "f''16 e''16 d''16 c''16 b'16 d''16"},
            {'b': 'f4 g8', 't': "f''16 d''16 a'8 b'8"},
            {'b': 'f4 g8', 't': "f''16 a''16 a'8 b'16 d''16"},
            {'b': 'f4 g8', 't': "a'8 f''16 d''16 a'16 b'16"},
        ],
        [
            {'b': 'c8 g,8 c,8', 't': "c''4 r8"},
            {'b': 'c4 c,8', 't': "c''8 c'8 r8"},
        ],
    ]
