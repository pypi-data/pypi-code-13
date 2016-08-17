from mpl_toolkits.axes_grid1 import host_subplot
from sklearn.metrics import roc_curve, precision_score, recall_score
from matplotlib.backends.backend_pdf import FigureCanvasPdf as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import threading
import pickle
import re
import glob
import os
import sys
import settings
import lmdb

sys.path.insert(0, settings.caffe_root + 'python')
import caffe

PATIENCE = 5

class NetworkEvaluator():

    def __init__(self):

        self.ps = []

    def draw_roc_curve(self, gtlist, probas, iter, best_output, working_directory, classes):

        chosen_thresholds = []
        for key, label in enumerate(classes):

            label_gtlist = gtlist[:, key, ]
            label_probas = probas[:, key]

            fpr, tpr, thresholds = roc_curve(label_gtlist, label_probas)

            best_id = np.min(np.where(tpr > 0.75)[0].astype(int))

            best_threshold = thresholds[best_id]
            chosen_fpr = fpr[best_id]
            chosen_tpr = tpr[best_id]
            chosen_thresholds.append(best_threshold)

            fig = plt.figure()
            canvas = FigureCanvas(fig)
            ax = fig.add_subplot(1, 1, 1)
            ax.plot(fpr, tpr)
            plt.title('ROC curve for ' + str(label))
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            fig.savefig(working_directory + 'eval/roc_' + label + '.jpg')

            estlist = (label_probas > best_threshold).astype(int)
            precision = precision_score(label_gtlist, estlist)
            recall = recall_score(label_gtlist, estlist)

            with open(working_directory + 'eval/report.txt', "ab") as report:
                report.write(label + ' : \r\n')
                report.write('Probability threshold chosen : ' + str(best_threshold) + '\r\n')
                report.write('FPR : ' + str(chosen_fpr) + '\r\n')
                report.write('TPR : ' + str(chosen_tpr) + '\r\n')
                report.write('Precision : ' + str(precision) + '\r\n')
                report.write('Recall : ' + str(recall) + '\r\n')
                report.write('\r\n')
            report.close()
        report = open(working_directory + 'eval/report.txt', "ab")
        report.write('Best iter : ' + str(iter) + '\n')
        if best_output != None:
            report.write('Best Output : ' + str(best_output) + '\n')
        report.close()
        pickle.dump(chosen_thresholds, open(working_directory + 'eval/thresholds.pkl', 'w'))

    def learning_curves(self, working_directory):

        f = open(working_directory + '/output.txt', 'r')

        training_iterations = []
        training_loss = []

        test_iterations = []
        test_accuracy = []
        test_loss = []

        # model = working_directory.split('/')[1]
        model = 'deep_residual'

        if model == 'googlenet':
            test_loss2 = []
            test_loss3 = []
            cpt = 1

        for line in f:

            if 'Test net output #0' in line:
                loss = float(line.strip().split(' = ')[-1].split(' ')[0])
                test_loss.append(loss)

            elif 'Test net output #1' in line:
                loss = float(line.strip().split(' = ')[-1].split(' ')[0])
                test_loss2.append(loss)

            elif 'Test net output #2' in line:
                loss = float(line.strip().split(' = ')[-1].split(' ')[0])
                test_loss3.append(loss)

            if 'Train net output' in line:
                loss = float(line.strip().split(' = ')[-1].split(' ')[0])
                training_loss.append(loss)

            if '] Iteration ' in line and 'Testing net (#0)' in line:
                arr = re.findall(r'ion \b\d+\b,', line)
                test_iterations.append(int(arr[0].strip(',')[4:]))

            if '] Iteration ' in line and 'loss = ' in line:
                arr = re.findall(r'ion \b\d+\b,', line)
                training_iterations.append(int(arr[0].strip(',')[4:]))

        print 'train iterations len: ', len(training_iterations)
        print 'train loss len: ', len(training_loss)
        print 'test loss len: ', len(test_loss)
        print 'test iterations len: ', len(test_iterations)
        print 'test accuracy len: ', len(test_accuracy)

        f.close()

        host = host_subplot(111)  # , axes_class=AA.Axes)
        plt.subplots_adjust(right=0.75)

        par1 = host.twinx()

        host.set_xlabel("iterations")
        host.set_ylabel("loss")
        # par1.set_ylabel("validation accuracy")

        p1, = host.plot(training_iterations, training_loss, label="training loss")


        if model == 'alexnet':
            p2, = host.plot(test_iterations, test_loss, label="validation loss")
            # p3, = host.plot(test_iterations, test_accuracy, label="validation accuracy")
            best_test_loss = test_loss
            best_output = None

        elif model == 'deep_residual':
            p2, = host.plot(test_iterations, test_loss, label="validation loss")
            best_test_loss = test_loss
            best_output = None

        elif model == 'googlenet':

            min1 = min(test_loss)
            min2 = min(test_loss2)
            min3 = min(test_loss3)

            if min1 < min2 and min1 < min3:
                best_test_loss = test_loss
                best_output = 1
            elif min2 < min1 and min2 < min3:
                best_test_loss = test_loss2
                best_output = 2
            elif min3 < min1 and min3 < min1:
                best_test_loss = test_loss3
                best_output = 3
            elif min2 == min3:
                best_test_loss = test_loss2
                best_output = 2
            elif min1 == min2:
                best_test_loss = test_loss2
                best_output = 2
            elif min1 == min3:
                best_test_loss = test_loss3
                best_output = 3

            p2, = host.plot(test_iterations, best_test_loss, label="validation loss")
            # p3, = host.plot(test_iterations, test_loss2, label="validation loss 2")
            # p4, = host.plot(test_iterations, test_loss3, label="validation loss 3")

        host.legend(loc=0)

        host.axis["left"].label.set_color(p1.get_color())
        # par1.axis["right"].label.set_color(p2.get_color())

        plt.draw()
        plt.savefig(working_directory + '/eval/learning_curves.jpg')

        with open(working_directory + 'network/solver.prototxt', 'r') as solver_file:

            for line in solver_file:
                if 'test_interval' in line:
                    interval = int(line.split(' ')[-1])

        return (np.argmin(best_test_loss) + 1) * interval, best_output

    def eval_network(self, working_directory, labels):

        # self.set_directory_structure(working_directory + '/output.txt')
        if not os.path.exists(working_directory + '/eval'):
            os.makedirs(working_directory + '/eval')

        best_iter, best_output = self.learning_curves(working_directory)

        net = caffe.Net(working_directory + 'network/valnet.prototxt',
                        working_directory + 'training/snapshot_iter_' + str(best_iter) + '.caffemodel',
                        caffe.TEST)

        net.forward()

        gtlist = net.blobs['label'].data.astype(np.int)
        gtlist = np.squeeze(gtlist)

        if best_output != None:
            probas = np.absolute(net.blobs['proba' + str(best_output)].data)
        else:
            probas = np.absolute(net.blobs['proba'].data)

        self.draw_roc_curve(gtlist, probas, best_iter, best_output, working_directory, labels)

    def evaluate_and_get_thresholds(self, working_directory, classes):

        net = caffe.Net(working_directory + '/deploy.prototxt',
                        working_directory + '/weights.caffemodel',
                        caffe.TEST)

        transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
        transformer.set_transpose('data', (2, 0, 1))

        val_images_env = lmdb.open(os.path.dirname(working_directory) + '/val_rush_images', readonly=True)
        val_labels_env = lmdb.open(os.path.dirname(working_directory) + '/val_rush_labels', readonly=True)

        gtlist = []
        probas = []
        with val_images_env.begin() as txn_val_images:
            with val_labels_env.begin() as txn_val_labels:
                images_cursor = txn_val_images.cursor()
                targets_cursor = txn_val_labels.cursor()

                length = txn_val_images.stat()['entries']
                print(length)

                for key, ((key_images, value_images), (key_targets, value_targets)) in enumerate(zip(images_cursor, targets_cursor)):

                    if key == 10000:
                        break

                    datum = caffe.proto.caffe_pb2.Datum()
                    datum.ParseFromString(value_images)
                    flat_img = np.fromstring(datum.data, dtype=np.uint8)
                    img = flat_img.reshape(datum.channels, datum.height, datum.width)
                    img = img.transpose((1, 2, 0))

                    datum = caffe.proto.caffe_pb2.Datum()
                    datum.ParseFromString(value_targets)
                    target = caffe.io.datum_to_array(datum)

                    gtlist.append(target[0][0])

                    transformed_image = transformer.preprocess('data', img)
                    transformed_image = np.reshape(transformed_image, (1, 3, 227, 227))
                    net.blobs['data'].reshape(*transformed_image.shape)
                    net.blobs['data'].data[...] = transformed_image

                    net.forward()

                    proba = np.absolute(net.blobs['proba'].data[0, ...])
                    probas.append(proba)

        gtlist = np.array(gtlist)
        probas = np.array(probas)

        chosen_thresholds = []
        for key, label in enumerate(classes):

            label_gtlist = gtlist[:, key, ]
            label_probas = probas[:, key]

            fpr, tpr, thresholds = roc_curve(label_gtlist, label_probas)

            best_id = np.min(np.where(tpr > 0.7)[0].astype(int))

            best_threshold = thresholds[best_id]
            chosen_fpr = fpr[best_id]
            chosen_tpr = tpr[best_id]
            chosen_thresholds.append(best_threshold)

            # if not os.path.exists('eval'):
            #     os.makedirs('eval')

            fig = plt.figure()
            canvas = FigureCanvas(fig)
            ax = fig.add_subplot(1, 1, 1)
            ax.plot(fpr, tpr)
            plt.title('ROC curve for ' + str(label))
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            fig.savefig(working_directory + '/eval/roc_' + label + '.jpg')

            estlist = (label_probas > best_threshold).astype(int)
            precision = precision_score(label_gtlist, estlist)
            recall = recall_score(label_gtlist, estlist)

            if not os.path.exists(working_directory + '/eval/'):
                os.makedirs(working_directory + '/eval/')

            with open(working_directory + '/eval/report.txt', "ab") as report:
                report.write(label + ' : \r\n')
                report.write('Probability threshold chosen : ' + str(best_threshold) + '\r\n')
                report.write('FPR : ' + str(chosen_fpr) + '\r\n')
                report.write('TPR : ' + str(chosen_tpr) + '\r\n')
                report.write('Precision : ' + str(precision) + '\r\n')
                report.write('Recall : ' + str(recall) + '\r\n')
                report.write('\r\n')
            report.close()

        pickle.dump(chosen_thresholds, open(working_directory + '/eval/thresholds.pkl', 'w'))

    def monitor(self):

        threading.Timer(10.0, self.monitor).start()

        new_ps = [p for p in self.ps if p[0].poll() == None]
        self.ps = new_ps

        for key, p in enumerate(self.ps):

            labels = p[2]
            working_directory = p[1]
            process = p[0]

            old_loss = 100
            cpt = 0
            best_loss = 100
            best_iter = None
            with open(working_directory + "/output.txt", "r") as output_file:
                for line in output_file:

                    if '] Iteration ' in line and 'Testing net (#0)' in line:
                        arr = re.findall(r'ion \b\d+\b,', line)
                        iter = int(arr[0].strip(',')[4:])

                    if 'Test net output #0:' in line:
                        new_loss = float(line.strip().split(' = ')[-1].split(' ')[0])

                        if new_loss < best_loss:
                            best_loss = new_loss
                            best_iter = iter
                            cpt = 0
                        else:
                            cpt += 1

                        if cpt >= PATIENCE:
                            process.kill()

                            models_file = glob.glob(working_directory + '/training/*')

                            for model_file in models_file:

                                if not str(best_iter) in model_file:
                                    os.remove(model_file)
                            self.eval_network(working_directory, labels)
                            break
                        old_loss = new_loss

            # def cmp_iteration(namefile1, namefile2):
            #
            #     iter1 = int(namefile1.split('/')[-1].split('.')[0].split('_')[-1])
            #     iter2 = int(namefile2.split('/')[-1].split('.')[0].split('_')[-1])
            #
            #     return 1 if iter1 > iter2 else -1
            #
            # weights_files = glob.glob(working_directory + 'training/*.caffemodel')
            # weights_files.sort(cmp_iteration)
            #
            # while len(weights_files) > (PATIENCE + 1):
            #     os.remove(weights_files[0])
            #     os.remove(weights_files[0].replace('caffemodel', 'solverstate'))
            #     weights_files.pop(0)

    def add_training(self, p):
        self.ps.append(p)
