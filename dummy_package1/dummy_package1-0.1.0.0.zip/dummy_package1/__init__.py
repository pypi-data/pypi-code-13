
__version__ = '0.1.0'

# import join methods
from dummy_package1.join.cosine_join import cosine_join
from dummy_package1.join.dice_join import dice_join
from dummy_package1.join.edit_distance_join import edit_distance_join
from dummy_package1.join.jaccard_join import jaccard_join
from dummy_package1.join.overlap_join import overlap_join
from dummy_package1.join.overlap_coefficient_join import overlap_coefficient_join

# import filters
from dummy_package1.filter.overlap_filter import OverlapFilter
from dummy_package1.filter.position_filter import PositionFilter
from dummy_package1.filter.prefix_filter import PrefixFilter
from dummy_package1.filter.size_filter import SizeFilter
from dummy_package1.filter.suffix_filter import SuffixFilter

# import matcher methods
from dummy_package1.matcher.apply_matcher import apply_matcher

# import profiling methods
from dummy_package1.profiler.profiler import profile_table_for_join

# import utility methods
from dummy_package1.utils.converter import dataframe_column_to_str, series_to_str

# import helper functions
from dummy_package1.utils.generic_helper import get_install_path
