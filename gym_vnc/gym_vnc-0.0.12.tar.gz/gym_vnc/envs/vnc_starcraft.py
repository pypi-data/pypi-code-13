import string

from gym_vnc import spaces
from gym_vnc.spaces import vnc_event
from gym_vnc.envs import vnc_env


class VNCStarCraftEnv(vnc_env.VNCEnv):
    safe_action_space = spaces.Hardcoded(
        spaces.KeyEvent(vnc_event.keycode(x)) for x in [c for c in string.printable] + [

            # TODO: enable these once we're sure they only get sent to the starcraft window
            # 'f2',  # Map positions
            # 'f3',  # Map positions
            # 'f4',  # Map positions
            # 'tab',
            # 'shift',
            # 'ctrl',
            # 'ctrl',
            # 'alt',
            # 'space',

            'left',
            'up',
            'right',
            'down']
    )

# TODO: enable these once we're sure they only get sent to the starcraft window
#     We only allow keyboard inputs used by StarCraft:
#     http://gamingweapons.com/image/steelseries/zboard-starcraft2-keyset/steelseries_zboard_starcraft2_keyset_02.jpg
#     """
#     _screen_dimensions = (480, 640)
#     _x_offset = 5  # Centered
#     _y_offset = 30  # Remove the chrome
#
#     @classmethod
#     def _safe_pointer_event(cls, event):
#         """Returns true if the click is in a place that will not break out of the box"""
#         height = cls._screen_dimensions[0]
#         width = cls._screen_dimensions[1]
#         margin = 5  # Never allow clicking within 5 pixels of the edge of the screen
#
#         unsafe_locations = [
#             (event.y < cls._y_offset + margin),  # At the top, where menu chrome is
#             (event.y > height + cls._y_offset - margin),  # Too far down
#             (event.x < cls._x_offset + margin),  # Too far left
#             (event.x > width + cls._x_offset - margin),  # Too far right
#             (410 < event.x < 510) and (370 < event.y < 450),  # Where the menu button is
#         ]
#         return not any(unsafe_locations)
