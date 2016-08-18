import ConfigParser
import os
config = ConfigParser.ConfigParser()

# config.readfp(open(__file__.replace('pyc', 'ini'), 'r'))
config.readfp(open(os.path.join(os.path.dirname(__file__), 'settings.ini'), 'r'))

caffe_root = os.environ['HOME'] + '/' + config.get('library', 'caffe_root')
key_frames_rushs_path = os.environ['HOME'] + '/' + config.get('data', 'key_frames_rushs_path')
