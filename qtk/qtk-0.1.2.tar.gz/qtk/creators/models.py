from scipy.optimize import root, least_squares, \
    differential_evolution, basinhopping
import numpy as np
import QuantLib as ql


from qtk.fields import Field as F
from qtk.templates import Template as T
from .common import CreatorBase


class SolverMixin(object):
    def cost_function_generator(self, model, helpers, norm=False):
        def cost_function(params):
            params_ = ql.Array(list(params))
            model.setParams(params_)
            error = [h.calibrationError() for h in helpers]
            if norm:
                return np.sqrt(np.sum(np.abs(error)))
            else:
                return error
        return cost_function

    def solve(self, method):
        model = self.setup_model()
        engine = self.setup_engine(model)
        helpers = self.setup_helpers()
        for h in helpers:
            h.setPricingEngine(engine)
        method = method.upper()
        if method == "LM":
            return self._solve_lm(model, helpers)
        elif (method == "LEASTSQUARES") or (method=="LS"):
            return self._solve_least_squares(model, helpers)
        elif (method == "DIFFERENTIALEVOLUTION") or (method == "DE"):
            return self._solve_differential_evolution(model, helpers)
        else:
            raise ValueError("Unrecognized solver choice %s" % method)

    def _solve_lm(self, model, helpers):
        initial_condition = list(model.params())
        cost_function = self.cost_function_generator(model, helpers)
        solution = root(cost_function, initial_condition, method='lm')
        return model

    def _solve_least_squares(self, model, helpers):
        initial_condition = list(model.params())
        cost_function = self.cost_function_generator(model, helpers)
        bound = self.bounds()
        solution = least_squares(cost_function,
                                 initial_condition,
                                 bounds=bound)
        return model

    def _solve_differential_evolution(self, model, helpers):
        cost_function = self.cost_function_generator(model, helpers, norm=True)
        bound = self.bounds(npinf=False)
        bound = zip(*bound)
        solution = differential_evolution(cost_function, bound, maxiter=100)
        return model

    def setup_helpers(self):
        raise NotImplementedError("The 'setup_helpers' method is not implemented for " + self.__class__.__name__)

    def setup_model(self):
        raise NotImplementedError("The 'setup_model' method is not implemented for "+self.__class__.__name__)

    def setup_engine(self, model=None):
        raise NotImplementedError("The 'setup_engine' method is not implemented for " + self.__class__.__name__)

    def bounds(self):
        return (-np.inf, np.inf)


class SwaptionHelperCreator(CreatorBase):
    _vol_type_map = {"SHIFTEDLOGNORMAL": ql.ShiftedLognormal, "NORMAL": ql.Normal}
    _templates = [T.INST_DERIVATIVE_SWAPTION_HELPER]
    _req_fields = [F.VOLATILITY, F.INDEX, F.DISCOUNT_CURVE]
    _opt_fields = [F.MATURITY_DATE, F.MATURITY_TENOR,
                   F.UNDERLYING_MATURITY_DATE, F.UNDERLYING_MATURITY_TENOR,
                   F.FIXED_LEG_TENOR, F.FIXED_LEG_BASIS, F.FLOAT_LEG_BASIS,
                   F.VOLATILITY, F.STRIKE, F.NOTIONAL, F.VOLATILITY_TYPE,
                   F.VOLATILITY_SHIFT]

    def _create(self, asof_date):
        maturity = self.get(F.MATURITY_DATE) or \
                   self.get(F.MATURITY_TENOR)
        undl_maturity = self.get(F.UNDERLYING_MATURITY_DATE) or \
                        self.get(F.UNDERLYING_MATURITY_TENOR)
        assert maturity is not None
        assert undl_maturity is not None
        vols = self[F.VOLATILITY]
        vol_quote = ql.QuoteHandle(ql.SimpleQuote(vols))
        index = self[F.INDEX]
        fixed_tenor = self.get(F.FIXED_LEG_TENOR)
        fixed_basis = self.get(F.FIXED_LEG_BASIS)
        float_basis = self.get(F.FLOAT_LEG_BASIS) or fixed_basis
        fixed_basis = fixed_basis or float_basis
        yield_curve = self[F.DISCOUNT_CURVE]
        yield_handle = ql.YieldTermStructureHandle(yield_curve)
        strike = self.get(F.STRIKE, ql.nullDouble())
        notional = self.get(F.NOTIONAL, 1.0)
        vol_type = self.get(F.VOLATILITY_TYPE, "ShiftedLogNormal")
        vol_type = vol_type.upper()
        vol_type_enum = self._vol_type_map.get(vol_type, ql.ShiftedLognormal)
        vol_shift = self.get(F.VOLATILITY_SHIFT, 0.0)
        swaption_helper = ql.SwaptionHelper(
            maturity, undl_maturity, vol_quote, index, fixed_tenor, fixed_basis,
            float_basis, yield_handle, ql.CalibrationHelper.RelativePriceError,
            strike, notional, vol_type_enum, vol_shift)

        return swaption_helper


class HullWhite1FCreator(CreatorBase, SolverMixin):
    _templates = [T.MODELS_YIELD_HW1F]
    _req_fields = [F.YIELD_CURVE]
    _opt_fields = [F.ALPHA, F.SIGMA1, F.INSTRUMENT_COLLECTION, F.SOLVER]

    def _create(self, asof_date):
        alpha = self.get(F.ALPHA)
        sigma1 = self.get(F.SIGMA1)
        yield_curve = self[F.YIELD_CURVE]
        yield_handle = ql.YieldTermStructureHandle(yield_curve)
        calibrate = self.get(F.CALIBRATE, False)
        if calibrate:
            method = self.get(F.SOLVER, "LEASTSQUARES")
            model = self.solve(method)
        elif (alpha is not None) and (sigma1 is not None):
            model = ql.HullWhite(yield_handle, alpha, sigma1)
        else:
            raise ValueError(
                "Parameter %s and %s should be provided for model or %s should be True"
                %(F.ALPHA.id, F.SIGMA1.id, F.CALIBRATE.id))

        return model

    def setup_model(self):
        yield_curve = self[F.YIELD_CURVE]
        yield_handle = ql.YieldTermStructureHandle(yield_curve)
        alpha = self.get(F.ALPHA, 0.025)
        sigma1 = self.get(F.SIGMA1, 0.05)
        return ql.HullWhite(yield_handle, alpha, sigma1)

    def setup_engine(self, model=None):
        if model is not None:
            engine = ql.JamshidianSwaptionEngine(model)
            return engine
        else:
            raise ValueError("Input model cannot be None")

    def setup_helpers(self):
        helpers_dict = self.get(F.INSTRUMENT_COLLECTION)
        helpers = [h[F.OBJECT.id] for h in helpers_dict]
        return helpers

    def bounds(self, npinf=True):
        alpha = self.get(F.ALPHA)
        sigma1 = self.get(F.SIGMA1)
        delta = 1e-15
        maxinf = np.inf if npinf else (1-delta)
        mininf = -np.inf if npinf else (-1+delta)
        bound = ([(alpha or mininf)-delta, (sigma1 or 1e-15)-delta],
                 [(alpha or maxinf)+delta, (sigma1 or maxinf)+delta])
        return bound