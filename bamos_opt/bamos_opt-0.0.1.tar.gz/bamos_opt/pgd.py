import numpy as np


def solve(x0, f, g, proj, eps, maxit, lam=None, acc=True,
          doLinesearch=True, callback=None):
    results = {
        'feval': 0,
        'geval': 0
    }

    x = proj(np.copy(x0))
    prev_x = x

    results['bestF'] = None
    results['bestX'] = np.copy(x)

    for k in range(maxit):
        omega = (k - 1.0) / (k + 2.0)
        d = x - prev_x
        y = x if acc else x + omega * d
        if k > 1 and np.linalg.norm(d) < eps:
            break
        f_y = f(y)
        g_y = g(y)
        prev_x = x
        if doLinesearch:
            lam = 1
            beta = 0.5
            while True:
                x = proj(y - lam * g_y)
                dxy = x - y
                f_x = f(x)
                results['feval'] = results['feval'] + 1
                if f_x <= f_y + np.dot(g_y, dxy) + np.linalg.norm(dxy)**2 / (2 * lam):
                    break
                lam = beta * lam
        else:
            x = proj(y - lam*g_y)
            f_x = f(x)
            results['feval'] = results['feval'] + 1

        if results['bestF'] is None or f_x < results['bestF']:
            results['bestF'] = f_x
            results['bestX'][:] = x

        if callback:
            callback(k, results['bestF'], y, g_y, lam)

    return results
