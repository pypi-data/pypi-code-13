#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2016-08-04 
# @Author  : Alexa (AlexaZhou@163.com)
# @Link    : 
# @Disc    : 

import sys
import os
import json
import getopt
import pysso.pysso as pysso

help_doc = '''usage: [options] cmd
    [-c filename] write: write default config format into a file
    [-c filename] run: run with config 
    '''

example_config = {
    "bind_ip":"0.0.0.0",
	"port":80,
	"encrypt_seed":"4C26DCC044A543E2A13F63FA872EB90D",
	"database":{
        "host":"127.0.0.1",
        "db":"husky",
        "user":"root",
        "password":"asdffghjkl"
	}
}


def write_example_config( config_name ):
    print(' write_example_config ')

    if os.path.exists( config_name ):
        print('the file already exists')
        sys.exit(1)

    config_dict = example_config
    with open( config_name,'w' ) as f:
        f.write( json.dumps( config_dict, sort_keys=True, indent=4, ensure_ascii=False ) )
        print('write config to %s successed'%config_name)
    

def load_config( config_name ):
    print(' load_config:',config_name)
    config = None
    with open( config_name, 'r' ) as f:
        config = json.load(f)
    
    return config

def exit_with_message( message ):
    print( message )
    print(help_doc) 
    sys.exit(1)


if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], 'c:', []) 
        
    if len(args) != 1:
        exit_with_message('args error') 

    cmd = args[0]
    if cmd not in ['write','run']:
        exit_with_message('args error')

    config_name = './config.json'
    for option, value in opts: 
        #print("option:%s --> value:%s"%(option, value))
        if option == '-c':
            config_name = value
    
    if cmd == 'write':
        write_example_config( config_name )
    else:
        config = load_config( config_name )
        pysso.set_config( config )
        pysso.start_server( )
    
    sys.exit(0)


