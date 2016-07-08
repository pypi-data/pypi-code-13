# -*- coding: utf-8 -*-
import bisect
from abjad.tools import durationtools
from abjad.tools.abctools import AbjadObject


class Inequality(AbjadObject):
    '''An inequality.

        >>> template = 'timespan_2.start_offset < timespan_1.start_offset'
        >>> inequality = timespantools.Inequality(template)

    ::

        >>> inequality
        Inequality('timespan_2.start_offset < timespan_1.start_offset')

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Time relations'

    __slots__ = (
        '_template',
        )

    templates = (
        'offset == timespan.start',
        'offset < timespan.start',
        'offset <= timespan.start',
        'offset == timespan.stop',
        'offset < timespan.stop',
        'offset <= timespan.stop',
        'timespan.start == offset',
        'timespan.start < offset',
        'timespan.start <= offset',
        'timespan.stop == offset',
        'timespan.stop < offset',
        'timespan.stop <= offset',
        'timespan_1.start_offset == timespan_2.start_offset',
        'timespan_1.start_offset < timespan_2.start_offset',
        'timespan_1.start_offset <= timespan_2.start_offset',
        'timespan_1.start_offset == timespan_2.stop_offset',
        'timespan_1.start_offset < timespan_2.stop_offset',
        'timespan_1.start_offset <= timespan_2.stop_offset',
        'timespan_1.stop_offset == timespan_2.start_offset',
        'timespan_1.stop_offset < timespan_2.start_offset',
        'timespan_1.stop_offset <= timespan_2.start_offset',
        'timespan_1.stop_offset == timespan_2.stop_offset',
        'timespan_1.stop_offset < timespan_2.stop_offset',
        'timespan_1.stop_offset <= timespan_2.stop_offset',
        'timespan_2.start_offset == timespan_1.start_offset',
        'timespan_2.start_offset < timespan_1.start_offset',
        'timespan_2.start_offset <= timespan_1.start_offset',
        'timespan_2.start_offset == timespan_1.stop_offset',
        'timespan_2.start_offset < timespan_1.stop_offset',
        'timespan_2.start_offset <= timespan_1.stop_offset',
        'timespan_2.stop_offset == timespan_1.start_offset',
        'timespan_2.stop_offset < timespan_1.start_offset',
        'timespan_2.stop_offset <= timespan_1.start_offset',
        'timespan_2.stop_offset == timespan_1.stop_offset',
        'timespan_2.stop_offset < timespan_1.stop_offset',
        'timespan_2.stop_offset <= timespan_1.stop_offset',
        )

    ### INITIALIZER ###

    def __init__(self, template=None):
        template = template or \
            'timespan_1.start_offset < timespan_2.start_offset'
        assert template in self.templates, repr(template)
        self._template = template

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats inequality.

            >>> print(format(inequality))
            timespantools.Inequality('timespan_2.start_offset < timespan_1.start_offset')

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        positional_argument_values = []
        positional_argument_values.append(self.template)
        return systemtools.StorageFormatSpecification(
            self,
            is_indented=False,
            keyword_argument_names=(),
            positional_argument_values=positional_argument_values,
            )

    ### PRIVATE METHODS ###

    def _find_index_ge(self, a, x):
        r'''Finds index of leftmost item greater than or equal to x.
        '''
        i = bisect.bisect_left(a, x)
        if i != len(a):
            return i
        raise ValueError

    def _find_index_gt(self, a, x):
        r'''Finds index of leftmost value greater than x.
        '''
        i = bisect.bisect_right(a, x)
        if i != len(a):
            return i
        raise ValueError

    def _find_index_le(self, a, x):
        r'''Finds index of rightmost value less than or equal to x.
        '''
        i = bisect.bisect_right(a, x)
        if i:
            return i - 1
        raise ValueError

    def _find_index_lt(self, a, x):
        r'''Finds index of rightmost value less than x.
        '''
        i = bisect.bisect_left(a, x)
        if i:
            return i - 1
        raise ValueError

    def _index(self, a, x):
        r'''Finds index of leftmost value exactly equal to x.
        '''
        i = bisect.bisect_left(a, x)
        if i != len(a) and a[i] == x:
            return i
        raise ValueError

    @staticmethod
    def _make_repr(offset):
        return 'Offset({}, {})'.format(*offset.pair)

    ### PUBLIC PROPERTIES ###

    @property
    def template(self):
        r'''Gets template of inequality.

            >>> inequality.template
            'timespan_2.start_offset < timespan_1.start_offset'

        Returns string.
        '''
        return self._template

    ### PUBLIC METHODS ###

    def evaluate(
        self,
        timespan_1_start_offset,
        timespan_1_stop_offset,
        timespan_2_start_offset,
        timespan_2_stop_offset,
        ):
        r'''Evalutes inequality.

        Returns true or false.
        '''
        make_repr = self._make_repr
        template = self.template
        template = template.replace(
            'timespan_1.start_offset', make_repr(timespan_1_start_offset))
        template = template.replace(
            'timespan_1.stop_offset', make_repr(timespan_1_stop_offset))
        template = template.replace(
            'timespan_2.start_offset', make_repr(timespan_2_start_offset))
        template = template.replace(
            'timespan_2.stop_offset', make_repr(timespan_2_stop_offset))
        truth_value = eval(template, {'Offset': durationtools.Offset})
        return truth_value

    def evaluate_offset_inequality(
        self,
        timespan_start,
        timespan_stop,
        offset,
        ):
        r'''Evalutes offset inequality.

        Returns true or false.
        '''
        make_repr = self._make_repr
        template = self.template
        template = self.template
        template = template.replace(
            'timespan.start', make_repr(timespan_start))
        template = template.replace(
            'timespan.stop', make_repr(timespan_stop))
        template = template.replace(
            'offset', make_repr(offset))
        truth_value = eval(template, {'Offset': durationtools.Offset})
        return truth_value

    def get_offset_indices(
        self,
        timespan_1,
        timespan_2_start_offsets,
        timespan_2_stop_offsets,
        ):
        r'''Gets offset indices of inequality.

        .. todo:: add example.

        Returns nonnegative integer pair.
        '''
        inequality = self.template
        assert isinstance(inequality, str), repr(inequality)
        leftmost_index, rightmost_index = None, None

        # 1.a
        if inequality == \
            'timespan_1.start_offset == timespan_2.start_offset':
            try:
                leftmost_index = self._find_index(
                    timespan_2_start_offsets, timespan_1.start_offset)
                rightmost_index = leftmost_index + 1
            except ValueError:
                pass
        # 1.b
        elif inequality == \
            'timespan_1.start_offset < timespan_2.start_offset':
            try:
                leftmost_index = self._find_index_gt(
                    timespan_2_start_offsets, timespan_1.start_offset)
                rightmost_index = len(timespan_2_start_offsets)
            except ValueError:
                pass
        # 1.c
        elif inequality == \
            'timespan_1.start_offset <= timespan_2.start_offset':
            try:
                leftmost_index = self._find_index_ge(
                    timespan_2_start_offsets, timespan_1.start_offset)
                rightmost_index = len(timespan_2_start_offsets)
            except ValueError:
                pass
        # 2.a
        elif inequality == \
            'timespan_1.start_offset == timespan_2.stop_offset':
            try:
                leftmost_index = self._find_index(
                    timespan_2_stop_offsets, timespan_1.start_offset)
                rightmost_index = leftmost_index + 1
            except ValueError:
                pass
        # 2.b
        elif inequality == \
            'timespan_1.start_offset < timespan_2.stop_offset':
            try:
                leftmost_index = self._find_index_gt(
                    timespan_2_stop_offsets, timespan_1.start_offset)
                rightmost_index = len(timespan_2_stop_offsets)
            except ValueError:
                pass
        # 2.c
        elif inequality == \
            'timespan_1.start_offset <= timespan_2.stop_offset':
            try:
                leftmost_index = self._find_index_ge(
                    timespan_2_stop_offsets, timespan_1.start_offset)
                rightmost_index = len(timespan_2_stop_offsets)
            except ValueError:
                pass
        # 3.a
        elif inequality == \
            'timespan_1.stop_offset == timespan_2.start_offset':
            try:
                leftmost_index = self._find_index(
                    timespan_2_start_offsets, timespan_1.stop_offset)
                rightmost_index = leftmost_index + 1
            except ValueError:
                pass
        # 3.b
        elif inequality == \
            'timespan_1.stop_offset < timespan_2.start_offset':
            try:
                leftmost_index = self._find_index_gt(
                    timespan_2_start_offsets, timespan_1.stop_offset)
                rightmost_index = len(timespan_2_start_offsets)
            except ValueError:
                pass
        # 3.c
        elif inequality == \
            'timespan_1.stop_offset <= timespan_2.start_offset':
            try:
                leftmost_index = self._find_index_ge(
                    timespan_2_start_offsets, timespan_1.stop_offset)
                rightmost_index = len(timespan_2_start_offsets)
            except ValueError:
                pass
        # 4.a
        elif inequality == \
            'timespan_1.stop_offset == timespan_2.stop_offset':
            try:
                leftmost_index = self._find_index(
                    timespan_2_start_offsets, timespan_1.stop_offset)
                rightmost_index = leftmost_index + 1
            except ValueError:
                pass
        # 4.b
        elif inequality == \
            'timespan_1.stop_offset < timespan_2.stop_offset':
            try:
                leftmost_index = self._find_index_gt(
                    timespan_2_stop_offsets, timespan_1.stop_offset)
                rightmost_index = len(timespan_2_stop_offsets)
            except ValueError:
                pass
        # 4.c
        elif inequality == \
            'timespan_1.stop_offset <= timespan_2.stop_offset':
            try:
                leftmost_index = self._find_index_ge(
                    timespan_2_stop_offsets, timespan_1.stop_offset)
                rightmost_index = len(timespan_2_stop_offsets)
            except ValueError:
                pass
        # 5.a
        elif inequality == \
            'timespan_2.start_offset == timespan_1.start_offset':
            try:
                leftmost_index = self._find_index(
                    timespan_2_start_offsets, timespan_1.start_offset)
                rightmost_index = leftmost_index + 1
            except ValueError:
                pass
        # 5.b
        elif inequality == \
            'timespan_2.start_offset < timespan_1.start_offset':
            try:
                leftmost_index = 0
                rightmost_index = self._find_index_ge(
                    timespan_2_start_offsets, timespan_1.start_offset)
            except ValueError:
                pass
        # 5.c
        elif inequality == \
            'timespan_2.start_offset <= timespan_1.start_offset':
            try:
                leftmost_index = 0
                rightmost_index = self._find_index_gt(
                    timespan_2_start_offsets, timespan_1.start_offset)
            except ValueError:
                pass
        # 6.a
        elif inequality == \
            'timespan_2.start_offset == timespan_1.stop_offset':
            try:
                leftmost_index = self._find_index(
                    timespan_2_start_offsets, timespan_1.stop_offset)
                rightmost_index = leftmost_index + 1
            except ValueError:
                pass
        # 6.b
        elif inequality == \
            'timespan_2.start_offset < timespan_1.stop_offset':
            try:
                leftmost_index = 0
                rightmost_index = self._find_index_ge(
                    timespan_2_start_offsets, timespan_1.stop_offset)
            except ValueError:
                pass
        # 6.c
        elif inequality == \
            'timespan_2.start_offset <= timespan_1.stop_offset':
            try:
                leftmost_index = 0
                rightmost_index = self._find_index_gt(
                    timespan_2_start_offsets, timespan_1.stop_offset)
            except ValueError:
                pass
        # 7.a
        elif inequality == \
            'timespan_2.stop_offset == timespan_1.start_offset':
            try:
                leftmost_index = self._find_index(
                    timespan_2_stop_offsets, timespan_1.start_offset)
                rightmost_index = leftmost_index + 1
            except ValueError:
                pass
        # 7.b
        elif inequality == \
            'timespan_2.stop_offset < timespan_1.start_offset':
            try:
                leftmost_index = 0
                rightmost_index = self._find_index_ge(
                    timespan_2_stop_offsets, timespan_1.start_offset)
            except ValueError:
                pass
        # 7.c
        elif inequality == \
            'timespan_2.stop_offset <= timespan_1.start_offset':
            try:
                leftmost_index = 0
                rightmost_index = self._find_index_gt(
                    timespan_2_stop_offsets, timespan_1.start_offset)
            except ValueError:
                pass
        # 8.a
        elif inequality == \
            'timespan_2.stop_offset == timespan_1.stop_offset':
            try:
                leftmost_index = self._find_index(
                    timespan_2_stop_offsets, timespan_1.stop_offset)
                rightmost_index = leftmost_index + 1
            except ValueError:
                pass
        # 8.b
        elif inequality == \
            'timespan_2.stop_offset < timespan_1.stop_offset':
            try:
                leftmost_index = 0
                rightmost_index = self._find_index_ge(
                    timespan_2_stop_offsets, timespan_1.stop_offset)
            except ValueError:
                pass
        # 8.c
        elif inequality == \
            'timespan_2.stop_offset <= timespan_1.stop_offset':
            try:
                leftmost_index = 0
                rightmost_index = self._find_index_gt(
                    timespan_2_stop_offsets, timespan_1.stop_offset)
            except ValueError:
                pass
        else:
            raise ValueError(inequality)

        if leftmost_index is not None and rightmost_index is not None:
            return leftmost_index, rightmost_index
        else:
            return []
