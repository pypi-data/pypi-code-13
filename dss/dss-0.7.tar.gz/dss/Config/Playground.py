import json
import os.path


# returns Win path  C:\Practicum\core
# or POSIX path     /Users/oxelv/Practicum/core
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PLUGIN_NAME = 'ipconfig'

# C:\Practicum\core\ipconfig\config_temp.json
# /Users/oxelv/Practicum/core/plugins/ipconfig/config_temp.json
PATH_TO_CONFIG = os.path.join(BASE_DIR, 'plugins asd', PLUGIN_NAME, 'config_temp.json')
print PATH_TO_CONFIG

if os.path.isfile(PATH_TO_CONFIG):
    with open(PATH_TO_CONFIG) as data_file:
        data = json.load(data_file)

        # Replaces general path with OS' specific path
        for key, value in data.iteritems():
            if 'Is Path Type' in value:
                if value['Is Path Type']:
                    split_path = value['Value'].split('/')
                    final_path = os.path.join(BASE_DIR, *split_path)
                    value['Value'] = final_path

        # Now data can be easily accessed like this
        print data['File Format']['Selected']
        print data['Archiving Time Interval']['Value']
        print data['Archive Size']['Value']
