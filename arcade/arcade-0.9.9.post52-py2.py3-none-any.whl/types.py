from typing import Tuple
from typing import List
from typing import Union

RGB = Union[Tuple[int, int, int], List[int, int, int]]
RGBA = Union[Tuple[int, int, int, int], List[int, int, int, int]]
Color = Union[RGB, RGBA]
Point = Union[Tuple[int, int], List[int, int]]
PointList = Union[Tuple[Point, ...], List[Point, ...]]
