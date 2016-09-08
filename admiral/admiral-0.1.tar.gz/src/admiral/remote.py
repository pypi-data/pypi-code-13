import importlib
import itertools
import os
import cPickle as pickle
import sys


class RunRemoteException(Exception):
    pass


def _write_orders(job_dir, job_name, fn, args, kwdargs, overwrite):
    remote = {
        "function": fn,
        "args": args,
        "kwdargs": kwdargs
        }

    remote_instructions_path = os.path.join(
        job_dir, "{}.orders".format(job_name))

    if (not overwrite) and os.path.exists(remote_instructions_path):
        raise RunRemoteException("Remote instructions file already exists:"
                                 "'{}'. Use 'overwrite=True' to overwrite this file")

    with open(remote_instructions_path, "w") as f:
        pickle.dump(remote, f, protocol=-1)


    return remote_instructions_path

    
def run_remote(fn, jobmanager, job_name, args=None, kwdargs=None,
               array=False, job_dir=None, overwrite=False, 
               tries=10, wait=30, **jobmanager_kwdargs):

    if not array:
        if args is None:
            args = []
        if kwdargs is None:
            kwdargs = {}
        

    pythonpath = ":".join(sys.path)

    if job_dir is None:
        job_dir = jobmanager.batch_dir

    
    if array:
        if kwdargs is None:
            kwdargs = [{}]*len(args)
        if args is None:
            args = [[]]*len(kwdargs)
                               
        assert not isinstance(kwdargs, dict)
        assert len(args) == len(kwdargs)
                   
        remote_instructions_paths = []

        for i, (cur_args, cur_kwdargs) in enumerate(zip(args, kwdargs)):
            cur_job_name = "{}_{:05d}".format(job_name, i)
            remote_instructions_paths.append(
                _write_orders(job_dir, cur_job_name,
                              fn, cur_args, cur_kwdargs, overwrite))
        os.putenv("remote_instructions_paths", " ".join(remote_instructions_paths))
        
        command = ["export PYTHONPATH={pythonpath}",
                   "remote_instructions_paths=(${{remote_instructions_paths}})",
                   "echo ${{remote_instructions_paths[*]}}",
                   "{python} {this} ${{remote_instructions_paths[${{SLURM_ARRAY_TASK_ID}}]}}"]
        command = "\n".join(command)

        command = command.format(pythonpath=pythonpath,
                                 remote_instructions_paths=remote_instructions_paths,
                                 python=sys.executable,
                                 this=__file__)

        array_command = None
        if array:
            array_command = "0-{}".format(len(args)-1)
            
        job = jobmanager.make_job(command, job_name=job_name, array=array_command,
                                  **jobmanager_kwdargs)
        job.run()

    return job


if __name__ == "__main__":
    remote_instructions_path = sys.argv[1]

    remote_instructions = pickle.load(open(remote_instructions_path))

    #print ">>>>>>", remote_instructions
    function = remote_instructions["function"]
    args = remote_instructions["args"]
    kwdargs = remote_instructions["kwdargs"]

    function(*args, **kwdargs)
