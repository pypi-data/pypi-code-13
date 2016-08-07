import configparser
import os
import sys

from colorama import init, Fore
from lopy.commands import install, do, run, execute, console

# Initialize colorama
init(autoreset=True)

def find_up(path):
  # Look for the following in order:
  # .lopyconfig
  # .pip directory
  # requirements.txt
  # .git directory
  # If none are found, then lopy can't sensibly find directory to work on 
  lookups = [ ".lopyconfig", ".pip/", "requirements.txt", ".git/" ]
  abs_path = os.path.realpath(path)

  if abs_path == '/':
    return False
  for lookup in lookups:
    if os.path.exists(lookup):
      return abs_path
  return find_up(abs_path + '/..')

def lopy_help():
    return '''lopy -- Install local Python packages

Commands:
  install   Local pip install (by default installs requirements.txt)
            Usage: lopy install [dep_name]

  do        Run a lopyconfig task
            Usage: lopy do <task_name>

  run       Run a python script at <path> (alias for `exec python`)
            Usage: lopy run <script.py>

  exec      Execute a program within the local lopy environment
            Usage: lopy exec <command>

  console   Spawn a console
            Usage: lopy console
    '''
def main():
  arg_dict = {
    "install": install,
    "do": do,
    "exec": execute,
    "run": run,
    "console": console
  }

  raw_args = sys.argv[1:]

  try:
    args = {
      "command": raw_args[0],
      "args": raw_args[1:],
    }
  except IndexError:
    quit(lopy_help())

  method = args["command"]
  method_arguments = args["args"]

  try:
    arg_dict[method]
  except KeyError:
    # If the command doesn't exist, see if the file exists
    if os.path.isfile(method):
      method_arguments = [ method ] + method_arguments
      method = "run"
    else:
      quit(lopy_help())

  # Find the closest directory to run lopy in
  lopy_dir = find_up(os.getcwd())

  # Quit with error if could not find lopy_dir
  if not lopy_dir:
    # We specifically allow installing a module directly
    if method == 'install' and len(method_arguments) > 0:
      print(Fore.RED + 'Could not locate suitable directory. Using current directory...')
      lopy_dir = os.getcwd()
    else:
      quit("Could not locate .lopyconfig, .pip directory, requirements.txt, or .git directory")

  # Check if `module_dir` key is present in `.lopyconfig`
  config = configparser.ConfigParser()
  config.read(lopy_dir + '/.lopyconfig')
  module_dir = '.pip'

  if len(config):
    try:
      module_dir = config['config']['module_dir']
    except KeyError:
      pass

  lopy_dir = lopy_dir + '/' + module_dir

  arg_dict[method](lopy_dir, config, *method_arguments)
