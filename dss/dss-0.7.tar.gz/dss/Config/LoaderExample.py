import json
import os.path


# returns Win path  C:\Practicum\core
# or POSIX path     /Users/oxelv/Practicum/core
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PLUGIN_NAME = 'ipconfig'

# C:\Practicum\core\ipconfig\config_temp.json
# /Users/oxelv/Practicum/core/plugins/ipconfig/config_temp.json
PATH_TO_CONFIG = os.path.join(BASE_DIR, 'plugins', PLUGIN_NAME, 'config_temp.json')

if os.path.isfile(PATH_TO_CONFIG):
    with open(PATH_TO_CONFIG) as data_file:
        data = json.load(data_file)

        # Replaces general path with OS' specific path
        for key, value in data['General'].iteritems():
            if 'Is Path Type' in value:
                if value['Is Path Type']:
                    split_path = value['Value'].split('/')
                    final_path = os.path.join(BASE_DIR, *split_path)
                    value['Value'] = final_path

        for key, value in data['Archiving'].iteritems():
            if 'Is Path Type' in value:
                if value['Is Path Type']:
                    split_path = value['Value'].split('/')
                    final_path = os.path.join(BASE_DIR, *split_path)
                    value['Value'] = final_path

        # Now data can be easily accessed like this
        # GENERAL SETTINGS
        print data['General']['Flags']['Value']  # entry
        print data['General']['Parser']['Value']  # entry (smart path)
        print data['General']['Extension']['Selected']  # selected from list

        # ARCHIVING SETTINGS
        print data['Archiving']['Archive Time Interval']['Value']   # entry
        print data['Archiving']['File Format']['Selected']          # selected from list
