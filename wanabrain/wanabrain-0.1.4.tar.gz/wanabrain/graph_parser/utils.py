import unicodedata
import shutil
import os
import glob

def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

def transfer_files():

    working_directory = '/home/leo/Desktop/graph_test/'

    dst = os.path.join(os.path.dirname(__file__), '../resources/tags/')
    shutil.copyfile(working_directory + 'network/deploy.prototxt', dst + 'deploy.prototxt')

    dst = os.path.join(os.path.dirname(__file__), '../resources/tags/onto.graphml')
    shutil.copyfile(working_directory + 'onto.graphml', dst)

    if not os.path.exists(os.path.join(os.path.dirname(__file__), '../resources/tags/weights/')):
        os.makedirs(os.path.join(os.path.dirname(__file__), '../resources/tags/weights/'))

    if not os.path.exists(os.path.join(os.path.dirname(__file__), '../resources/tags/thresholds/')):
        os.makedirs(os.path.join(os.path.dirname(__file__), '../resources/tags/thresholds/'))

    for dir in os.listdir(working_directory):

        if os.path.isdir(os.path.join(working_directory, dir)):

            if os.path.exists(os.path.join(working_directory, dir + '/training')) and os.path.exists(os.path.join(working_directory, dir + '/eval')):

                dst = os.path.join(os.path.dirname(__file__), '../resources/tags/weights/' + dir + '.caffemodel')
                src = glob.glob(os.path.join(working_directory, dir + '/training/*.caffemodel'))
                shutil.copyfile(src[0], dst)

                dst = os.path.join(os.path.dirname(__file__), '../resources/tags/thresholds/' + dir + '.pkl')
                src = os.path.join(working_directory, dir + '/eval/thresholds.pkl')
                shutil.copyfile(src, dst)

if __name__ == '__main__':

    transfer_files()