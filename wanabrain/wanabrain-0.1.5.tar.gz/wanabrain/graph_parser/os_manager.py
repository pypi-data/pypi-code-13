import os
import shutil
from distutils.dir_util import copy_tree


class OsManager:

    def create_working_directory(self, working_directory, model, labels):

        # if os.path.exists(working_directory):
        #     shutil.rmtree(working_directory)
        # os.makedirs(working_directory)
        fromDirectory = os.path.join(os.path.dirname(__file__), '../resources/networks/' + model)
        toDirectory = working_directory + 'network/'
        copy_tree(fromDirectory, toDirectory)
        os.remove(toDirectory + 'weights.caffemodel')

        os.rename(toDirectory + 'train_val.prototxt', toDirectory + '/old_train_val.prototxt')
        new_train_val = open(toDirectory + '/train_val.prototxt', 'w')
        with open(toDirectory + '/old_train_val.prototxt', 'r') as train_val:
            for line in train_val:
                if 'dynamic_num_output' in line:
                    new_train_val.write(line.replace('dynamic_num_output', str(len(labels))))
                elif '../' in line:
                    new_train_val.write(line.replace('../', working_directory))
                else:
                    new_train_val.write(line)

        new_train_val.close()
        os.remove(toDirectory + '/old_train_val.prototxt')

        os.rename(toDirectory + 'valnet.prototxt', toDirectory + '/old_valnet.prototxt')
        new_valnet = open(toDirectory + '/valnet.prototxt', 'w')
        with open(toDirectory + '/old_valnet.prototxt', 'r') as valnet:
            for line in valnet:
                if 'dynamic_num_output' in line:
                    new_valnet.write(line.replace('dynamic_num_output', str(len(labels))))
                elif '../' in line:
                    new_valnet.write(line.replace('../', working_directory))
                else:
                    new_valnet.write(line)

        new_valnet.close()
        os.remove(toDirectory + '/old_valnet.prototxt')