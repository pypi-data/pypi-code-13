# coding=UTF-8
"""
Intro and usage
===================
Pykkar is a virtual robot living in a virtual world. It can step, turn 90 degrees right,
paint floor tiles, take and put down traffic cones and push boxes. It can detect
whether there is a wall or other obstacle ahead or whether it's standing on a painted
tile. It can be commanded by Python code (either procedural or OOP style)

Pykkar's world can be created by a call to ``create_world`` (when using procedural style)
or by instantiating class ``World`` (OOP style). Both take single argument, which is
a string representation of the world. Lines in the string represent the rows in the world
map. Each character represents one tile. Meaning of characters:

#                    wall
<space>              plain floor
.                    painted floor
b                    box on plain floor
B                    box on painted floor
^ > v <              pykkar on plain floor without cone 
                     (caret, greater-than, lowercase v, less-than)
N E S W              pykkar on painted floor without cone
1 2 3 4 5 6 7 8 9    cone stack on plain floor
C                    single cone on painted floor

Sample:

    create_world('''
    ####
    #> #
    # 3#
    ####
    ''')

this creates a world where 2x2 floor are is padded with walls. Pykkar is in north-west
corner of the floor, looking east and in south-east corner there is a stack of 3 traffic
cones.

In procedural style, Pykkar can be commanded by calling global functions defined in this 
module (eg. ``step()``, ``right()``, etc). There are also functions for querying the 
world (``is_wall()``, ``is_box()``, etc). New compound commands can be defined by defining 
new functions in client module.

In OOP style, Pykkar is represented by a separate object of class ``Pykkar``. In the
start of the program, client code is supposed to create new world (eg. ``w = World(layout)``)
and a Pykkar living in that world (eg ``p = Pykkar(w)``). Commands are given by calling 
the methods of Pykkar object. New commands should be defined by subclassing ``Pykkar``. 
"""

"""
Technical stuff
================
In order to reserve the main thread for executing commands (this way respective function calls
can be written in client module's toplevel), tkinter window must run in a different thread. 
Unfortunately, tkinter runs reliably only in the main thread of the process. 
For this reason the execution is divided into 2 processes: the "main" process, 
which is just a shallow command proxy and the child process, which runs actual program 
logic and presents the world state in a tkinter window.

Main process (ie. user module) normally begins by creating the world (with either 
``create_world(...)`` or ``World(...)``). This spawns a child process which creates
tkinter window representing the world. Main process then continues by executing
user-provided function/method calls, which amounts to writing respective command strings
to child process' stdin and reading results back from child process' stdout.

Main player in child process is an object of class ``_WorldProper``. It keeps the 
data structures about world layout, responds to commands that alter the world state and runs 
a tkinter window. It reads periodically next command from stdin, acts upon it and writes 
result (may be None) to stdout.

NB! as stdout from tkinter process is parsed, you can't just print out debug information
to sys.stdout. Use sys.stderr instead!

Reading from stdin blocks, as usual. This would make window temporariliy unresponsive 
when commands are given interactively (including stepping in a debugger). One case, where
this can be annoying is when pykkar is run in a debugger and user wants to move the window.
For this reason, the child process is divided into 2 threads. Main thread runs tkinter
mainloop, and secondary thread takes care of stding and stdout. They communicate via
two Queues (see _WorldProper.execute and _WordProper._process_commands).


Creating new bitmaps
========================
TODO
    * embed base gif-s as base64 strings
        * http://effbot.org/tkinterbook/photoimage.htm
        * http://effbot.org/librarybook/base64.htm
        * http://www.tcl.tk/man/tcl8.4/TkCmd/photo.htm#M17
    * load user provided gif-s, when present

"""

import sys
import subprocess
import os.path
import traceback
from threading import Thread

try: 
    import tkinter as tk # works in Python 3
except ImportError:
    import Tkinter as tk # works in Python 2

try: 
    from queue import Queue  # works in Python 3
except ImportError:
    from Queue import Queue # works in Python 2


N = (0,-1)
W = (-1,0)
E = (1,0)
S = (0,1)

class World():
    """ Object, which creates GUI and mediates commands and results
        between Pykkar and GUI"""
        
    # This is actually a proxy for the actual world (_WorldProper, 
    # which lives in another process)
    
    def __init__(self, layout_str):
        """ """
        self.proc = subprocess.Popen (
            (sys.executable, '-u', '-m', 'pykkar',  repr(layout_str)),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0
        )

        # Check initialization result
        result_str = self.proc.stdout.readline().decode()
        if result_str.strip() != "OK":
            raise RuntimeError("World creation failed: " + eval(result_str))

    def execute(self, command_str):
        if self.proc.poll() != None:
            return
        
        self.proc.stdin.write((command_str + "\n").encode())
        self.proc.stdin.flush()
        result_str = self.proc.stdout.readline().decode()
        if result_str == "":
            return
        
        result = eval(result_str)
        
        if isinstance(result, Exception):
            raise result
        else:
            return result

def create_world(layout_str):
    global world
    world = World(layout_str)

def step():
    world.execute("step")

def right():
    world.execute("right")
    
def take():
    world.execute("take")
    
def put():
    world.execute("put")
    
def push():
    world.execute("push")
    
def paint():
    world.execute("paint")
    
def get_heading():
    return world.execute("get_heading")
    
def get_direction():
    return world.execute("get_direction")
    
def get_speed():
    return world.execute("get_speed")
    
def set_speed(value):
    world.execute("set_speed " + str(value))
    
def is_wall():
    return world.execute("is_wall")        
        
def is_box():
    return world.execute("is_box")        
        
def is_cone():
    return world.execute("is_cone")        

def is_painted():
    return world.execute("is_painted")        


class Pykkar:
    """ Just a handle to the world, it passes all commands to its world """
    def __init__(self, world):
        self._world = world

    def step(self):
        self._world.execute("step")
    
    def right(self):
        self._world.execute("right")
        
    def take(self):
        self._world.execute("take")
        
    def put(self):
        self._world.execute("put")
        
    def push(self):
        self._world.execute("push")
        
    def paint(self):
        self._world.execute("paint")
        
    def get_heading(self):
        return self._world.execute("get_heading")
        
    def get_direction(self):
        return self._world.execute("get_direction")
        
    def get_speed(self):
        return self._world.execute("get_speed")
        
    def set_speed(self, value):
        self._world.execute("set_speed " + str(value))
        
    def is_wall(self):
        return self._world.execute("is_wall")        
            
    def is_box(self):
        return self._world.execute("is_box")        
            
    def is_cone(self):
        return self._world.execute("is_cone")       
    
    def is_painted(self):
        return self._world.execute("is_painted") 
            
    
class _WorldProper:
    _block_size = 32

    def __init__(self, layout_str):
        self._command_queue = Queue(maxsize=1)
        self._result_queue = Queue(maxsize=1)

        self._setup_layout(layout_str)
        self._setup_ui()
        self._speed = 5
        self.closed = False
        
        
    def run(self):
        try:
            self.root.after_idle(self._process_commands)
            self.root.mainloop()
        finally:
            # give a result in case there's a pending command from client
            self.closed = True
            if not self._command_queue.empty():
                self._result_queue.put(Exception("World has ended"), block=False)
    
        
    def execute(self, command_str):
        """ meant for calling by outsiders (from another thread) """
        
        if self.closed:
            # ignore command and return constant answer
            result = Exception("Window is closed")
        else:
            # put won't normally block, because commands are given and processed synchronously
            self._command_queue.put(command_str, block=False)
            # get blocks until mainloop handles the command
            result = self._result_queue.get()
        
        return result

    def _setup_layout(self, layout_str):
        self.layout = []
        self.px = None
        self.py = None
        lines = layout_str.strip("\r\n").split("\n")
        longest_row_width = 0
        
        for y in range(len(lines)):
            line = list(lines[y].strip("\r"))
            row = []
            for x in range(len(line)):
                code = line[x]
                tile = _Tile.create_from_code(code)
                
                if tile.pykkar_heading != None:
                    if self.px != None:
                        raise RuntimeError("Only one pykkar is allowed")
                    self.px = x
                    self.py = y
                
                row.append(tile)
                
            self.layout.append(row)
                
            longest_row_width = max(longest_row_width, len(row))
        
        if self.px == None:
            raise Exception("Pykkar is missing")
        
        # pad the layout
        for line in self.layout:
            # extend with floor in the right
            line.extend(list((longest_row_width - len(line)) * [_Tile('plain_floor')]))
        
             
        self.width = len(self.layout[0])
        self.height = len(self.layout)
        
    def _setup_ui(self):
        self.root = tk.Tk()
        self.root.title("Pykkar")
        self.px_width = self.width * _WorldProper._block_size
        self.px_height = self.height * _WorldProper._block_size
        self.root.geometry("%dx%d" % (self.px_width, self.px_height))
        self.root.resizable(0,0)
        self.canvas = tk.Canvas(self.root, 
                                width=self.px_width, 
                                height=self.px_height,
                                highlightthickness=0)
        self.canvas.grid()
        
        # load images
        self.images = {}
        for name in ('wall', 'box', 'cone', 'plain_floor', 'painted_floor',
                     'pykkar_n', 'pykkar_e', 'pykkar_s', 'pykkar_w',
                     'pykkar_n_cone', 'pykkar_e_cone', 'pykkar_s_cone', 'pykkar_w_cone'):
            self.images[name] = self._load_image(name)
        
        # draw tiles
        for y in range(len(self.layout)):
            row = self.layout[y]
            for x in range(len(row)):
                tile = row[x]
                
                # base image
                tile.base_image_id = self.canvas.create_image (
                    x * _WorldProper._block_size,
                    y * _WorldProper._block_size,
                    image=self.images[tile.base_kind], 
                    anchor=tk.NW
                )

                # item image
                if tile.item_kind != None and tile.pykkar_heading == None:
                    tile.item_image_id = self.canvas.create_image (
                        x * _WorldProper._block_size,
                        y * _WorldProper._block_size,
                        image=self.images[tile.item_kind], 
                        anchor=tk.NW
                    )
                    self._update_item_image(tile)
                
                # pykkar
                if tile.pykkar_heading != None:
                    self.pykkar_id = self.canvas.create_image (
                        self.px * _WorldProper._block_size,
                        self.py * _WorldProper._block_size,
                        image=self._get_pykkar_img(tile.pykkar_heading, tile.item_kind),
                        anchor=tk.NW
                    )
            # done with row
        # done with all rows            
                
        self.canvas.tag_raise(self.pykkar_id)
    
    def _load_image(self, name):
        filename = "./" + name + ".gif"
        if os.path.exists(filename):
            return tk.PhotoImage(file=filename)
        else:
            return tk.PhotoImage(data=_image_data[name])
    
    def _process_commands(self):
        """ is called periodically be WorldProper itself """
        delay = _WorldProper._delays[self._speed-1]
        
        if not self._command_queue.empty():
            try:
                command_str = self._command_queue.get()
                parts = command_str.strip().split()
                cmd = parts[0]
                args = tuple(parts[1:]) 
                # look up corresponding method
                f = getattr(self, "_cmd_" + cmd)
                result = f(*args)
                #self._result_queue.put(result, block=False)
                self._result_queue.put(result)
                
                # reduce delay for some commands
                if cmd in ['set_speed', 'get_speed']:
                    delay = 10 
                
            except BaseException as e:
                traceback.print_exc(file=sys.stderr)
                # no command may stay without result, otherwise client remains blocked
                self._result_queue.put(e)
        
        # schedule next processing
        self.root.after(delay, self._process_commands)
    
    def _cmd_get_x(self):
        return self.px
    
    def _cmd_get_y(self):
        return self.py
    
    def _cmd_is_wall(self):
        (next_x, next_y) = self._get_next_pos()
        # wall means either actuall wall block or outside of window
        return not self._is_valid_pos(next_x, next_y) \
            or self.layout[next_y][next_x].base_kind == 'wall' 
    
    def _cmd_is_box(self):
        return self._is_item("box")
    
    def _cmd_is_cone(self):
        return self._is_item("cone")
    
    def _cmd_is_painted(self):
        return self._get_current_tile().base_kind == 'painted_floor'
    
    def _is_item(self, item_kind):
        (next_x, next_y) = self._get_next_pos()
        return self._is_valid_pos(next_x, next_y) \
            and self.layout[next_y][next_x].item_kind == item_kind
    
    def _cmd_step(self):
        (next_x, next_y) = self._get_next_pos()
        next_tile = self.layout[next_y][next_x]
        if not self._is_valid_pos(next_x, next_y) \
                or next_tile.base_kind not in ('plain_floor', 'painted_floor') \
                or next_tile.item_kind != None:
            raise Exception("Can't go to (%d,%d)" % (next_x, next_y))
        
        current_tile = self._get_current_tile()
        next_tile.pykkar_heading = current_tile.pykkar_heading
        next_tile.item_kind = current_tile.item_kind
        next_tile.item_count = current_tile.item_count
        
        current_tile.pykkar_heading = None
        current_tile.item_kind = None
        current_tile.item_count = None
        
        # move pykkar image
        self.canvas.coords(self.pykkar_id, 
                           next_x * _WorldProper._block_size,
                           next_y * _WorldProper._block_size)
        
        # update current position
        self.px = next_x
        self.py = next_y
        
    def _cmd_right(self):
        headings = (N,E,S,W)
        cur_tile = self._get_current_tile() 
        
        cur_heading_index = headings.index(cur_tile.pykkar_heading)
        new_heading_index = (cur_heading_index + 1) % 4
        cur_tile.pykkar_heading = headings[new_heading_index]
        
        self._update_pykkar_image(cur_tile)
    
    def _cmd_with_cone(self):
        tile = self._get_current_tile()
        return tile.item_kind == 'cone'
    
    def _cmd_take(self):
        cur_tile  = self._get_current_tile()
        next_tile = self._get_next_tile()
        
        if cur_tile.item_kind != None:
            raise Exception("Pykkar already carries something")
        
        if next_tile.item_kind != 'cone':
            raise Exception("Pykkar can take only cones")
        
        cur_tile.item_kind = next_tile.item_kind
        cur_tile.item_count = 1
        next_tile.item_count -= 1
        if next_tile.item_count == 0:
            next_tile.item_kind = None
            next_tile.item_count = None
        
        self._update_pykkar_image(cur_tile)
        self._update_item_image(next_tile)
    
    def _cmd_put(self):
        cur_tile  = self._get_current_tile()
        next_tile = self._get_next_tile()
        
        if cur_tile.item_kind == None:
            raise Exception("Not carrying anything")
        
        if next_tile.base_kind not in ['plain_floor', 'painted_floor'] \
            or (next_tile.item_kind != cur_tile.item_kind \
                and next_tile.item_kind != None):
            raise Exception("Can't put it there")
        
        if cur_tile.item_kind != 'cone' and next_tile.item_kind != None:
            raise Exception("There is one already")
            
        if cur_tile.item_kind == 'cone' and next_tile.item_count == 9:
            raise Exception("Can't stack more than 9 cones")
            
        
        next_tile.item_kind = cur_tile.item_kind
        next_tile.item_count = 1 if next_tile.item_count == None else next_tile.item_count + 1
        
        cur_tile.item_kind = None
        cur_tile.item_count = None
        
        self._update_pykkar_image(cur_tile)
        self._update_item_image(next_tile)
    
    def _cmd_push(self):
        if self._cmd_with_cone():
            raise Exception("Can't push when carrying something")
        
        (next_x, next_y) = self._get_next_pos()
        if not self._is_valid_pos(next_x, next_y):
            raise Exception("Nothing to push")
        
        cur_tile  = self._get_current_tile()
        next_tile = self._get_next_tile()
        
        if next_tile.item_kind == None:
            raise Exception("Nothing to push")
            
        
        next_next_x = self.px + (cur_tile.pykkar_heading[0]*2)
        next_next_y = self.py + (cur_tile.pykkar_heading[1]*2)
        if not self._is_valid_pos(next_next_x, next_next_y):
            raise Exception("Nowhere to push")
        
        next_next_tile = self.layout[next_next_y][next_next_x]
        
        if next_next_tile.base_kind not in ['plain_floor', 'painted_floor']:
            raise Exception("Nowhere to push")
            
        if next_next_tile.item_kind != None:
            raise Exception("No room to push")
        
        # move item
        next_next_tile.item_kind = next_tile.item_kind
        next_next_tile.item_count = next_tile.item_count
        next_tile.item_kind = None
        next_tile.item_count = None
        
        self._update_item_image(next_tile)
        self._update_item_image(next_next_tile)
        
        # move pykkar
        self._cmd_step()
        
    def _cmd_paint(self):
        tile = self._get_current_tile()
        if tile.item_kind != None:
            raise Exception("Can't paint when carrying something")
        
        self.canvas.itemconfig(tile.base_image_id, image=self.images['painted_floor'])
        tile.base_kind = 'painted_floor'
    
    def _cmd_get_heading(self):
        return self._get_current_tile().pykkar_heading
    
    def _cmd_get_direction(self):
        heading = self._cmd_get_heading()
        if heading == N:
            return "N"
        elif heading == E:
            return "E"
        elif heading == S:
            return "S"
        else:
            assert heading == W
            return "W"
    
    def _cmd_set_speed(self, value):
        self._speed = int(value)

    def _cmd_get_speed(self):
        return self._speed

    def _get_current_tile(self):
        return self.layout[self.py][self.px]
    
    def _get_next_tile(self):
        (next_x, next_y) = self._get_next_pos()
        if not self._is_valid_pos(next_x, next_y):
            raise Exception("Not valid position")
        
        return self.layout[next_y][next_x]
    
    def _get_next_pos(self):
        tile = self._get_current_tile() 
        next_x = self.px + tile.pykkar_heading[0]
        next_y = self.py + tile.pykkar_heading[1]
        return (next_x, next_y)
    
    def _is_valid_pos(self, x, y):
        return  x >= 0 and x < self.width \
            and y >= 0 and y < self.height
    
    
    def _update_pykkar_image(self, tile):
        new_image = self._get_pykkar_img(tile.pykkar_heading,
                                         tile.item_kind)
        
        self.canvas.itemconfig(self.pykkar_id, image=new_image)
    
    def _get_tile_pos(self, tile):
        for y in range(self.height):
            for x in range(self.width):
                if self.layout[y][x] is tile:
                    return (x, y)
    
    def _update_item_image(self, tile):
        (x, y) = self._get_tile_pos(tile)
        
        # update image
        if tile.item_kind == None:
            #if tile.item_image_id != None:
                self.canvas.delete(tile.item_image_id)
        else:
            img = self.images[tile.item_kind]
            if tile.item_image_id == None:
                tile.item_image_id = self.canvas.create_image(
                    x * _WorldProper._block_size,
                    y * _WorldProper._block_size,
                    image=img,
                    anchor=tk.NW
                )
            else:
                self.canvas.itemconfig(tile.item_image_id, image=img)
        
        # update count text
        if tile.item_count == None or tile.item_count <= 1:
            if tile.text_id != None:   
                self.canvas.delete(tile.text_id)
        else:
            if tile.text_id == None:
                tile.text_id = self.canvas.create_text (
                    x * _WorldProper._block_size+3,
                    y * _WorldProper._block_size+1,
                    text=str(tile.item_count),
                    anchor=tk.NW
                )
            else:
                self.canvas.itemconfig(tile.text_id, text=str(tile.item_count))
            
    
    def _get_pykkar_img(self, heading, item_kind):
        img_name = "pykkar"
        if   heading == N: img_name += '_n'
        elif heading == E: img_name += '_e'
        elif heading == S: img_name += '_s'
        else:              img_name += '_w'
        
        if item_kind != None:
            img_name += '_' + item_kind
        
        return self.images[img_name]
    
    _delays = (500, 300, 200, 150, 100, 75, 50, 30, 25, 20) 
    
class _CmdBroker(Thread):
    """ Mediates between stdin/stdout/stderr and World""" 
    def __init__(self, world_proper):
        Thread.__init__(self)
        self.world_proper = world_proper
    
    def run(self):
        while True:
            command_str = sys.stdin.readline()
            if command_str == "": # client finished
                break
            
            result = self.world_proper.execute(command_str.strip())
            print(repr(result))

class _Tile:
    
    @staticmethod
    def create_from_code(code):
        proto = _content_codes[code]
        return _Tile(proto.base_kind, proto.pykkar_heading, proto.item_kind, proto.item_count)
        
    
    def __init__(self, base_kind, pykkar_heading=None, item_kind=None, item_count=None):
        self.base_kind = base_kind
        self.pykkar_heading = pykkar_heading
        self.item_kind = item_kind
        self.item_count = item_count
        self.base_image_id = None
        self.item_image_id = None
        self.text_id = None
    
    def __eq__(self, other):
        return  self.base_kind == other.base_kind \
            and self.pykkar_heading == other.pykkar_heading \
            and self.item_kind == other.item_kind \
            and self.item_count == other.item_count
            
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __str__(self):
        return self.get_content_code()
                
    def get_content_code(self):
        for key in _content_codes:
            if _content_codes[key] == self:
                return key
            
        raise LookupError("No code found")
        
_content_codes = {
    '#' : _Tile('wall'),
    ' ' : _Tile('plain_floor'),
    '.' : _Tile('painted_floor'),
    
    'b' : _Tile('plain_floor', None, 'box', 1),
    'B' : _Tile('painted_floor', None, 'box', 1),
    
    '^' : _Tile('plain_floor', N),
    '>' : _Tile('plain_floor', E),
    'v' : _Tile('plain_floor', S),
    '<' : _Tile('plain_floor', W),
    
    'N' : _Tile('painted_floor', N),
    'E' : _Tile('painted_floor', E),
    'S' : _Tile('painted_floor', S),
    'W' : _Tile('painted_floor', W),
    
    
    '1' : _Tile('plain_floor', None, 'cone', 1),
    '2' : _Tile('plain_floor', None, 'cone', 2),
    '3' : _Tile('plain_floor', None, 'cone', 3),
    '4' : _Tile('plain_floor', None, 'cone', 4),
    '5' : _Tile('plain_floor', None, 'cone', 5),
    '6' : _Tile('plain_floor', None, 'cone', 6),
    '7' : _Tile('plain_floor', None, 'cone', 7),
    '8' : _Tile('plain_floor', None, 'cone', 8),
    '9' : _Tile('plain_floor', None, 'cone', 9),
    
    'C' : _Tile('painted_floor', None, 'cone', 1),
} 


_image_data = {
    'box' : """
        R0lGODlhIAAgALMAAAAAAMxVAMyAAP+AAP+qM/+qZv/VM//VZv/Vmf/VzP//mf//zP////
        ///////////yH5BAEAAA8ALAAAAAAgACAAAwT/8MlJq70V6M27/5oEIEhClqdJquiaEoCY
        GAVx1LdNFMfeFzRgQSiIPUa1JG2H2zGXylpRZhMIBtZrFmvlagXMgRFJKILOmsVuekTcxF
        aAl0svxt3lMUIqLyAAX1laSGJ7BWwAM4eAO38CSU4FAGqLCjViInt5jz0JgENBZGZ7B4iK
        Yp+NAD8winaienxFAz8KADywWEiLIpaLugE/f4k0dot4mG1AdlepB39rfXkJ0VS/j8Y1ns
        Y0hcWxm2A1gEsL0nwJfDLdcgI9BxrBqjjH7JmyAUMjszh/SUWGELm5BsOXsR22vuERKKsI
        tUUH/dxyWO2IKzkjvg3Y8enGH28FWZLBSjTE2DtGPGCQzJPpDaM8A6BwfBQNwbd7m3QJ6h
        LnC6x1i9Cc8SVSUwEFJlQoTeECxbJYrIRIDbLkR1SGPiLJlOrkRxBEh3byFORl7JYxQtN6
        wMC2rYUIADs=""",
    'cone' : """
        R0lGODlhIAAgALMAAOyVC/n5+f////T09AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAACH5BAEAAAIALAAAAAAgACAAAwRTUMhJq7046827/2AoTgAwbqV5Xqm6Vu1r
        ta5M128Z7KUsAbsgbnRL2YpDENJ4AgafPaLzKUxylrEQlqbUUb9WjPdLjV63yAx6Hfa53/
        C4fE6fRwAAOw==""",
    'painted_floor' : """
        R0lGODlhIAAgAPcAAAAAAAAABgAAHQAATAAAlgAA/wAEAAAEBgAEHQAETAAElgAE/wATAA
        ATBgATHQATTAATlgAT/wAxAAAxBgAxHQAxTAAxlgAx/wBhAABhBgBhHQBhTABhlgBh/wCm
        AACmBgCmHQCmTACmlgCm/wD/AAD/BgD/HQD/TAD/lgD//wYAAAYABgYAHQYATAYAlgYA/w
        YEAAYEBgYEHQYETAYElgYE/wYTAAYTBgYTHQYTTAYTlgYT/wYxAAYxBgYxHQYxTAYxlgYx
        /wZhAAZhBgZhHQZhTAZhlgZh/wamAAamBgamHQamTAamlgam/wb/AAb/Bgb/HQb/TAb/lg
        b//x0AAB0ABh0AHR0ATB0Alh0A/x0EAB0EBh0EHR0ETB0Elh0E/x0TAB0TBh0THR0TTB0T
        lh0T/x0xAB0xBh0xHR0xTB0xlh0x/x1hAB1hBh1hHR1hTB1hlh1h/x2mAB2mBh2mHR2mTB
        2mlh2m/x3/AB3/Bh3/HR3/TB3/lh3//0wAAEwABkwAHUwATEwAlkwA/0wEAEwEBkwEHUwE
        TEwElkwE/0wTAEwTBkwTHUwTTEwTlkwT/0wxAEwxBkwxHUwxTEwxlkwx/0xhAExhBkxhHU
        xhTExhlkxh/0ymAEymBkymHUymTEymlkym/0z/AEz/Bkz/HUz/TEz/lkz//5YAAJYABpYA
        HZYATJYAlpYA/5YEAJYEBpYEHZYETJYElpYE/5YTAJYTBpYTHZYTTJYTlpYT/5YxAJYxBp
        YxHZYxTJYxlpYx/5ZhAJZhBpZhHZZhTJZhlpZh/5amAJamBpamHZamTJamlpam/5b/AJb/
        Bpb/HZb/TJb/lpb///8AAP8ABv8AHf8ATP8Alv8A//8EAP8EBv8EHf8ETP8Elv8E//8TAP
        8TBv8THf8TTP8Tlv8T//8xAP8xBv8xHf8xTP8xlv8x//9hAP9hBv9hHf9hTP9hlv9h//+m
        AP+mBv+mHf+mTP+mlv///////////////////////////////////////////yH5BAAAAA
        AALAAAAAAgACAABwj/AAEoS0aPYLJkwxAWVDaP4cCCBRFKhAggWcODBjFaTDZwXsaMDA8+
        5OhxYcOGJjkmHHbxJMeCJUmGdLjSoMeBDg3OvHiwZsSbN0lm/NlxZNCIJh0CVSkx50WcHi
        UK7WnR6MGlDE+OtLm1qMyRTr1qlWkwZUiiG5OK9NiSY9qqVT3WtEk1YU6IOumtxOk24kiz
        WON2pIsXr9CQEhOSbdk1qNaLEWVGVXuxJmSMO0NeHirUpE+4C93OdXo4KMaUMMe6bOryLO
        eBOjeCXSp59mDAO0vDzj3QLmjdOiuzLh23LmnNGZfC5Iv4qmSSl++uzfrXKFRliJEeXO72
        8tPiifuGRh+mOWzdzTDJducbk+v2q7PfM274mSfS7GS5R4UqPmLCm6MFJZ12UuWEHFftrU
        SPasQd5dVW2nlFID0ArKYdVkBJ+B4AAQEAOw==""",
    'plain_floor' : """
        R0lGODlhIAAgAOf1AAAAAAAAMwAAZgAAmQAAzAAA/wArAAArMwArZgArmQArzAAr/wBVAA
        BVMwBVZgBVmQBVzABV/wCAAACAMwCAZgCAmQCAzACA/wCqAACqMwCqZgCqmQCqzACq/wDV
        AADVMwDVZgDVmQDVzADV/wD/AAD/MwD/ZgD/mQD/zAD//zMAADMAMzMAZjMAmTMAzDMA/z
        MrADMrMzMrZjMrmTMrzDMr/zNVADNVMzNVZjNVmTNVzDNV/zOAADOAMzOAZjOAmTOAzDOA
        /zOqADOqMzOqZjOqmTOqzDOq/zPVADPVMzPVZjPVmTPVzDPV/zP/ADP/MzP/ZjP/mTP/zD
        P//2YAAGYAM2YAZmYAmWYAzGYA/2YrAGYrM2YrZmYrmWYrzGYr/2ZVAGZVM2ZVZmZVmWZV
        zGZV/2aAAGaAM2aAZmaAmWaAzGaA/2aqAGaqM2aqZmaqmWaqzGaq/2bVAGbVM2bVZmbVmW
        bVzGbV/2b/AGb/M2b/Zmb/mWb/zGb//5kAAJkAM5kAZpkAmZkAzJkA/5krAJkrM5krZpkr
        mZkrzJkr/5lVAJlVM5lVZplVmZlVzJlV/5mAAJmAM5mAZpmAmZmAzJmA/5mqAJmqM5mqZp
        mqmZmqzJmq/5nVAJnVM5nVZpnVmZnVzJnV/5n/AJn/M5n/Zpn/mZn/zJn//8wAAMwAM8wA
        ZswAmcwAzMwA/8wrAMwrM8wrZswrmcwrzMwr/8xVAMxVM8xVZsxVmcxVzMxV/8yAAMyAM8
        yAZsyAmcyAzMyA/8yqAMyqM8yqZsyqmcyqzMyq/8zVAMzVM8zVZszVmczVzMzV/8z/AMz/
        M8z/Zsz/mcz/zMz///8AAP8AM/8AZv8Amf8AzP8A//8rAP8rM/8rZv8rmf8rzP8r//9VAP
        9VM/9VZv9Vmf9VzP9V//+AAP+AM/+AZv+Amf+AzP+A//+qAP+qM/+qZv+qmf+qzP+q///V
        AP/VM//VZv/Vmf/VzP///////////////////////////////////////////yH+EUNyZW
        F0ZWQgd2l0aCBHSU1QACwAAAAAIAAgAAAI/gABKEtGj2CyZMMQFlQ2j+HAggURSoQIIFnD
        gwYxWkw2cF7GjAwPPuTocWHDhiY5Jhx28STHgiVJhnS40qDHgQ4Nzrx4sGbEmzdJZvzZcW
        TQiCYdAlUpMedFnB4lCu1p0ejBpQxPjrS5tajMkU69apVpMGVIohuTivTYkmPaqlU91rRJ
        NWFOiDrprcTpNuJIs1jjdqSLF6/QkBITkm3ZNajWixFlRlV7sSZkjDtDXh4q1KRPuAvdzn
        V6OCjGlDDHumzq8izngTo3gl0qefZgwDtLw8490C5o3Torsy4dty5pzRmXwuSL+Kpkkpfv
        rs361yhUZYiRHlzu9vLT4on7R4Yfpjls3c0wyXbnG5Pr9quz3zNu+Jkn0uxkuUeFKj5iwp
        ujBSWddlLlhBxX7a1Ej2rEHeXVVtp5RSA9AKymHVZASfgeAAEBADs=""",
    'pykkar_e' : """
        R0lGODlhIAAgALMAAAAAAJ83G8febf///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAACH5BAEAAAMALAAAAAAgACAAAwSMcMhJq7046827/6AWjKRXXmRaAagqAXCc
        sVY6DrGgCzIFiyTAbriL/X4bGHFJm/QsyqW0mRRKr1SMFWsscrY8Y5TnTV7JRWv2Aia21d
        8zOLqGytNlTXu47ddXezpdeU5sOWeESDNjWDhPFTYvgWEsipCRkkyAGJiSMS5Ofxw2AZsh
        pCGpqqusra6vFREAOw==""",
    'pykkar_e_cone' : """
        R0lGODlhIAAgALMAAAAAAJ83Gw2VC8l/CeyVC8febfT09PT09AAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAACH5BAEAAAIALAAAAAAgACAAAwS2UMhJq7046827H14oDaQVnKiHDkQ5oXAF
        XDDbDkCeZ7NZE0BSYaiT9TArIMFAGgyJutluY1sym8+jpHjJVQ0GpZDoyRW+YeDVWdBiAE
        +0EnzDceBDuTrdBGnwZ3NpVnt1PHGCiVZNf4iFj2Auh3mKhEuSk4GPliRuXXh6i06engI6
        oWNtFFMZcqlkUUhJaq9QUqUCMAFVtaqruD83UQAxv1QtPsUTrBeYEroBIiPS1NXW19jZGh
        EAOw==""",
    'pykkar_n' : """
        R0lGODlhIAAgALMAAAAAAJ83G8febf///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAACH5BAEAAAMALAAAAAAgACAAAwSecMhJq724grxp59N3fYCIbWU2pKkammPr
        SnA8a3PtdmXfh7dAgLYSGI8CX2eYEdIAyOhxI2RenEVkTwqoNofQaSkZRnoxznJSqxacr4
        HxlKvFotvt9XRgPUXlc3s5XEpqOhp0UkYyKoCLimQ3NH+QhyOUXJIeZXlJmnxCnWJvX2mQ
        nqRoXo5aoH2qWJ0pqaqbhRK0aJqvn72+v8DBwBEAOw==""",
    'pykkar_n_cone' : """
        R0lGODlhIAAgALMAAAAAAJ83Gw2VC8l/CeyVC8febfT09PT09AAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAACH5BAEAAAIALAAAAAAgACAAAwS5UMhJq724grxp59N3fYCIbWUmpKkamoNV
        mio9xB7tivftuSNJaUDokYCCQEC4KtwM0Nuss8wohYCCcwCNagsbZfVybW4J6PTgCxBbl1
        ktMa3+FtyYa/zZ7a+1eGQBJVt9hn9gZXl7dI1of2E7Z450kEhZN5SNazoyfIagUkifoKE4
        KpmamqcYqaqrqK+yrBQ9tre4uW96dr1hirtwcb1gScB5eMN2KYEqwFNTEs3OSNLV19jZ2t
        vc2REAOw==""",
    'pykkar_s' : """
        R0lGODlhIAAgALMAAAAAAJ83G8febf///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAACH5BAEAAAMALAAAAAAgACAAAwSZcMhJq7046827/2DwiV1gSkCqptTJmWIq
        zLQASDCpwQNQ16zc6+T70W7CDUxmPPI+xV+UBeo1o7MbtGmTQrFAqXbDvBrHGuxKde6oxd
        6d9XiW6i6mtxQIcOFNcHRHA34WMGc+bIOFFUuIYFqMLURcfDh3higrVz2XbhNrKihVnWRV
        VKYeomRoaTeoFyytsWOzFLWpoBm2pCARADs=""",
    'pykkar_s_cone' : """
        R0lGODlhIAAgALMAAAAAAJ83Gw2VC8l/CeyVC8febfT09PT09AAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAACH5BAEAAAIALAAAAAAgACAAAwS8UMhJq7046827/2DwiV1gSkCqptTJmWJa
        zHQBSDCpwQJQ16zc6+T70W5CzGDJbDqfTSVhSq1arwPN4MrFZrXd8JKzNJjP6PSYAyin34
        bljV3YhqdLW6doFw/0Oz0zfV1/NjoXJkV1cGZ5KS6JJjQDjXl6kRYwNYRUhpiIFTCLnQSX
        c5miRJRop6ihoigqbnF/N697E21Lpiw9ICgUUbrAvhNrFHN7xscVzBosz863bMrKF9Yb17
        8Y28DfAhEAOw==""",
    'pykkar_w' : """
        R0lGODlhIAAgALMAAAAAAJ83G8febf///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAACH5BAEAAAMALAAAAAAgACAAAwSJcMhJq7046827/2AIBmQpAkBVmuKAqiUq
        U2uAvRQg7Dw+1LbLS8YrCnC120xnNM40PldzKktZrLlidXrEZlC9MNd76zGP3COHCRZT17
        tzPE0WxuVyJ3x+r+L3XUR0gGladWWFZkpkeU1RSi5bdCtQjG19P0lXX34TmhVkQEEWLBxA
        LaipqqusIREAOw==""",
    'pykkar_w_cone' : """
        R0lGODlhIAAgALMAAAAAAJ83Gw2VC8l/CeyVC8febfT09PT09AAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAACH5BAEAAAIALAAAAAAgACAAAwS4UMhJq7046827/6A3hEJgntYwZgBQnWg1
        ECvrUnCrqwQNY60KoEAs8noDWADo0hWNA0PPF7Poms8CzyBFboKTIfFI4E4HusuNMlSZe2
        8aEawBHOPxQXGdccO7ZYB6cxtuXXiCexoqUYeAeYoYjIF/U5CEi5OUlUiRdZOIZ54sY36c
        cnRfUJaCqWyuYlqMeRxBV7GyUWdVanwCTqW7P1Y2OzNUJmovSksTPEnJHcwpKiQdNdbZ2t
        vZEQA7""",
    'wall' : """
        R0lGODlhIAAgAIQAAAAAAGpsN2tVRWBgYHNzcwFhuCiX/owtALplDZlvQNl8ALqOV6quYv
        +1Us/RbYSEhJaWlrmoktWWhsa9lN+uot7Wrf/aqOvnkv//hMDAwMbGxtjY2AAAAAAAAAAA
        AAAAACH/C05FVFNDQVBFMi4wAwEAAAAh+QQAZAAAACwAAAAAIAAgAIcAAAAAADMAAGYAAJ
        kAAMwAAP8AKwAAKzMAK2YAK5kAK8wAK/8AVQAAVTMAVWYAVZkAVcwAVf8AgAAAgDMAgGYA
        gJkAgMwAgP8AqgAAqjMAqmYAqpkAqswAqv8A1QAA1TMA1WYA1ZkA1cwA1f8A/wAA/zMA/2
        YA/5kA/8wA//8zAAAzADMzAGYzAJkzAMwzAP8zKwAzKzMzK2YzK5kzK8wzK/8zVQAzVTMz
        VWYzVZkzVcwzVf8zgAAzgDMzgGYzgJkzgMwzgP8zqgAzqjMzqmYzqpkzqswzqv8z1QAz1T
        Mz1WYz1Zkz1cwz1f8z/wAz/zMz/2Yz/5kz/8wz//9mAABmADNmAGZmAJlmAMxmAP9mKwBm
        KzNmK2ZmK5lmK8xmK/9mVQBmVTNmVWZmVZlmVcxmVf9mgABmgDNmgGZmgJlmgMxmgP9mqg
        BmqjNmqmZmqplmqsxmqv9m1QBm1TNm1WZm1Zlm1cxm1f9m/wBm/zNm/2Zm/5lm/8xm//+Z
        AACZADOZAGaZAJmZAMyZAP+ZKwCZKzOZK2aZK5mZK8yZK/+ZVQCZVTOZVWaZVZmZVcyZVf
        +ZgACZgDOZgGaZgJmZgMyZgP+ZqgCZqjOZqmaZqpmZqsyZqv+Z1QCZ1TOZ1WaZ1ZmZ1cyZ
        1f+Z/wCZ/zOZ/2aZ/5mZ/8yZ///MAADMADPMAGbMAJnMAMzMAP/MKwDMKzPMK2bMK5nMK8
        zMK//MVQDMVTPMVWbMVZnMVczMVf/MgADMgDPMgGbMgJnMgMzMgP/MqgDMqjPMqmbMqpnM
        qszMqv/M1QDM1TPM1WbM1ZnM1czM1f/M/wDM/zPM/2bM/5nM/8zM////AAD/ADP/AGb/AJ
        n/AMz/AP//KwD/KzP/K2b/K5n/K8z/K///VQD/VTP/VWb/VZn/Vcz/Vf//gAD/gDP/gGb/
        gJn/gMz/gP//qgD/qjP/qmb/qpn/qsz/qv//1QD/1TP/1Wb/1Zn/1cz/1f///wD//zP//2
        b//5n//8z///8AAAAAAAAAAAAAAAAI/wABAECjbBKaSWIATFJ28GDCgQUdKmRoEOHEimgS
        EsSYcCFHiB8pNuxY0WBCkSYVlsy48CBCMQnFjOxI8WXMmQoPZrrxUGBGmR1d9ug5EGZGAD
        DF8ASQSRlDgVCRwlza9GlUgTB9Eiup0SlSNFq5TvTK1GnDSUsjKhO4EGXas18xGpwIV6Zc
        sBvrTgrpsiHSvW5SRsQoNTCaTCf3ws14NrHLSW5iwnw5sGImiUkR4l1JeeDSv2cjPxQzFK
        tcmTmhXkZ6eW/W1WzBirmcFGTXvVKV3r49KTfYlhZbHsT6myJNNMOhEjwYGaLL5s4h8w5M
        U3HwwUc9Vjy+HUBEh0G3n5lsrJGjGOAIS593WHzk0fWaB+KEajRrQ8RE60sGWtZq1KSvmX
        WVTw+hsZVOXa111EAHToLYWGuNdVZaBkXY1oTjVRRXY3RpaBeHeXlo2VE1+QUfbd7dVZR1
        iclVFIeDKRbTUPGdBZlFQDFWWV/4YfUZfPPVBpp4TIEVG2suoTbXkbP9tNtEgeW2FEEPUt
        lbUu1ZFCKBHR6XXEAAOw==""",
}


#def _create_rotated_image(source, source_height, source_width):
# Does not work ... but idea is good :)
#    """ returns new tk.PhotoImage with source pixels rotated 90deg clockwise.
#        Assuming source image has square dimensions
#    """
#    #source_height = int(source['height'])
#    #source_width = int(source['width'])
#    #print(source['height'], source['height'], file=sys.stderr)
#    dest = tk.PhotoImage(width=source_height, height=source_width)
#    for x in range(source_width):
#        for y in range(source_height):
#            px = source.get(x, y)
#            print("pixel: ", px, file=sys.stderr)
#            dest.put(px, to=(source_height-y, x))
#    
#    return dest

        
if __name__ == '__main__':
    if len(sys.argv) < 2:
        layout_str = "####\n#> #\n#  #\n####"
    else:
        layout_str = eval(sys.argv[1])

    try:
        wp = _WorldProper(layout_str)
        cb = _CmdBroker(wp)
        cb.start()
        print("OK")
    except:
        print(repr(traceback.format_exc()))

    # run mainloop
    wp.run()
    
    
    
            
        
        
        
        
        
