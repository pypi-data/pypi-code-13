'''
Created on Apr 27, 2016

:author: iitow
'''
from pluginable import Plugin
from modules.log import message
import yaml
import json


class maker(Plugin):
    ''' Receipt creator tasks go here
    '''
    def __init__(self, action_manager):
        '''
        maker Constructor
        :param action_manager: Obj, from action_manager class
        '''
        self.action_manager = action_manager
        Plugin.__init__(self, self.action_manager)

    def is_json(self,data,**defaults):
        '''
        Is string json?
        
        :param data: String
        :return: Boolean
        :example:
        ```
        - string.utils.is_json:
            - data
            - set_env: SOMEVAL
        ```
        '''
        try:
            json_object = json.loads(data)
        except ValueError:
            return False
        return True

    def on_actions(self, path, **defaults):
        '''
        This creates a receipt of all actions in the chain

        :param path: String, system path to put receipt
        :param defaults: additional params
        :example:
        ```
        - receipt.maker.on_actions:
            - "./receipt.yaml"
        ```
        '''
        print message('info',"[on_actions] %s" % (path),debug=self.debug)
        receipt = {}
        receipt["results"] = []
        for action in self.action_manager.chain:
            result = action.get_receipt()
            receipt.get("results").append(result)
        self._to_file(receipt, path)

    def custom(self, path, **defaults):
        '''
        Create a custom receipt from key/value pairs in defaults

        :param path: String, system path to put receipt
        :param defaults: additional params
        :example:
        ```
        - receipt.maker.custom:
            - "./receipt.yaml"
            - var1: "SOMEVALUE1"
            - var2: "SOMEVALUE2"
            - var3: "SOMEVALUE3"
        ```
        '''
        print message('info',"[custom] %s" % (path),debug=self.debug)
        for key, value in defaults.iteritems():
            print message('info',"%s: %s" % (key, value),debug=self.debug)
        self._to_file(defaults, path)

    def custom_json(self, path, data,**defaults):
        '''
        produces output file from json data
        :param path: String
        :param data: String
        :example:
        ```
        - receipt.maker.custom_json:
            - path/put/file
            - somejsonhere
        ```
        '''
        if self.is_json(data):
            data = json.loads(data)
            if self.verbose:
                print message('info',"[custom_json] @ %s" % (path),debug=self.debug)
                print message('info'," %s" % (str(data)),debug=self.debug)
                self._to_file(data, path)
        else:
            raise Exception('Must be well formed json string')

    def read(self, path, **defaults):
        '''
        Reads in a custom receipt and generates environment variables
        :param defaults: additional params
        :note: Consumes only files from a custom receipt
        :example:
        ```
        - receipt.maker.read:
           - "receipt.yaml"
        ```
        '''
        print message('info',"[read] %s" % path,debug=self.debug)

        data = self._to_dict(path)
        for key, value in data.iteritems():
            self.EnvManager.set(key, value)
            if self.verbose:
                print message('info',"[set] %s=%s" % (key, value),debug=self.debug)

    def add(self,
            path,
            json_str,
            **defaults):
        '''
        Add to an existing receipt
        :param path: String, path to existing file
        :param json_str: String, using json syntax add to receipt
        :param to_json: Boolean, write file out as json
        :note: json syntax, {hello:{world}}
        :example:
        ```
       - receipt.maker.add:
                        - "./custom.yaml"
                        - '{"HELLO":["WORLD","05/10/14"]}'
        ```
        '''
        data = None
        print message('info',"[add] %s" % path,debug=self.debug)
        data = self._to_dict(path)
        json_dict = self._str_to_dict(json_str)
        data.update(json_dict)
        self._to_file(data, path)

    def _to_dict(self, path):
        '''
        Private, Load a file in and output a dict

        :param path: String
        :param is_string: String path is a string do not load file
        :return: Dictionary
        '''
        file_type = path.rsplit(".", 1)[1]
        with open(path) as file:
            if 'json' in file_type:
                if self.verbose:
                    print message('info',"[_to_dict] json",debug=self.debug)
                data = json.loads(file.read())
                return data
            else:
                if self.verbose:
                    print message('info',"[_to_dict] yaml",debug=self.debug)
                data = yaml.load(file)
                return data
        print message('info',"[None]",debug=self.debug)
        return None

    def _str_to_dict(self, data):
        '''
        Convert json string to dict
        :param data: String
        :return: Dictionary
        '''
        if self.verbose:
            print message('info',"[_str_to_dict] %s" % (data),debug=self.debug)
        data = json.loads(data)
        return data

    def _to_file(self,
                 data,
                 path):
        '''
        Private, convert dict to file

        :param path: String
        '''
        file_type = path.rsplit(".", 1)[1]
        with open(path, 'w') as file:
            if 'json' in file_type:
                if self.verbose:
                    print message('info',"[_to_file] json",debug=self.debug)
                file.write(json.dumps(data,
                                      indent=4,
                                      sort_keys=True))
            elif 'txt' in file_type:
                if self.verbose:
                    print message('info',"[_to_file] txt",debug=self.debug)
                for key, value in data.iteritems():
                    pair = "%s=%s\n" % (key, value)
                    file.write(pair)
            else:
                if self.verbose:
                    print message('info',"[_to_file] yaml",debug=self.debug)
                file.write(yaml.dump(data,
                                     default_flow_style=False,
                                     allow_unicode=True))
