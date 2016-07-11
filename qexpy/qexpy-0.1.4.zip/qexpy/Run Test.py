import error as e
import plotting as p
import numpy as np

e.Measurement.set_method('Derivative')

data = np.array([
                [387.924,    9,  2.0],
                [388.238,   11,  2.0],
                [388.552,   17,  2.0],
                [388.615,   17,  2.0],
                [388.678,   21,  2.0],
                [388.741,   24,  2.0],
                [388.804,   25,  2.0],
                [388.866,   29,  2.0],
                [388.929,   33,  2.0],
                [388.992,   41,  2.0],
                [389.055,   48,  2.0],
                [389.118,   56,  2.0],
                [389.180,   63,  2.0],
                [389.243,   64,  2.0],
                [389.306,   61,  2.0],
                [389.369,   51,  2.0],
                [389.432,   41,  2.0],
                [389.495,   34,  2.0],
                [389.557,   28,  2.0],
                [389.620,   25,  2.0],
                [389.683,   21,  2.0],
                [389.746,   19,  2.0],
                [389.809,   18,  2.0],
                [389.872,   16,  2.0],
                [390.186,   11,  2.0],
                [390.500,    8,  2.0]], dtype='float64')

w = e.Measurement(data[:, 0], name='Angular Frequeny',
                  units=['rads', 1, 's', -1])
s = e.Measurement(data[:, 1], data[:, 2], name='Amplitude', units='mm')


def Response(w, C, wn, Q):
    top = (C*Q)/(np.multiply(wn, w))
    bot = np.sqrt(np.power((wn/w - w/wn), 2)*np.power(Q, 2)+1)
    return top/bot

figure = p.Plot(w, s)
figure.fit(Response, guess=[2800, 389.3, 1140])
figure.residuals()
figure.show('file')
