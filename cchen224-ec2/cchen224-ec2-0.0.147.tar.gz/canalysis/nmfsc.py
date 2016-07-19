import numpy as np
import cmath


class NMF:

    def __init__(self, sparseness_W=None, sparseness_H=None, initialization=None, **control):
        self.sparseness_W = sparseness_W
        self.sparseness_H = sparseness_H

        self._stepsize_W = control.get('stepsize_W', .15)
        self._stepsize_H = control.get('stepsize_H', .15)
        self._iteration_criterion = control.get('iteration_criterion', 1e-200)
        self._eps = control.get('eps', 1e-8)
        self._Z = control.get('Z', [])

        pass

    def initialize(self):
        pass

    def decompose(self, V, r):
        n, k = V.shape
        # TODO initialize SVD
        W = np.random.standard_normal((n, r)) ** 2
        H = np.random.standard_normal((r, k)) ** 2


        if not self.sparseness_W:
            self._project(W.T, self.sparseness_W)
        if not self.sparseness_H:
            self._project(H, self.sparseness_H)

        # TODO record objhistory

        # start iteration (step 4 on page 1462)
        iter = 0
        while True:
            iter += 1

            if not self.sparseness_W:
                W -= self._stepsize_W * np.dot((np.dot(W, H) - V), H.T)
                error = 0.5 * sum(sum((V - np.dot(W, H)) ** 2))
                while True:
                    self._project(W.T, self.sparseness_W)
                    if error > 0.5 * sum(sum((V - np.dot(W, H)) ** 2)):
                        break
                    self._stepsize_W /= 2.
                    if self._stepsize_W < self._iteration_criterion:
                        return W, H
                    self._stepsize_W *= 1.2
            else:
                W *= np.dot(V, H.T) / (np.dot(W, np.dot(H, H.T)) + self._eps)

            if not self.sparseness_H:
                H -= self._stepsize_H * np.dot(W.T, np.dot(W, H) - V)
                error = 0.5 * sum(sum((V - np.dot(W, H)) ** 2))
                while True:
                    self._project(H, self.sparseness_H)
                    if error > 0.5 * sum(sum((V - np.dot(W, H)) ** 2)):
                        break
                    self._stepsize_H /= 2.
                    if self._stepsize_H < self._iteration_criterion:
                        return W, H
                    self._stepsize_H *= 1.2
            else:
                H *= np.dot(W.T, V) / (np.dot(np.dot(W.T, W), H) + self._eps)



    def _project(self, X, sparseness):
        for counter, row in enumerate(X):
            L2 = np.sqrt(np.dot(row, row))
            X[counter] = self._project(row, self._sparseness(sparseness, row, 1.), 1.)

    def _project_per_column(self, x, L1, L2):
        # Given any vector x, find the closest non-negative vector s with a given L1 and L2 norm.
        n = len(x)

        s = x + (L1 - x.sum()) / n
        # TODO: introduce initial zero matrix
        Z = np.zeros(n, bool)

        while True:
            m = (~Z) * L1 / (n - Z.sum())
            alpha = self._solve_alpha(s, m, L2)
            s = m + alpha * (s - m)
            negs = (s < 0)

            if not negs.any():
                return s

            Z |= negs
            s[Z] = 0
            c = (sum(s) - L1) / (~Z).sum()
            s -= c * (~Z)

    @staticmethod
    def _sparseness(s, x, L2):
        # TODO review page 1460
        sn = np.sqrt(len(x))
        return L2 * (s + sn - s * sn)

    @staticmethod
    def _solve_alpha(s, m, L2):
        w = s - m
        a = sum((w ** 2))
        b = 2 * np.dot(w, s.T)
        c = sum(s ** 2) - L2
        alpha = (-b + cmath.sqrt(b ** 2 - 4 * a * c).real) / (2 * a)
        return alpha
