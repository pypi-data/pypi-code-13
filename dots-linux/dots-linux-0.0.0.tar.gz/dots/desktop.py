import subprocess, json

from .shell import Shell


class Desktop:

    def __init__(self):
        """An interface to the Linux command-line utility `xdotool` to provide
        utilities for the Xorg-desktop.
        """
        pass

    def snapshot(self):
        self.desktops = {}
        self.populate_desktops()
        self.dump()

    def dump(self):
        from os import path
        cfg_file = path.expanduser('~/.config/dots/desktops.json')

        with open(cfg_file, 'w+') as stream:
            json.dump(obj=self.desktops, fp=stream, indent=4)

    def populate_desktops(self):
        windows = []
        window_ids = Desktop.window_ids()
        for id in window_ids:
            window = {
                'title': None,
                'position': {
                    'x': None,
                    'y': None
                },
                'dimensions': {
                    'w': None,
                    'h': None
                }
            }

            title = Desktop.window_title(id)
            geometry = Desktop.window_geometry(id)
            x, y = Desktop.window_position(geometry)
            w, h = Desktop.window_dimensions(geometry)

            for key in window:
                if key in vars():
                    window[key] = locals()[key]
                elif type(window[key]) is dict:
                    for _key in window[key]:
                        if _key in vars():
                            window[key][_key] = locals()[_key]

            desktop = Desktop.window_desktop(id)
            if desktop not in self.desktops:
                self.desktops[desktop] = []
            self.desktops[desktop].append(window)

    @classmethod
    def virtual_desktops(cls):
        """Provides a count and range for the number of virtual-desktops in the
        current Xorg-environment.

        Additionally determines the lower/upper-bounds to return in the range.

        Returns:
            desktops (int): A natural-number representation of the number of
                virtual desktops available.
            desktops_range (range): A determinable python-range which represents
                the computer's counting of the desktops.
        """

        desktops = Shell.check_output('xdotool get_num_desktops')
        desktops = int(desktops)

        desktop_zero_start = Shell.check_output(
            'xdotool search --desktop 0 --name ".*"')
        if desktop_zero_start:
            desktops_range = range(desktops)
        else:
            desktops_range = range(1, desktops + 1)

        return (desktops, desktops_range)

    @classmethod
    def window_title(cls, id):
        return Shell.check_output('xdotool getwindowname {}'.format(id))

    @classmethod
    def window_desktop(cls, id):
        return Shell.check_output('xdotool get_desktop_for_window {}'.format(
            id))

    @classmethod
    def window_geometry(cls, id):
        return Shell.check_output('xdotool getwindowgeometry {}'.format(id))

    @classmethod
    def window_ids(cls):
        """Returns a list of all windows available while also filtering empty
        desktops.

        Returns:
            window_ids (list)"""

        ids = []
        _, desktops_range = cls.virtual_desktops()
        for desktop in desktops_range:
            desktop_windows = Shell.check_output(
                'xdotool search --desktop {} --name ".*"'.format(desktop))
            if desktop_windows:    # Returns False if the desktop has no windows
                for id in desktop_windows:
                    ids.append(id)
        return ids

    @classmethod
    def window_position(cls, geometry):
        x, y = geometry[1].replace('Position: ', '').replace(' (screen: 0)', '') \
            .split(',')
        return (x, y)

    @classmethod
    def window_dimensions(cls, geometry):
        w, h = geometry[2].replace('Geometry: ', '').split('x')
        return (w, h)

    def help(self):
        # Parse desktop geometry
        store = {}
        for window in window_details:
            w = {'id': None, 'position': None, 'geometry': None, 'title': None}

            # Storage
            #
            vs = [var for var in vars()]
            for var in vs:
                if var in w:
                    w[var] = locals()[var]
            desktop = call('xdotool get_desktop_for_window {}'.format(id))[0]
            if desktop not in store:
                store[desktop] = []
            store[desktop].append(w)
