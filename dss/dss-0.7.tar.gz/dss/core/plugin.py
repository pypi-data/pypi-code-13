import importlib
import json
import os
import schedule
import signal
import subprocess
import time
import signal
import psutil

META_DIR_NAME = "META"      # Name given to the metafile directory
META_EXT = ".txt"           # Metafile extension
NO_ARGS_MSG = "(No args passed)" #Message under args for the metafile

class PluginFactory(object):
    def build_from(self, base_dir):
        self.base_dir = base_dir
        self.config_file_path = os.path.join(base_dir, "config.json")
        self.config = None

        try:
            with open(self.config_file_path) as config_file:
                self.config_file = json.load(config_file)
                self.config = self.config_file.get("General")
        except ValueError as e:
            print ("Check format of JSON file: %s" % self.config_file_path)
            print e
        except Exception as e:
            print e

        if self.config != None:
            ctype = self.config["Type"]["Selected"]
            if ctype == Plugin.type:
                return Plugin(base_dir, self.config)
            elif ctype == SchedulablePlugin.type:
                return SchedulablePlugin(base_dir, self.config)
            elif ctype == MultiProcessPlugin.type:
                return MultiProcessPlugin(base_dir, self.config)
            elif ctype == ManualPlugin.type:
                return ManualPlugin(base_dir, self.config)
            elif ctype == ParserPlugin.type:
                return ParserPlugin(base_dir, self.config)
            else:
                raise ValueError("Type %s not found in plugin factory" % ctype)
        else:
            print ("The configurations from the JSON file could not be loaded: %s" % self.config_file_path)


###################################################################################
# provide result objects if required back to the client
class Plugin(object):
    __id = 0
    type = "plugin"

    def __init__(self, base_dir, config):
        self.base_dir = base_dir
        self.config = config

        self.name = self.config.get("Plugin Name", {}).get("Value")
        self.is_enabled = self.config.get("Is Enabled",{}).get("Selected")
        self.process = None

        self.exe_path = self.config.get("Exe Path",{}).get("Value")
        self.flags = self.config.get("Flags",{}).get("Value")
        self.output_dir = os.path.join(os.path.join(base_dir, self.config.get("Output",{}).get("Value")), '')
        self.meta_dir = os.path.join(os.path.join(self.output_dir, META_DIR_NAME))
        self.ext = self.config.get("Extension", {}).get("Selected")

        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

        # If the program is not standalone executable a shell will be needed
        if self.config.get("Is Standalone",{}).get("Selected"):
            self.is_shell_needed = False
        elif not self.config.get("Is Standalone",{}).get("Selected"):
            self.is_shell_needed = True

    def run(self):
        if self.is_enabled:
            if not self.is_live():
                self.build_cmd()
                self.create_metafile()
                try:
                    if os.name == "posix":
                        self.process = subprocess.Popen(self.cmd,
                                                        shell=True,
                                                        cwd=self.base_dir,
                                                        stdout=subprocess.PIPE,
                                                        stderr=subprocess.PIPE)
                    elif os.name == "nt":
                        if self.name == "pykeylogger":
                            self.process = subprocess.Popen(self.cmd,
                                                            shell=self.is_shell_needed,
                                                            cwd=self.base_dir,
                                                            stdout=subprocess.PIPE,
                                                            stderr=subprocess.PIPE)
                        else:
                            self.process = subprocess.Popen("call " + self.cmd,
                                                            shell=True,
                                                            cwd=self.base_dir,
                                                            stdout=subprocess.PIPE,
                                                            stderr=subprocess.PIPE)
                    
                except Exception as err:
                    print ("Error attempting to run: plugin: %s | cmd: %s\n" %(self.name, self.cmd))
                    print err

                print (" --> Running %s" % self.name)
                print (" [x] Starting: %s - pId:%s" % (self.name,self.process.pid))
                self.is_running = True  # TODO: need to callback when process ends to set is_running=false

    # If output needs to be appended to command. Some plugins generate their own output files into raw folder.
    # e.g. pykeylogger, the output is redirected using it's keylogger.ini file.
    def build_cmd(self):
        posix_prefix = ""
        if os.name == "posix":
            posix_prefix = "exec "

        # keep spaces between commands
        epoch_time = str(int(time.time()))
        if self.ext:
            self.out_file_name = epoch_time
            self.out_file_path = os.path.join(self.output_dir, self.out_file_name)
            self.cmd = posix_prefix \
                       + str(self.exe_path) + " "\
                       + str(self.flags) + " "\
                       + '"' + str(self.out_file_path) + str(self.ext) + '"' #No space between these two

        elif self.ext is None:
            self.out_file_name = epoch_time  # Needed for metafile.
            self.cmd = posix_prefix + " "\
                       + str(self.exe_path) + " "\
                       + str(self.flags)

    def create_metafile(self):
        if not os.path.exists(self.meta_dir):
            os.mkdir(self.meta_dir)
            os.path.join(self.meta_dir, "")

        self.metadata_filename = 'meta_' + str(self.out_file_name) + META_EXT
        self.metadata_file_path = os.path.join(self.meta_dir, self.metadata_filename)
        
        meta_file = open(self.metadata_file_path, "w")
        if os.name == "posix":
            os.chmod(self.metadata_file_path, 0755)
        meta_file.write(self.name + "\n===============================\n"
                        + "cmd= " + self.cmd)
        meta_file.close()


    def terminate(self):
        if self.process:
            try:
                parent_pid = self.process.pid
                parent = psutil.Process(parent_pid)
                for child in parent.children(recursive=True):  # or parent.children() for recursive=False
                    child.kill()
                parent.kill()
                #self.process.kill()
                # self.process.terminate()
                # os.kill(self.process.pid, signal.SIGTERM)
                if self.name == "tshark":
                    print "tshark found"
                    # for proc in psutil.process_iter():
                    #     print proc
                    #     if proc.name == r'tshark.exe':
                    #         print "tshark killed"
                    #         proc.kill()
                print (" [x] Terminating: %s - pId:%s" % (self.name,self.process.pid))
            except Exception as e:
                print (" !! %s: %s" % (self.name,e))
        elif self.process is None:
            print ("  ...%s process already dead" % self.name)
        self.process = None
    # TODO: implement status object, and job?! to collect status
    def is_live(self):
        if self.process:
            return True
        return False

    def parse(self):
        if not self.is_live():
            return self.parser(self.base_dir).parse()
        else:
            return []

            # TODO: Detect changes to configuration elems (e.g. enabled) & reflect changes to Config file

    def save_config(self):
        print "Save me"

        # def suspend(self):
        #     if self.is_running:
        #         self.is_running = False
        #
        #         try:
        #             #self.ps_process.suspend()
        #             self.process.kill()
        #             self.process.terminate()
        #
        #         except psutil.NoSuchProcess:
        #             pass

        # def resume(self):
        #     if not self.is_running:
        #         self.is_running = True
        #
        #         try:
        #             #self.ps_process.resume()
        #             pass
        #         except psutil.NoSuchProcess:
        #             pass


###############################################################
#  plugin will not start on core.run()
class ManualPlugin(Plugin):
    type = "manual"

    def __init__(self, base_dir, config):
        super(ManualPlugin, self).__init__(base_dir, config)


###############################################################
# plugin will not start on core.run()
class ParserPlugin(Plugin):
    type = "parser"

    def __init__(self, base_dir, config):
        super(ParserPlugin, self).__init__(base_dir, config)

###############################################################
class MultiProcessPlugin(Plugin):
    type = "multi"

    def __init__(self, base_dir, config):
        super(MultiProcessPlugin, self).__init__(base_dir, config)
        self.multi_processes = []

    def run(self):
        if self.is_enabled:
            # TODO: validation of data
            i = 0
            for arg_array in self.config.get("Interfaces",{}).get("Value"):
                # args = [self.run_path]
                # args.extend(arg_array)
                # args.extend([self.Config["output"]])

                # Create output file for each instance
                self.cmd = str(self.exe_path) + " " + str(self.flags)
                #### If log file needs to be created
                if self.config.get("Extension", {}).get("Selected"):
                    epoch_time = str(int(time.time()))
                    self.out_file_name = epoch_time + self.config.get("Extension", {}).get("Selected")
                    self.out_file_path = os.path.join(self.output_dir, self.out_file_name)
                    self.cmd = self.cmd + " " + str(self.out_file_path)

                if self.out_file_name != None:
                    self.create_metafile()

                proc = subprocess.Popen(self.cmd,
                                        cwd=self.base_dir,
                                        shell=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)

                self.multi_processes.append(proc)
                i += 1
            self.is_running = True

    def terminate(self):
        for process in self.multi_processes:
            try:
                # TODO: this is not killing tshark, processing continues to run. tshark
                # spawns a dumppcap process, this maybe the issue
                # process.terminate()
                process.kill()
                process.terminate()
                self.process = None
            except Exception as e:
                print e

        # def suspend(self):
        #     if self.is_running:
        #         for process in self.ps_processes:
        #             try:
        #                 process.suspend()
        #             except psutil.NoSuchProcess:
        #                 pass
        #         self.is_running = False

        # def resume(self):
        #     if not self.is_running:
        #         for process in self.ps_processes:
        #             try:
        #                 self.process.resume()
        #             except psutil.NoSuchProcess:
        #                 pass
        #         self.is_running = True


###############################################################
class SchedulablePlugin(Plugin):
    type = "schedulable"

    def __init__(self, base_dir, config):
        # call super constructor
        super(SchedulablePlugin, self).__init__(base_dir, config)
        # TODO: we need to be able to define different scheduling schemes
        # see:  https://pypi.python.org/pypi/schedule
        # define structure in JSON we can then parse to define repetition
        # periods such seconds, minutes, etc...
        seconds = self.config.get("Schedule",{}).get("Value")

        #schedule.every(seconds).seconds.do(self.__run_process) # TODO uncomment

    def __run_process(self):
        self.create_metafile()
        self.process = subprocess.Popen(self.cmd,
                                        cwd=self.base_dir,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
