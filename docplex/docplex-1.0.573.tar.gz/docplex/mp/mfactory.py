# --------------------------------------------------------------------------
# Source file provided under Apache License, Version 2.0, January 2004,
# http://www.apache.org/licenses/
# (c) Copyright IBM Corp. 2015, 2016
# --------------------------------------------------------------------------

# gendoc: ignore

import math

from docplex.mp.linear import Var, LinearExpr, MonomialExpr, AbstractLinearExpr, ZeroExpr
from docplex.mp.linear import _DummyFeasibleConstraint, _DummyInfeasibleConstraint
from docplex.mp.linear import LinearConstraintType, LinearConstraint, RangeConstraint, IndicatorConstraint
from docplex.mp.functional import MaximumExpr, MinimumExpr, AbsExpr
from docplex.mp.compat23 import fast_range
from docplex.mp.utils import *


def fix_format_string(fmt, dimen=1, key_format='_%s'):
    ''' Fixes a format string so that it contains dimen slots with %s inside
        arguments are:
         --- dimen is th enumber of slots we need
         --- key_format is the format in which the %s is embedded. By default '_%s'
             for example if each item has to be surrounded by {} set key_format to _{%s}
    '''
    assert (dimen >= 1)
    actual_nb_slots = 0
    curpos = 0
    str_size = len(fmt)
    while curpos < str_size and actual_nb_slots < dimen:
        new_pos = fmt.find('%', curpos)
        if new_pos < 0:
            break
        actual_nb_slots += 1
        if actual_nb_slots >= dimen:
            break
        curpos = new_pos + 2
    # how much slots do we need to add to the end of the string??
    nb_missing = max(0, dimen - actual_nb_slots)
    return fmt + nb_missing * (key_format % '%s')


def compile_naming_function(keys, user_name, default_fn, arity=1, key_format=None, _default_key_format='_%s'):
    # INTERNAL
    # builds a naming rule from an input , a dimension, and an optional meta-format
    # Makes sure the format string does contain the right number of format slots
    if user_name is None:
        return lambda k: default_fn()

    elif isinstance(user_name, str):
        if key_format is None:
            used_key_format = _default_key_format
        elif isinstance(key_format, str):
            used_key_format = key_format
        else:
            raise DOcplexException("key format accepts None or string, got: {0!r}".format(key_format))
        fixed_format_string = fix_format_string(user_name, arity, used_key_format)
        if 1 == arity:
            return lambda k: fixed_format_string % str(k)
        else:
            # here keys are tuples of size >= 2
            return lambda key_tuple: fixed_format_string % tuple(str(z) for z in key_tuple)

    elif is_function(user_name):
        return user_name

    elif is_iterable(user_name):
        key_to_names_dict = dict(zip(keys, user_name))
        # use a closure
        return lambda k: key_to_names_dict[k] if k in key_to_names_dict else default_fn()

    else:
        raise DOcplexException('Cannot use this for naming variables: {0!r} - expecting string, function or iterable'
                               .format(user_name))




class _AbstractModelFactory(object):
    def __init__(self, model):
        self._model = model
        self._error_handler = model.error_handler


class ModelFactory(object):
    def is_free_lb(self, var_lb):
        return var_lb <= - self.infinity

    def is_free_ub(self, var_ub):
        return var_ub >= self.infinity

    def __init__(self, model, engine):
        self._model = model
        self.__engine = engine
        self.infinity = engine.get_infinity()
        self.zero_expr = ZeroExpr(model)
        self.one_expr = None

    def get_one_expr(self):
        if self.one_expr is None:
            self.one_expr = LinearExpr(self._model, e=None, constant=1, safe=True)
        return self.one_expr

    def new_trivial_feasible_ct(self, name=None):
        return _DummyFeasibleConstraint(self._model, self.zero_expr, name=name)

    def new_trivial_infeasible_ct(self):
        return _DummyInfeasibleConstraint(self._model, self.zero_expr, self.get_one_expr())

    def fatal(self, msg, *args):
        self._model.fatal(msg, args)

    def warning(self, msg, *args):
        self._model.warning(msg, args)

    def update_engine(self, engine):
        # the model has already disposed the old engine, if any
        self.__engine = engine
        self.infinity = engine.get_infinity()

    def new_var(self, vartype, lb=None, ub=None, varname=None):
        self_model = self._model
        actual_name = varname or self_model._create_automatic_varname()
        var = Var(self_model, vartype, actual_name, lb, ub, is_automatic_name=not bool(varname))
        idx = self.__engine.create_one_variable(vartype, float(var.get_lb()), float(var.get_ub()), actual_name)
        self_model._register_one_var(var, idx, varname)
        return var

    def _expand_names(self, keys, user_name, arity, key_format):
        default_naming_fn = self._model._create_automatic_varname
        actual_naming_fn = compile_naming_function(keys, user_name, default_naming_fn, arity, key_format)
        computed_names = [str(actual_naming_fn(key)) for key in keys]
        # if is_function(user_name):
        #     # must check the result of user function.
        #     for key, name in izip(keys, computed_names):
        #         if not is_string(name):
        #             self.fatal("Name function must return a string, got: {0}, key: {1}".format(name, key))

        return computed_names

    def _expand_bounds(self, keys, var_bound, default_bound, size, is_lb_or_ub):
        ''' Converts raw bounds data (either LB or UB) to CPLEX-compatible bounds list.
            If lbs is None, this is the default, return [].
            If lbs is [] take the default again.
            If it is a number, build a list of size <size> with this number.
            If it is a list, use it if size ok (check numbers??),
            else try it as a function over keys.
        '''
        if var_bound is None:
            # default lb is zero, default ub is infinity
            return []

        elif is_number(var_bound):
            if is_lb_or_ub:
                if var_bound == default_bound:
                    return []
                else:
                    return [float(var_bound)] * size
            else:
                # ub
                if var_bound >= default_bound:
                    return []
                else:
                    return [float(var_bound)] * size

        elif isinstance(var_bound, str):
            self._bad_bounds_fatal(var_bound)

        elif isinstance(var_bound, list):
            nb_bounds = len(var_bound)
            if nb_bounds == 0:
                return None  # use defaults
            elif nb_bounds < size:
                # see how we can use defaults for those missing bounds
                self.fatal("Variable bounds list is too small, expecting: %d, got: %d" % (size, nb_bounds))
            else:
                if nb_bounds > size:
                    self.warning("Variable bounds list is too large, required: %d, got: %d." % (size, nb_bounds))
                for b, b_value in enumerate(var_bound):
                    if not is_number(b_value):
                        self.fatal("Variable bounds list expects numbers, got: {0!s} (pos: #{1})",
                                   b_value, b)
                return var_bound

        elif is_iterator(var_bound):
            # unfold the iterator, as CPLEX needs a list
            return list(var_bound)

        elif isinstance(var_bound, dict):
            return [var_bound.get(k, default_bound) for k in keys]
        else:
            # try a function?
            try:
                _computed_bounds = [var_bound(k) for k in keys]
                if not is_iterable(_computed_bounds):
                    self._bad_bounds_fatal(var_bound)
                elif _computed_bounds:
                    for b in _computed_bounds:
                        if not is_number(b):
                            self.fatal("computed bound expects a number, got: {0!s}", b)
                return _computed_bounds
            except TypeError:
                self._bad_bounds_fatal(var_bound)
            except Exception as e:
                self.fatal("error calling function model bounds: {0!s}, error: {1!s}", var_bound, e)

    def _bad_bounds_fatal(self, bad_bound):
        self.fatal("unexpected variable bound: {0!s}, expecting: None|number|function|iterable", bad_bound)

    # @profile
    def new_var_list(self, var_container,
                     keys, vartype,
                     lb=None, ub=None,
                     name=str,
                     arity=1, key_format=None,
                     allow_empty_keys=True):
        if not keys:
            if allow_empty_keys:
                return []
            else:
                self.fatal("No keys to index the variables.")
        else:
            if any((k is None for k in keys)):
                self.fatal("A variable key cannot be None, see: {0!s}", keys)

        mdl = self._model

        # compute defaults once
        default_lb = vartype.default_lb
        default_ub = vartype.default_ub
        number_of_vars = len(keys)
        xlbs = self._expand_bounds(keys, lb, default_lb, number_of_vars, is_lb_or_ub=True)
        xubs = self._expand_bounds(keys, ub, default_ub, number_of_vars, is_lb_or_ub=False)
        # at this point both list are either [] or have size numberOfVars
        use_default_lbs = False
        use_default_ubs = False
        nb_lbs = len(xlbs)
        if 0 == nb_lbs:
            use_default_lbs = True
        elif number_of_vars == nb_lbs:
            pass
        else:
            mdl.fatal("Internal error: bad lbs size, got: {0}, expecting: {1}", nb_lbs, number_of_vars)
        nb_ubs = len(xubs)
        if 0 == nb_ubs:
            use_default_ubs = True
        elif number_of_vars == nb_ubs:
            pass
        else:
            mdl.fatal("Internal error: bad ubs size, got: {0}, expecting: {1}", nb_ubs, number_of_vars)

        is_safe = use_default_ubs and use_default_lbs
        is_auto = name is None  # not bool(name)

        all_names = self._expand_names(keys, name, arity, key_format)

        allvars = [Var(mdl, vartype,
                       all_names[k],
                       xlbs[k] if xlbs else default_lb,
                       xubs[k] if xubs else default_ub,
                       _safe_domain=is_safe,
                       is_automatic_name=is_auto,
                       container=var_container) for k in fast_range(number_of_vars)]

        # query the engine for a list of indices.
        indices = self.__engine.create_variables(keys, vartype, xlbs, xubs, all_names)
        mdl._register_block_vars(allvars, indices, all_names)
        return allvars

    def constant_expr(self, cst, context=None):
        if 0 == cst:
            return self.zero_expr
        else:
            k = self.to_valid_number(cst, context=context)
            return LinearExpr(self._model, e=None, constant=k, safe=True)

    def linear_expr(self, e=0, constant=0, name=None):
        expr = LinearExpr(self._model, e, constant, name)
        return expr

    def to_valid_number(self, e, context=None, infinity=1e+20):
        if not is_number(e):
            self.fatal("Not a number: {}".format(e))
        elif math.isnan(e):
            msg = "NaN value found in expression"
            try:
                msg = "{0}: {1}".format(context(), msg)
            except TypeError:
                msg = "{0}: {1}".format(context, msg)
            self.fatal(msg)
        elif -infinity <= e <= infinity:
            return e
        elif e >= infinity:
            return infinity
        else:
            return -infinity

    def _to_linear_expr(self, e, linexpr_class=LinearExpr, force_clone=False, context=None):
        # INTERNAL
        if isinstance(e, linexpr_class):
            if force_clone:
                return e.clone()
            elif force_clone:
                return e.clone()
            else:
                # print('-- not cloning: {0!s}'.format(e))
                return e
        elif isinstance(e, (AbstractLinearExpr, Var, ZeroExpr)):
            return e.to_linear_expr()
        elif is_number(e):
            return self.constant_expr(cst=e, context=context)
        else:
            try:
                return e.to_linear_expr()
            except AttributeError:
                # delegate to the factory
                return self.linear_expr(e)

    def _to_expr(self, e):
        # INTERNAL
        if hasattr(e, "iter_terms"):
            return e
        elif is_number(e):
            return self.constant_expr(cst=e)
        else:
            try:
                return e.to_linear_expr()
            except DOCPlexQuadraticArithException:
                return e
            except AttributeError:
                pass
            self.fatal("cannot convert to expression: {0!r}", e)

    def new_monomial_expr(self, dvar, coef):
        # assume coef is a number here
        if 0 == coef:
            return self.zero_expr
        else:
            return MonomialExpr(self._model, dvar, coef)

    def _new_binary_constraint(self, lhs, ctype, rhs, name=None):
        # noinspection PyPep8
        left_expr  = self._to_linear_expr(lhs, context="LinearConstraint.left_expr")
        right_expr = self._to_linear_expr(rhs, context="LinearConstraint.right_expr")
        self._model._check_both_in_selfmodel(left_expr, right_expr, "new_binary_constraint")
        ct = LinearConstraint(self._model, left_expr, ctype, right_expr, name)
        left_expr.notify_used(ct)
        right_expr.notify_used(ct)
        return ct

    def new_le_constraint(self, e, rhs, ctname=None):
        return self._new_binary_constraint(e, LinearConstraintType.LE, rhs, name=ctname)

    def new_eq_constraint(self, e, rhs, ctname=None):
        return self._new_binary_constraint(e, LinearConstraintType.EQ, rhs, name=ctname)

    def new_ge_constraint(self, e, rhs, ctname=None):
        return self._new_binary_constraint(e, LinearConstraintType.GE, rhs, name=ctname)

    def new_range_constraint(self, lb, expr, rhs, ctname=None):
        # INTERNAL
        linexpr = self._to_linear_expr(expr)
        rng = RangeConstraint(self._model, linexpr, lb, rhs, ctname)
        linexpr.notify_used(rng)
        return rng

    def new_indicator_constraint(self, binary_var, linear_ct, active_value=1, ctname=None):
        # INTERNAL
        indicator_ct = IndicatorConstraint(self._model, binary_var, linear_ct, active_value, ctname)
        return indicator_ct

    def new_max_expr(self, *args):
        nb_args = len(args)
        if 0 == nb_args:
            return - self.infinity
        elif 1 == nb_args:
            return args[0]
        else:
            return MaximumExpr(self._model, args)

    def new_min_expr(self, *args):
        nb_args = len(args)
        if 0 == nb_args:
            return self.infinity
        elif 1 == nb_args:
            return args[0]
        else:
            return MinimumExpr(self._model, args)

    def new_abs_expr(self, e):
        if is_number(e):
            return abs(e)
        else:
            self_model = self._model
            return AbsExpr(self_model, self._to_linear_expr(e))

    def resync_whole_model(self):
        self_model = self._model
        self_engine = self.__engine

        for var in self_model.iter_variables():
            # do not call create_one_var public API
            # or resync would loop
            idx = self_engine.create_one_variable(var.vartype, var.lb, var.ub, var.name)
            if idx != var.get_index():
                print("index discrepancy: {0!s}, new index= {1}, old index={2}".format(var, idx,
                                                                                       var.get_index()))  # pragma: no cover

        for ct in self_model.iter_constraints():
            if isinstance(ct, LinearConstraint):
                self_engine.create_binary_linear_constraint(ct)
            elif isinstance(ct, RangeConstraint):
                self_engine.create_range_constraint(ct)
            elif isinstance(ct, IndicatorConstraint):
                self_engine.create_indicator_constraint(ct)
            else:
                self_model.error("Unexpected constraint type: {0!s} - ignored", type(ct))  # pragma: no cover

        # send objective
        self_engine.set_objective(self_model.objective_sense, self_model.objective_expr)
