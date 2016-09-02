# Copyright 2016 Red Hat, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Generating approximation indicators. """


class ApproxPrefix(object):
    """
    Class that transforms numeric value by prepending an approximation prefix,
    based on the relation. The approximation prefix varies, based on the
    amount of the difference indicated by the relation.
    """
    # pylint: disable=too-few-public-methods

    def __init__(self, limits):
        """
        Initializer.

        :param limits: the limits of the various buckets
        :type limits: list of Rational, may be the empty list

        The limits must be all non-zero and in ascending order.
        """
        self.limits = limits

    @staticmethod
    def _relation_to_symbol(relation):
        """
        Change a numeric relation to a string symbol.

        :param Rational relation: the relation

        :returns: a symbol with the right relation to ``relation`` or None
        :rtype: str or NoneType
        """
        if relation == 0:
            return None
        elif relation < 0:
            return '>'
        elif relation > 0:
            return '<'
        else:
            assert False # pragma: no cover

    def _amount(self, relation):
        """
        Convert relation to an int value.

        :param Rational relation: the relation
        :returns: an int, indicating the category of the relation
        :rtype: int
        """
        if relation == 0: # pragma: no cover
            return 0

        abs_relation = abs(relation)
        return next(
           (i for i, l in enumerate(self.limits) if abs_relation < l),
           len(self.limits)
        ) + 1


    def xform(self, relation, value):
        """
        Decorate ``value`` with approximation indicator for ``relation``.

        :param Rational relation: relation of ``value`` to value it represents
        :param str value: a value to decorate
        """
        approx_str = ApproxPrefix._relation_to_symbol(relation)
        if approx_str is not None:
            return "%s %s" % (approx_str * self._amount(relation), value)
        else:
            return value
