from typing import Tuple
from typing import List
from typing import Union

# RGB = Union[Tuple[int, int, int], List[int, int, int]]
RGB_tuple = Tuple[int, int, int]
RGB_list = list
RGB = Union[RGB_tuple, list]

def test_function(color: RGB_tuple):
    print(color[0])


my_color = (255, 0, 0)
test_function(my_color)
