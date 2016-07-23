import re, boto3, os, json, jmespath, sys, argparse
from yac.lib.variables import get_variable, set_variable

# state is persisted in a json file in s3
def load_state_s3(s3_bucket, s3_path, service_alias):

    sites = {}

    s3 = boto3.resource('s3')

    state_filename = get_state_filename(service_alias)

    state_file_local_path_full = get_state_local_path(s3_path,service_alias)

    s3_file_path = "%s/%s"%(s3_path,state_filename)

    # pull file down to the local dir
    s3.meta.client.download_file(s3_bucket, 
                                 s3_file_path, 
                                 state_file_local_path_full)

    # pull contents into a dictionary
    if os.path.exists(state_file_local_path_full):
        with open(state_file_local_path_full) as file_arg_fp:
            file_contents = file_arg_fp.read()
            state = json.loads(file_contents)

    return state

def save_state_s3(s3_bucket, s3_path, service_alias, state):

    s3 = boto3.resource('s3')

    state_file_local_path_full = get_state_local_path(s3_path, service_alias)

    # write state dictionary to the file
    state_str = json.dumps(state, indent=2)

    # make sure dir exists
    state_file_local_path = os.path.basename(state_file_local_path_full)
    
    if not os.path.exists(state_file_local_path):
        os.makedirs(state_file_local_path)

    with open(state_file_local_path_full, 'w') as file_arg_fp:
        file_arg_fp.write(state_str)
        
    state_filename = get_state_filename(service_alias)            
    s3_file_path = "%s/%s"%(s3_path,state_filename)

    # write file to s3
    s3.meta.client.upload_file(state_file_local_path_full, 
                               s3_bucket,
                               s3_file_path)

def get_state_filename(service_alias):

    state_filename = "%s-state.json"%(service_alias)

    return state_filename

def get_state_local_path(s3_path,service_alias):

    home = os.path.expanduser("~")
    state_file_local_path = os.path.join(home,'.yac',s3_path)
    state_filename = get_state_filename(service_alias)
    state_file_local_path_full = os.path.join(state_file_local_path,state_filename)

    # make sure local path exists
    if not os.path.exists(state_file_local_path):
        os.makedirs(state_file_local_path)

    return state_file_local_path_full