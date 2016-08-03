from core.core import Core
import cmd

class dssCmdLine(cmd.Cmd):
    """Command processor for dss"""
    prompt = '_$ '
    use_rawinput = False

    def do_start(self, args):
        dss_core = Core()
        dss_core.run()

    def do_list(self,args):
        dss_core = Core()
        dss_core.list()

    def do_parse(self, args):
        dss_core = Core()
        dss_core.parse()

    def do_terminate(self,args):
        dss_core = Core()
        dss_core.terminate()

    def do_decompress(self,args):
        dss_core = Core()
        dss_core.decompress()

    def do_enable(self, args):
        dss_core = Core()
        dss_core.get_enabled()

    def do_running(self,args):
        dss_core = Core()
        dss_core.get_running()

    def do_EOF(self,args):
        '"Handles exiting the system with end of file character"'
        print '\n'
        return True
if __name__ == '__main__':
    dssCmdLine().cmdloop()
