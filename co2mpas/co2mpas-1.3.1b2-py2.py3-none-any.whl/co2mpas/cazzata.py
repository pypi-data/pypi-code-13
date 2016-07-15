import numpy as np
import pandas as pd
from scipy.integrate import cumtrapz
import co2mpas.dispatcher.utils as dsp_utl
def re_sampling(x, xp, fp):
    """
    Re-samples data maintaining the signal integral.

    :param x:
        The x-coordinates of the re-sampled values.
    :type x: np.array

    :param xp:
        The x-coordinates of the data points.
    :type xp: np.array

    :param fp:
        The y-coordinates of the data points, same length as xp.
    :type fp: np.array

    :return:
        Re-sampled y-values.
    :rtype: np.array
    """

    x, fp = np.asarray(x, dtype=float), np.asarray(fp, dtype=float)
    xp, y = np.asarray(xp, dtype=float), np.zeros_like(x)
    n = len(x)
    X, dx = np.zeros(n + 1), np.zeros(n + 1)
    dx[1:-1] = np.diff(x)
    X[0], X[1:-1], X[-1] = x[0], x[:-1] + dx[1:-1] / 2, x[-1]
    I = np.diff(np.interp(X, xp, cumtrapz(fp, xp, initial=0)))

    dx /= 8.0
    A = np.diag((dx[:-1] + dx[1:]) * 3.0)
    i, j = np.indices(A.shape)
    A[i == j - 1] = A[i - 1 == j] = dx[1:-1]

    return np.linalg.solve(A, I)

book = pd.ExcelFile('./input/sensitivity/params/data.xlsx')
writer = pd.ExcelWriter('./input/sensitivity/params/data_corrected.xlsx')
sheets = []

plan = []
keys = ['id', 'time_sample_frequency', 'velocities', 'phases_integration_times',
        'initial_temperature']
ref = '#%s!%s2:..:D:{"opts": {"empty": true},  "func": "redim", "kwds": {"col": 1}}'

name = 'f{}-t{}-{}'.format
def _var_plan(sn, f, t=''):
    v = ref % (sn, {1: 'A', 10: 'B'}[f])
    d = dsp_utl.map_list(keys, name(f, t, sn), f, v, '[(0, 4000)]', t)
    return d

for sn in book.sheet_names[1:]:
    velocities = book.parse(sn)['velocities'].values * 3.6
    times = np.array(range(0, len(velocities))) * 0.1
    new_time = np.array(range(0, int(max(times)) + 1))
    dfs = (
        pd.DataFrame({'velocities_1hz': re_sampling(new_time, times, velocities)}),
        pd.DataFrame({'velocities_10hz': velocities})
    )
    sheets.append((sn, dfs))
    plan.append(_var_plan(sn, 1, '80'))
    plan.append(_var_plan(sn, 10, '80'))

pd.DataFrame(plan).to_excel(writer, 'plan.prediction.wltp_h', index=False)
for sn, (df1, df2)  in sheets:
    df1.to_excel(writer, sn, index=False)
    df2.to_excel(writer, sn, index=False, startcol=1)
writer.save()