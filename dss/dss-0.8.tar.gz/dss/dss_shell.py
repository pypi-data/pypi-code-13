import os
import sys
import cmd
import time
import shlex
import subprocess
from turtle import *
from core.core import Core
from plugins.collectors.manualscreenshot import takeshoot


class Shell(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.core = Core()
        self.core.list()

        self.intro = "\nDecision Support System Logger: For information type help or ? \n"
        self.prompt = ">> "
        self.completekey = 'tab'

        self._hist = []
        self._locals = []
        self._globals = []

    def precmd(self, line):
        self._hist += [line.strip()]
        return line

    def postcmd(self, stop, line):
        return stop

    def empyline(self):
        pass

    def default(self, line):
        try:
            exec line in self._locals, self._globals
        except Exception, e:
            print e.__class__, ":", e

    def do_hist(self, args):
        """ History of previously used commands"""
        print self._hist

    def do_shell(self, args):
        """ Allows shell commands to be executed using: \"shell <cmd>\"."""
        os.system(args)

    def do_postloop(self):
        cmd.Cmd.postloop(self)
        print "Exiting."

    def do_enabled(self, args):
        """ Lists the enabled plugins only"""
        self.core.get_enabled()

    def do_EOF(self, args):
        print ("Exiting")
        self.core.terminate()

    def do_exit(self, args):
        """ Terminates the entire program (alias for terminate)"""
        self.core.terminate()

    def do_quit(self, args):
        """ Terminates the entire program (alias for terminate)"""
	self.core.terminate()

    def do_restart(self, args):
        """ Terminates and runs the core. """
        self.core.terminate()
        self.core.run()

    def do_run(self, args):
        """ Begins running the Core """
        self.core.run()

    def do_running(self, args):
        """ Lists the plugins that are running only"""
        self.core.get_running()

    def do_start(self, args):
        """ Begins running the core (alias for run) """
        if self.core:
            self.core.terminate()
        self.core.run()

    def do_suspend(self, args):
        """ Suspends the core and """
        self.core.suspend()

    def do_terminate(self, args):
        """ Terminate the core and kills all the plugin processes """
        self.core.terminate()

    def complete_terminate(self):
        self.core.terminate()

    def do_decompress(self, args):
        """ Restore all the compressed data back to its uncompressed state """
        self.core.decompress()

    def do_list(self, args):
        """ Prints a list of the installed plugins """
        self.core.list()

    def do_parse(self, args):
        """ Parse the raw data provided by each plugin """
        self.core.parse()

    def do_screenshot(self, args):
        """ Take a screenshot """
        self.screenshot = takeshoot.CaptureScreen()
	
	

def parse(arg):
    return tuple(map(int, arg.split))

if __name__ == '__main__':
    shell = Shell()
    shell.cmdloop()
