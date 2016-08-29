# geniegui
# (c) Sven Rahmann, 2011--2012

"""
The functions of the geniegui module examine an argparse.ArgumentParser object
and create a tkinter GUI for it that allows to edit in all option values.
The given default values are shown,
and by default optional options are disabled.
"""

# This needs Python 3.2+ and Tk/Tcl distribution 8.5. ++
#
# Windows:
# I found that it just works with standard Python 3.2.
# For using it with virtualenv, however, explicitly set
# the environment variable TCL_LIBRARY = D:\Python32\tcl\tcl85
# (or wherever the .dll is located)
#
# Mac:
# The best idea is to download the community edition from ActiveState.
# Also it cannot hurt to set TCL_LIBRARY.
#
# Linux:
# I also use the ActiveState distribution.
# If the only problem is that the tile package is missing,
# see http://sourceforge.net/projects/tktable/files/,
# but I have never been able to install it properly.
#
# DEFINITELY read these pages:
# http://www.tkdocs.com/tutorial/

import sys
import shlex
import argparse
import multiprocessing
import io
from collections import OrderedDict
from contextlib import contextmanager
import textwrap
import platform

import tkinter as tk
from tkinter import ttk

###############################################################


class AutoHideScrollbar(tk.Scrollbar):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)
        self.is_visible = False

    def set(self, first, last):
        if float(first) > 0 or float(last) < 1:
            self.grid()
        else:
            self.grid_remove()
        super().set(first, last)

    def grid_configure(self, *args, **kwargs):
        self.is_visible = True
        super().grid_configure(*args, **kwargs)

    def grid_remove(self, *args, **kwargs):
        self.is_visible = False
        super().grid_remove(*args, **kwargs)

    def pack_configure(self, *args, **kwargs):
        raise NotImplementedError

    def place_configure(self, *args, **kwargs):
        raise NotImplementedError


class AutoScrollable(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        xscrollbar = AutoHideScrollbar(self, orient=tk.HORIZONTAL)
        yscrollbar = AutoHideScrollbar(self, orient=tk.VERTICAL)
        xscrollbar.grid(row=1, column=0, sticky="we")
        yscrollbar.grid(row=0, column=1, sticky="ns")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(1, weight=0)

        canvas = tk.Canvas(self)
        canvas.grid(row=0, column=0, sticky="nswe")

        canvas.config(xscrollcommand=xscrollbar.set)
        canvas.config(yscrollcommand=yscrollbar.set)
        xscrollbar.config(command=canvas.xview)
        yscrollbar.config(command=canvas.yview)

        content = tk.Frame(canvas)
        content_id = canvas.create_window(0, 0, window=content, anchor="nw")
        def on_content_config(event):
            content.update_idletasks()
            canvas.config(scrollregion=canvas.bbox(tk.ALL))
        content.bind("<Configure>", on_content_config)
        def on_canvas_config(event):
            #print(content.grid_bbox())
            #print(vars(event))
            width = max(content.winfo_reqwidth(), event.width - 4)
            height = max(content.winfo_reqheight(), event.height - 4)
            canvas.itemconfig(content_id, width=width)
            canvas.itemconfig(content_id, height=height)
        canvas.bind("<Configure>", on_canvas_config)
        self.content = content

        # NOTE: os specific handling done like in
        # https://code.activestate.com/recipes/578894/
        system = platform.system()
        speed = 2
        if system == "Linux":
            def get_delta(event):
                if event.num == 4:
                    return -1 * speed
                if event.num == 5:
                    return speed
                return 0
        elif system == "Windows":
            def get_delta(event):
                return -1 * int(event.delta / 120 * speed)
        else:  # if system == "Darwin":
            def get_delta(event):
                return event.delta

        def on_mousewheel(event):
            if event.widget is yscrollbar:
                return
            delta = get_delta(event)
            if delta > 0:
                if yscrollbar.get()[1] >= 1:
                    return
            elif delta < 0:
                if yscrollbar.get()[0] <= 0:
                    return
            #delta = int(canvas.winfo_height() * yscrollbar.delta(0, delta))
            canvas.yview_scroll(delta, "units")

        if system == "Linux" :
            def bind_mousewheel(event):
                canvas.bind_all("<Button-4>", on_mousewheel)
                canvas.bind_all("<Button-5>", on_mousewheel)
            def unbind_mousewheel(event):
                canvas.unbind_all("<Button-4>")
                canvas.unbind_all("<Button-5>")
        else:
            def bind_mousewheel(event):
                canvas.bind_all("<MouseWheel>", on_mousewheel)
            def unbind_mousewheel(event):
                canvas.unbind_all("<MouseWheel>")
        self.bind("<Enter>", bind_mousewheel)
        self.bind("<Leave>", unbind_mousewheel)
    # Couldn't get bindtag propagation to work properly; used bind_all instead..
        #canvas.bind("<MouseWheel>", on_mousewheel)  # is_windows
        #canvas.bind("<Button-4>", on_mousewheel)    # is_linux
        #canvas.bind("<Button-5>", on_mousewheel)    # is_linux
        #master.bind_class(self, "<MouseWheel>", on_mousewheel)
        #master.bind_class(self, "<Button-4>", on_mousewheel)
        #master.bind_class(self, "<Button-5>", on_mousewheel)
        #self.bindtags((self,) + self.bindtags())
    #def bind_child(self, child):
    #    child.bindtags((self,) + child.bindtags())

###############################################################


from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog, scrolledtext


############################# DEBUG ###########################
def print_attributes(obj):
    for k,v in obj.items():
        print(k, ":", type(v))
    print()


############################# STUFF ###########################

def wrap(text, *args, **kwargs):
    return "\n".join(textwrap.wrap(text, *args, **kwargs))

def _optstr(fromdefault, nargs=None):
    if nargs is None or nargs == "?":
        return str(fromdefault)
    # else return string from the list
    try:
        s = "  ".join("'{}'".format(str(x)) for x in fromdefault)
    except TypeError:
        print("TypeError in _optstr({},{})".format(fromdefault, nargs))
        raise
    return s

def _optstrlist(fromdefault, nargs=None):
    if nargs is None or nargs == "?":
        if fromdefault is None:
            defaults = []
        else:
            defaults = [fromdefault]
    else:
        defaults = fromdefault
    try:
        defaults = [str(x) for x in defaults]
    except TypeError:
        print("TypeError in _optstrlist({},{})".format(fromdefault, nargs))
        raise
    return defaults

def _optlist(fromstring, nargs=None):
    if nargs is None:
        return [fromstring]
    result = shlex.split(fromstring)
    if nargs=="+" and len(result)==0:
        # must return at least an empty string
        return [""]
    if nargs=="?" and len(result) > 1:
        return [fromstring]
    return result

def new_frame(
        tkmaster, column=0, row=0, column_config=[(0, 1)], row_config=[(0, 1)],
        sticky="NSWE"):
    frame = ttk.Frame(tkmaster)
    frame.configure(padding=2)
    frame.grid(column=column, row=row, sticky=sticky)
    for child_column, weight in column_config:
        frame.columnconfigure(child_column, weight=weight)
    for child_row, weight in row_config:
        frame.rowconfigure(child_row, weight=weight)
    return frame


@contextmanager
def std_redirector(stdin=None, stdout=None, stderr=None):
    if stdin is None: stdin = sys.stdin
    if stdout is None: stdout = sys.stdout
    if stderr is None: stderr = sys.stderr
    tmp_fds = stdin, stdout, stderr
    orig_fds = sys.stdin, sys.stdout, sys.stderr
    sys.stdin, sys.stdout, sys.stderr = tmp_fds
    yield
    sys.stdin, sys.stdout, sys.stderr = orig_fds


############################# action handlers ###########################
# these handlers define how to extend a tk widget when given
# an argparse action

def _create_entry_field(element, action, textwidth=50, nargs=None,
                        checkbuttonvar=None, special=None, bg=None):
    """create a text entry field and return the corresponding Tk string variable
    (or do nothing, depending on the action type).
    The 'checkbuttonvar' parameter can be a checkbutton's IntVar
    that is set to 1 if the text changes, or None.
    The 'special' parameter creates a file or directory dialog button if set
    to "file" or "dir" respectively.
    """
    t = type(action)
    if t is argparse._StoreTrueAction:
        return None
    elif t is argparse._StoreConstAction:
        return None
    elif t is argparse._StoreAction:
        # create a corresponding Tk variable, set default, bind checkbutton
        var = StringVar()
        if action.default is not None:
            var.set(_optstr(action.default, nargs=nargs))
        if checkbuttonvar is not None:
            def activateoption(varname,varindex,varaccess):
                if var != "":  checkbuttonvar.set(1)
            var.trace_variable("w", activateoption)
        # Create the appropriate entry field type (text or choice)
        if action.choices is None:
            # normal entry field
            entry = Entry(element, textvariable=var, width=textwidth)
            entry.grid(row=1, column=0, sticky="NWE")
            if special is not None:
                if special == "dir":
                    def cmd():
                        result = filedialog.askdirectory(initialdir=var.get(), parent=element)
                        if result != "": var.set(result)
                elif special == "file":
                    def cmd():
                        result = filedialog.askopenfilename(initialdir=var.get(), parent=element)
                        if result != "": var.set(result)
                if special in {"dir","file"}:
                    btn = ttk.Button(element, text="...", width=3, command=cmd)
                    btn.grid(row=1, column=1, sticky="NE")
                else:
                    raise NotImplementedError("unknown special {}".format(special))
        else:  # action has choices -> do a Radiobox array
            buttonbox = tk.Frame(element, bg=bg)
            buttonbox.grid(row=1, column=0, sticky="NW")
            if action.nargs not in {"+", "*"}:
                for ch in action.choices:
                    btn = tk.Radiobutton(buttonbox, text=ch, variable=var, value=ch, bg=bg)
                    btn.pack(anchor=N, side=LEFT, ipadx=5)
            else:
                var_list = []
                defaults = set(_optstrlist(action.default, nargs=nargs))
                for ch in action.choices:
                    chk = BooleanVar()
                    var_list.append((chk, ch))
                    chk.set(ch in defaults)
                    btn = tk.Checkbutton(buttonbox, text=ch, variable=chk, bg=bg)
                    btn.pack(anchor=N, side=LEFT, ipadx=5)
                # bind checkbutton
                if checkbuttonvar is not None:
                    if action.nargs == "+":
                        def activateoption(varname, varindex, varaccess):
                            checkbuttonvar.set(any(chk.get() for (chk, _) in var_list))
                    else:  # if action.nargs == "*":
                        def activateoption(varname, varindex, varaccess):
                            if any(chk.get() for (chk, _) in var_list):
                                checkbuttonvar.set(True)
                    for chk, _ in var_list:
                        chk.trace_variable("w", activateoption)
                var = var_list

        return var
    # action not defined?
    else:
        print(action.__class__)
        print(action.choices)
        raise NotImplementedError(str(t))


def _do_nothing(gui, action):
    pass

def _add_store_action(gui, action, optional=True):
    textwidth = 120
    parent = gui.optionsframe#mainframe
    oprefix = gui.optionprefix
    if optional:
        name = dname = action.option_strings[0]
    else:
        dname = action.dest
        name = "__" + str(gui.nextpos) + "__" + dname
        gui.nextpos += 1
    myspecial = gui.specials.get(name, None)
    if myspecial == "hidden" or action.help == argparse.SUPPRESS:
        return
    # process nargs
    # gui.listoption is a dict() with nargs-values
    gui.listoption[name] = None
    helptext = ""
    if action.nargs:  # not None or 0
        helptext = "<{}> ".format(str(action.nargs))
        gui.listoption[name] = str(action.nargs)
    # lay out the GUI elements for this action
    bg = parent.cget("bg")
    if gui.opt_nrows % 4 == 0:
        bg = parent.winfo_rgb(bg)
        bg = [int(0.9 * x / 256) for x in bg]
        from codecs import decode, encode
        bg = "#" + decode(encode(bytes(bg), "hex"))
    bgframe = tk.Frame(parent, height=0, bg=bg)
    bgframe.grid(row=gui.opt_nrows, column=0, columnspan=4, sticky="NSWE")
    #if isinstance(gui.optionsframe.master.master, AutoScrollable):
    #    gui.optionsframe.master.master.bind_child(bgframe)

    optionlabel = tk.Label(parent, text=dname, bg=bg)
    optionlabel.grid(row=gui.opt_nrows, column=0, sticky="NE")
    state = NORMAL if optional else DISABLED
    required = not optional
    gui.useoptions[name] = IntVar()
    gui.useoptions[name].set(0 if optional else 1)
    optionbox = tk.Checkbutton(parent, state=state, variable=gui.useoptions[name], bg=bg)
    optionbox.grid(row=gui.opt_nrows, column=1, sticky="NW")
    element = tk.Frame(parent, bg=bg)
    element.grid(row=gui.opt_nrows, column=2, sticky="NWES")
    element.columnconfigure(0, weight=1)
    if action.help is not None:
        helptext += action.help
    helplabel = tk.Label(element, text=wrap(helptext, textwidth), justify=LEFT, bg=bg)
    helplabel.grid(row=0, column=0, sticky="NW")
    mynargs = gui.listoption[name]
    gui.options[name] = _create_entry_field(element, action, nargs=mynargs,
        checkbuttonvar=gui.useoptions[name], special=myspecial, textwidth=textwidth, bg=bg)

    bgframe.config(height=helplabel.winfo_height())
    bgframe.grid()
    # spacers
    #hspacer = Frame(parent, width=20)
    #hspacer.grid(row=gui.opt_nrows, column=3, sticky="NW")
    gui.opt_nrows += 1

    vspacer = Frame(parent, height=5)
    vspacer.grid(row=gui.opt_nrows, column=0, columnspan=4, sticky="NSWE")
    gui.opt_nrows += 1


def _add_subparsers_action(gui, action):
    subparsers = action.choices  # this is an OrderedDict.
    subcommands = [k for k in subparsers.keys() if k != "GUI"]
    #print("subparsers with subcommands:", subcommands)
    parent = gui.optionsframe#mainframe
    notebook = ttk.Notebook(parent)
    notebook.grid(row=gui.opt_nrows, column=0, sticky="NWSE", columnspan=3)
    gui.opt_nrows += 1
    notebook.columnconfigure(0, weight=1)  # expand on resize
    notebook.rowconfigure(0, weight=1)  # expand on resize
    scdescription = dict()
    for pseudoaction in action._choices_actions:  # need to use internals
        scdescription[pseudoaction.dest] = pseudoaction.dest + ": " + pseudoaction.help
    for sc in subcommands:
        subframe = Frame(notebook)
        subframe.grid(row=0, column=0, sticky="NWSE")
        subframe.columnconfigure(0, weight=1)  # expand on resize
        subframe.rowconfigure(0, weight=1)  # expand on resize
        notebook.add(subframe, text=sc)
        subparser = ArgparseGUI(subparsers[sc], guimaster=gui, title=sc,
            tkmaster=subframe, description=scdescription[sc])
        gui.subparsers[sc]=subparser
    gui.nofinalbuttons = True

def _add_posstore_action(gui, action):
    _add_store_action(gui, action, optional=False)


# define which function to call for the different types of argparse actions
optactionhandlers = {
    argparse._HelpAction: _do_nothing,
    argparse._VersionAction: _do_nothing,
    argparse._StoreAction: _add_store_action,
    argparse._StoreTrueAction: _add_store_action,
    argparse._StoreConstAction: _add_store_action,
    }

posactionhandlers = {
    argparse._SubParsersAction: _add_subparsers_action,
    argparse._StoreAction: _add_posstore_action,
    }

########### the main GUI frame #######################################

class ArgparseGUI():
    def __init__(self, parser, mainmethod=None, guimaster=None,
                 tkmaster=None, title=None, description=None):
        """create a GUI instance from argparse instance 'parser'
        inside TK toplevel 'tkwindow' with an optional 'title'
        and 'description'"""
        if tkmaster is None:
            tkmaster = Tk()
            tkmaster.withdraw()
            tkmaster.columnconfigure(0, weight=1)  # expand on resize
            tkmaster.rowconfigure(0, weight=1)  # expand on resize
            ttkstyle = ttk.Style()
            ttkstyle.configure("Information.TLabel", foreground="blue", wraplength=640, justify=LEFT)
        if guimaster is None:
            self.window = tkmaster
            if title is not None: tkmaster.title(title)
            self.name = "__main__"
        else:
            self.window = guimaster.window
            self.name = title
        self.mainmethod = mainmethod
        self.guimaster = guimaster
        self.parser = parser
        self.specials = parser._geniegui if hasattr(parser, "_geniegui") else dict()
        self.optionprefix = parser.prefix_chars[0]
        self.useoptions = OrderedDict()
        self.listoption = dict()
        self.options = dict()
        self.subparsers = dict()
        self.nofinalbuttons = False
        self.mainframe = new_frame(tkmaster, row_config=[])
        self.optionsframe = None
        self.nrows = 0
        self.opt_nrows = 0
        self.command = "__CANCEL__"
        self.nextpos = 0
        #print_attributes(parser.__dict__)
        self.processes = dict()  # running processes -- see runcommand
        self.create_gui(description)
        if guimaster is None:
            window = self.window
            window.update()
            some_delta_for_taskbar = 100
            some_delta_for_scrollbar = 20
            window_width = min(
                window.winfo_reqwidth() + some_delta_for_scrollbar,
                window.winfo_screenwidth() - some_delta_for_taskbar)
            window_height = min(
                window.winfo_reqheight() + some_delta_for_scrollbar,
                window.winfo_screenheight() - some_delta_for_taskbar)
            window.geometry(str(window_width) + "x" + str(window_height))
            window.deiconify()

    def create_gui(self, description=None):
        """create tkinter GUI with a given TK 'master' object
        from ArgumentParser object 'parser'."""
        # put mainframe into the root tkwindow using the grid manager
        parser = self.parser
        # description of the program
        if description is None:
            desc = parser.description if parser.description is not None else ""
        else:
            desc = description
        mainframe = self.mainframe
        ldesc = ttk.Label(mainframe, text=desc, style="Information.TLabel")
        ldesc.grid(row=self.nrows, column=0, sticky="NW", padx=5, pady=5)
        self.nrows += 1
        optionsframe_nrow = self.nrows
        if self.guimaster is None:
            optionsframe = AutoScrollable(mainframe)
            optionsframe.grid(column=0, row=optionsframe_nrow, sticky="NWSE")
            optionsframe = optionsframe.content
        else:
            optionsframe = tk.Frame(mainframe)
            optionsframe.grid(column=0, row=optionsframe_nrow, sticky="NWSE")
        mainframe.rowconfigure(optionsframe_nrow, weight=1)  # expand on resize
        self.nrows += 1
        optionsframe.columnconfigure(2, weight=1)  # expand on resize
        self.optionsframe = optionsframe
        # examine parser for all options, option groups, mutex groups, subparsers
        for action in parser._get_optional_actions():
            handler = optactionhandlers[type(action)]
            handler(self, action)
        for action in parser._get_positional_actions():
            handler = posactionhandlers[type(action)]
            handler(self, action)
        # final start/cancel buttons and epilog
        self.create_final_buttons()
        mainframe.epilog = ttk.Label(mainframe, text=parser.epilog, style="Information.TLabel")
        mainframe.epilog.grid(row=self.nrows, column=0, sticky="E")
        self.nrows += 1
        optionsframe.rowconfigure(self.opt_nrows-1, weight=1)  # expand on resize
        optionsframe.update()
        if optionsframe.master.winfo_width() != optionsframe.winfo_reqwidth():
            optionsframe.master.config(width=optionsframe.winfo_reqwidth())
        if optionsframe.master.winfo_height() != optionsframe.winfo_reqheight():
            optionsframe.master.config(height=optionsframe.winfo_reqheight())
        if (self.guimaster is not None) and optionsframe.children:
            opts_minheight = max(child.winfo_reqheight()
                                 for child in optionsframe.children.values())
            mainframe.rowconfigure(optionsframe_nrow,
                                   minsize=opts_minheight, weight=5)

    def create_final_buttons(self):
        if self.nofinalbuttons: return
        frame = Frame(self.optionsframe)
        frame.grid(row=self.opt_nrows, column=0, sticky="NE", columnspan=3)
        bstart = ttk.Button(frame, text="Start", padding=5,
                        command = lambda x=self.name: self.runcommand(x))
        bstart.pack(side=LEFT)
        bcancel = ttk.Button(frame, text="Quit", padding=5,
                         command = lambda x="__CANCEL__": self.runcommand(x))
        bcancel.pack(side=LEFT)
        self.opt_nrows += 1

    def poll(self):
        toremove = []
        for pid, pdict in self.processes.items():
            #print("polling", pid)
            outfield = pdict["outfield"]
            text = pdict["pipe"].read()
            text_stderr = pdict["pipe_stderr"].read()
            outfield.insert(END,text)
            outfield.insert(END,text_stderr, ("stderr",))
            #ranges = outfield.tag_ranges("stderr")
            #for i in range(len(ranges)-1, -1, -2):
            #    outfield.delete(ranges[i-1], ranges[i])
            outfield.see(END)
            p = pdict["process"]
            if not p.is_alive():
                toremove.append(pid)
                pdict["whenfinished"]()
        for pid in toremove:
            del self.processes[pid]
        self.window.after(1000, self.poll)

    def arguments(self):
        args = list()
        for name, tkvar in self.useoptions.items():
            if tkvar.get() == 0: continue  # option not used
            optvar = self.options[name]
            if isinstance(optvar, list) and not any(chk.get() for chk, _ in optvar):
                continue  # empty selection
            if name.startswith(self.optionprefix):
                # true option, not positional argument
                args.append(name)
            if optvar is None: continue  # flag only
            if not isinstance(optvar, list):
                optstr = optvar.get()  # the string
                args.extend(_optlist(optstr, nargs=self.listoption[name]))
                continue
            for (chk, optstr) in optvar:
                if not chk.get():
                    continue
                args.extend(_optlist(optstr, nargs=self.listoption[name]))
        if self.command in self.subparsers:
            args.append(self.command)
            args.extend(self.subparsers[self.command].arguments())
        return args

    def runcommand(self, cmd):
        # get topmost instance and its arguments
        instance = self
        while instance.guimaster is not None: instance = instance.guimaster
        if cmd == "__CANCEL__":
            self.window.destroy()  # not instance.window?
            return
        instance.command = cmd
        args = instance.arguments()
        processtitle = instance.window.title()+"  "+" ".join(args)
        pdict = newguiprocess(instance.window, processtitle, instance.mainmethod, args)
        pid = pdict["process"].pid
        instance.processes[pid] = pdict

############################# processing ###########################

class TextPipe():
    def __init__(self):
        self.connrecv, self.connsend = multiprocessing.Pipe(duplex=False)
    def write(self, string):
        self.connsend.send(string)
    def read(self):
        reader = self.connrecv
        textlist = []
        while reader.poll():
            textlist.append(reader.recv())
        return "".join(map(str,textlist))
    def flush(self):
        pass

def newguiprocess(tkmaster, processtitle, mainmethod, args):
    # Create a new window with a title, textbox and close button
    popup = Toplevel(tkmaster)
    popup.columnconfigure(0, weight=1)
    popup.rowconfigure(0, weight=1)
    popup.title(processtitle)
    pframe = new_frame(popup, 0, 0, [(0, 1)], [(1, 1)], "NSWE")
    plabel = ttk.Label(pframe, text=processtitle, style="Information.TLabel")
    plabel.grid(row=0, column=0, sticky="NW")
    poutputfield = scrolledtext.ScrolledText(pframe)
    poutputfield.grid(row=1, column=0, sticky="NWSE")
    poutputfield.tag_config("stderr", foreground="red")
    pbottomframe = new_frame(pframe, 0, 2, [(0, 1)], [(0, 1)], "SWE")
    pbottomlabel = ttk.Label(pbottomframe, text="Running...", style="Information.TLabel")
    pbottomlabel.grid(row=0, column=0, sticky="SW")
    pclose = Button(pbottomframe, text="Close", state=DISABLED, command=popup.destroy)
    pclose.grid(row=0, column=1, sticky="SE")
    def whenfinished():
        pclose.configure(state=NORMAL)
        pbottomlabel.configure(text="Finished.")
    mypipe = TextPipe()
    mypipe_stderr = TextPipe()
    p = multiprocessing.Process(target=runguiprocess,
        args=(mainmethod,args,mypipe, mypipe_stderr))
    p.start()
    return dict(process=p, whenfinished=whenfinished, outfield=poutputfield, pipe=mypipe, pipe_stderr=mypipe_stderr)

def runguiprocess(mainmethod, arglist, thepipe, thepipe_stderr):
    oldout, olderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = thepipe, thepipe_stderr
    mainmethod(arglist)
    sys.stdout, sys.stderr = oldout, olderr


############################# main methods ###########################

def get_argument_parser():
    """interface for geniegui.py"""
    return main_buildparser()

def main_buildparser():
    p = argparse.ArgumentParser(
        description="geniegui: Genome Informatics GUI",
        epilog="In development. Use at your own Risk!"
        )
    p.add_argument("--title", "-t",
                   help = "specify title of GUI window")
    p.add_argument("--mainfunction","-m", default="main",
                   help = "name of main function of called module")
    p.add_argument("--parserfunction","-p", default="get_argument_parser",
                   help = "name of get_argument_parser function of called module")
    p.add_argument("module",
                   help = "python module (without .py) to create GUI for")
    return p


def rungui(args):
    # get parser
    modulename = args.module
    #print("PATH is", sys.path)
    module = __import__(modulename)
    #print("MODULE is", module)
    try:
        parserfunction = getattr(module, args.parserfunction)
    except AttributeError:
        print("geniegui: no function '{}' in module file '{}'".format(args.parserfunction, module.__file__))
        raise
    parser = parserfunction()  # returns parser; it may have an attibute _geniegui
    # treat arguments
    title = args.title if args.title is not None else modulename
    # create and start GUI
    modulemain = getattr(module, args.mainfunction)  # will raise error if no main exists
    gui = ArgparseGUI(parser, mainmethod=modulemain, title=title)

    gui.poll()
    gui.window.mainloop()


def main(args=None):
    """main function"""
    p = get_argument_parser()
    pargs = p.parse_args() if args is None else p.parse_args(args)
    rungui(pargs)

############################# test methods ###########################

def test():
    #main(["geniegui","--title","Genie GUI"])
    main(["amplikyzer"])

if __name__ == "__main__":
    #test()
    main()

############################# END ###########################
