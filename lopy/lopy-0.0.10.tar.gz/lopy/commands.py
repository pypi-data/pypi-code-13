import os
import sys
import subprocess

from colorama import init, Fore

init(autoreset=True)

def install(lopy_dir, config, *args):
  if len(args) == 0:
    args = ("-r", "requirements.txt")

  # We execute the command directly with subprocess
  # instead of pip.main, because pip.main disregards
  # setting os.environ["PYTHONUSERBASE"] in some cases
  execute(lopy_dir, config, *(['pip', 'install', '--user'] + list(args)))

def do(lopy_dir, config, *args):
  # Look for the task given at args[0]
  task_name = args[0]

  try:
    task_command = config['tasks'][task_name]
    execute(lopy_dir, config, task_command)
  except KeyError:
    print(Fore.RED + "Task {} not found".format(task_name))

def console(lopy_dir, config, *args):
  execute(lopy_dir, config, "python")

def run(lopy_dir, config, *args):
  execute(lopy_dir, config, *([ "python" ] + list(args)))

def execute(lopy_dir, config, *args):
  env = os.environ.copy()
  env["PYTHONUSERBASE"] = lopy_dir
  env["PATH"] = lopy_dir + '/bin:' + env.get('PATH', '')
  process = subprocess.Popen(list(args), env=env)
  _wait_for_process(process)
  sys.exit(process.returncode)

# Here we ignore any KeyboardInterrupt in the main process
# and just continue to communicate with the subprocess
def _wait_for_process(process):
  try:
    process.communicate()
  except KeyboardInterrupt:
    _wait_for_process(process)
