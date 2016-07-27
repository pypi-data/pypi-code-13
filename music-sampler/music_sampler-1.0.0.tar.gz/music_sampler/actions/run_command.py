import shlex, subprocess

def run(action, command="", wait=False, **kwargs):
    action.process = subprocess.Popen(command, shell=True)
    if wait:
        action.process.wait()

def description(action, command="", wait=False, **kwargs):
    message = "running command {}".format(command)
    if wait:
        message += " (waiting for its execution to finish)"

    return message
