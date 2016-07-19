import re, boto3, os, json, jmespath, sys, argparse
from yac.lib.variables import get_variable, set_variable

# state is persisted in a json file in s3
def load_state(params, state_filename):

    sites = {}

    s3 = boto3.resource('s3')

    state_file_s3_path = get_state_s3_path(params, state_filename)
    state_file_local_path_full = get_state_local_path(params, state_filename)

    s3_bucket = get_variable(params,'s3-bucket',"")

    # pull file down to the local dir
    s3.meta.client.download_file(s3_bucket, 
        state_file_s3_path, 
        state_file_local_path_full)

    # pull contents into a dictionary
    if os.path.exists(state_file_local_path_full):
        with open(state_file_local_path_full) as file_arg_fp:
            file_contents = file_arg_fp.read()
            state = json.loads(file_contents)

    return state

def save_state(params, state, state_filename):

    s3 = boto3.resource('s3')

    state_file_s3_path = get_state_s3_path(params, state_filename)
    state_file_local_path_full = get_state_local_path(params, state_filename)

    s3_bucket = get_variable(params,'s3-bucket',"")

    # write sites dictionary to the file
    state_str = json.dumps(state, indent=2)

    # make sure dir exists
    state_file_local_path = os.path.basename(state_file_local_path_full)
    
    if not os.path.exists(state_file_local_path):
        os.makedirs(state_file_local_path)

    with open(state_file_local_path_full, 'w') as file_arg_fp:
        file_arg_fp.write(state_str)
            
    # write file to s3
    s3.meta.client.upload_file(state_file_local_path_full, 
        s3_bucket,
        state_file_s3_path)

def get_state_s3_path(params, state_filename):

    # the state of the current set of demo sites lives in the sites.json
    # file in the s3 bucket associated with this instance.

    service_alias = get_variable(params,'service-alias',"")
    env = get_variable(params,'env',"")

    return "%s/%s/%s"%(service_alias,env,state_filename)

def get_state_local_path(params, state_filename):

    home = os.path.expanduser("~")
    service_alias = get_variable(params,'service-alias',"")
    env = get_variable(params,'env',"")
    state_file_local_path = os.path.join(home,'.yac',service_alias,env)
    state_file_local_path_full = os.path.join(state_file_local_path,state_filename)

    # make sure local path exists
    if not os.path.exists(state_file_local_path):
        os.makedirs(state_file_local_path)

    return state_file_local_path_full