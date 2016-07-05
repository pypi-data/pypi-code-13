#!/usr/bin/env python
# encoding: utf-8
"""
dump.py

Created by Geert Dekkers on 2008-06-07.
Copyright (c) 2008 Geert Dekkers Web Studio, 2009, 2010, 2011, 2012, 2013 
Django Web Studio. All rights reserved.

Dumps the default database when it is mysql. 
Preferably to be triggered by a cron job, or launchd on macosx.
Could also be triggered by Scheduler on Windows, but we're not using Windows, are we?

Produces a timestamped dump which could be used for rollback.
Takes app specific settings, to be found in settings.py

To do: build a database-agnostic dump tool

# Required settings
# -----------------
APP_LOGS_ROOT
APP_DUMP_PATH

# Optional settings
# -----------------
APP_MYSQLDUMP_PATH = 'usr/bin' #(path to mysqldump, default is /usr/bin)
APP_DB_ROLLBACKS = 60 #(no. of rollbacks, default 60)

"""
import sys
import os
import datetime
import subprocess
import tarfile
from django.conf import settings
from django.core.management.base import NoArgsCommand


try:
    engine = settings.DATABASES['default']['ENGINE'] 
except:
    engine = settings.DATABASE_ENGINE

if not engine.find('mysql') > -1:
    print 'Only for mysql at the moment, exiting.'
    exit()
 
 
# For compatibility with django < 1.3   
try:
    dbuser = settings.DATABASES['default']['USER']
    dbpwd = settings.DATABASES['default']['PASSWORD']
    dbname = settings.DATABASES['default']['NAME']
except:
    dbuser = settings.DATABASE_USER
    dbpwd = settings.DATABASE_PASSWORD
    dbname = settings.DATABASE_NAME


dump_settings = {
    'log_root' : getattr(settings, 'APP_LOGS_ROOT', None),
    'dump_path': getattr(settings, 'APP_DUMP_PATH', None),
    'mysqlpath': getattr(settings, 'APP_MYSQLDUMP_PATH', '/usr/local/bin'),
    'dbuser': dbuser,
    'dbpwd': dbpwd,
    'dbname': dbname,
    'rollbacks': getattr(settings, 'APP_DB_ROLLBACKS', 60)    
}

# Check input before proceeding
for k, v in dump_settings.items():
    if not v:
        print 'No value for setting %s, exiting' % k
        exit()


#------------------------------------------------------------------------------
# Logging
#
# A "logs" directory will be created the first time this file is run.
#------------------------------------------------------------------------------
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=dump_settings['log_root'] + '/dump.log',
                    filemode='w')
#------------------------------------------------------------------------------

class Command(NoArgsCommand):

    def handle_noargs(self, **options):
    
        """Dumps the app database to disk, tar gzips the dump and deletes the original.
        Then ends by deleting the oldest dumps from the dumps directory."""
    
        # Check for the existence of a dumps dir in the path
    
        if not os.path.exists(dump_settings['dump_path']):
            print 'dump path doesnt exist, exiting...'
            exit()
    
        # Compile the dump filename and path
        dump_name = ''.join(
                            (datetime.datetime.today().isoformat('-')\
                            .replace(":","-").replace("-","").replace(".","-"), ".sql")
                            )
        dump_path = dump_settings['dump_path'] + "/" + dump_name
    
        # Initiate a gzipped tar file object
        tar = tarfile.open(
            dump_settings['dump_path'] + "/" + dump_name.replace(".sql", ".tar.gz"), 'w:gz'
            )
    
        # Compile the command. Use the complete path, because the script will probably be running as root.
        cmd = "%(mysqldump_path)s/mysqldump --user=%(user)s --password=%(password)s %(database)s" % {
            'mysqldump_path': dump_settings['mysqlpath'], 
            'user':dump_settings['dbuser'],
            'password': dump_settings['dbpwd'],
            'database': dump_settings['dbname'],
            'path': dump_settings['dump_path'] 
        }
    
        # Execute the cammand and get the output    
        try:
            proc = subprocess.Popen(cmd.encode('utf-8'),shell=True, stdout=subprocess.PIPE,)
            r = proc.communicate()[0]
            try:
                # Open a file and write the output to it.
                f = open(dump_path, 'w')
                f.write(r)
                try:
                    # Tar the file from disk, remove the dump file
                    tar.add(dump_path)
                    tar.close()
                    logging.info('Dumped database %s as %s' % (dump_settings['dbname'], dump_name))
                    try:
                        os.remove(dump_path)
                    except Exception, inst:
                        logging.error("Error removing file after gzipping %s" % inst)
                except Exception, inst:
                    logging.error("Error tar.gzipping the file %s" % inst)
            except Exception, inst:
                logging.error("Error writing file %s" % inst)
        
                
        except Exception, inst:
            logging.error("An error occurred dumping the database %s" % inst)
    
        # End by removing the last file from the dumps dir.
        # Set number of dumps to keep in the app specific last segment of settings.py
    
        files = os.listdir(dump_settings['dump_path'])
    
        if len(files) > dump_settings['rollbacks']:
            oldest_file = files.pop(0)
            try:
                os.remove(dump_settings['dump_path'] + "/" + oldest_file)
            except Exception, inst:
                logging.error("Error removing oldest file %s" % inst)

