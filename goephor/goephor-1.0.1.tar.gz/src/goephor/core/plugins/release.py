'''
Created on May 12, 2016

@author: iitow
'''
from pluginable import Plugin
from modules.log import message
import datetime
import yaml
import json


class utils(Plugin):
    ''' Helper plugin for obtaining release info
    '''
    def __init__(self, action_manager):
        '''
        utils Constructor
        :param action_manager: Obj, from action_manager class
        '''
        self.action_manager = action_manager
        Plugin.__init__(self, self.action_manager)

    def date(self,
             prefix,
             **defaults):
        '''
        get the current date

        :param prefix: %m/%d/%y"
        :example:
        ```
        - release.utils.date:
           - '%m/%d/%y'
        ```
        '''
        date = datetime.datetime.now().strftime(prefix)
        if self.verbose:
            print message('info',"[date] %s" % (str(date)),debug=self.debug)
        return date
    
    def pad(self, text, fill, amount, **defaults):
        '''
        Provides generic padding to numbers and strings
        
        :param text: String
        :param fill: Char
        :param amount: Int
        :return: String
        :example:
        ```
        - release.utils.pad:
           - '9'
           - '0'
           - 3
           - set_env: "PAD"
        ```
        '''
        output = text.rjust(amount,fill)
        if self.verbose:
            print message('info',"[pad] is %s" % (str(output)),debug=self.debug)
        return output

    def compare(self,
                new,
                old):
        '''
        Private, compare release numbers
        :param new: String, new release
        :param old: String, old release
        :note: Assume the last digit is build number
        so we split it off
        :example:
        '''
        old = old.rsplit('.', 1)[0]
        if new == old:
            return True
        return False

    def next(self,
             path,
             new_release):
        '''
        Get the next available release from Release.json
        for a given build
        :param path: String, path to Releases.json
        :param new_release: String, release name 7.1.1
        :note: will only use first three positions
        :example:
        ```
        - release.utils.next:
           - './Release.json'
           - '7.1.1'
           - set_env: "NEXT_REL"
        ```
        '''
        if len(new_release.split('.')) > 3:
            new_split = new_release.rsplit('.', 1)
            new_release = new_split[0]
            print message('info',"[info] compare using %s" % new_release,debug=self.debug)
        file_type = path.rsplit(".", 1)[1]
        try:
            with open(path) as file:
                if 'json' in file_type:
                    releases = json.loads(file.read())
                else:
                    releases = yaml.load(file)
        except Exception:
            error = "unable to read %s" % (path)
            raise Exception(error)
        minor = 0
        for name, values in releases.iteritems():
            if self.compare(new_release, name):
                print message('info',"[match] %s" % name,debug=self.debug)
                old_minor = int(name.rsplit('.', 1)[1])
                if minor < old_minor:
                    minor = old_minor
        if minor >= 0:
            next = "%s.%s" % (new_release, str(minor+1))
        else:
            next = "%s.%s" % (new_release, str(minor))
        print message('info',"[next] %s" % (next),debug=self.debug)
        return next
