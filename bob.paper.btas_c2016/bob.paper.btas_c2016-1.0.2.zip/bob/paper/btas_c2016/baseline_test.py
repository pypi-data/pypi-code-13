#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Pavel Korshunov <Pavel.Korshunov@idiap.ch>
# Thu  21 Jan 13:56:21 CEST 2016
#
# Copyright (C) 2012-2015 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
A simple baseline anti-spoofing system for the Test set that uses ratios computed from spectrogram as features and
logistic regression as a classifier. This script reads audio files provided for BTAS 2016 anti-spoofing
competition, extract features, train logistic regression classifier on the training set and, by using the
trained classifier, computes scores for the test set. The resulted scores are to be submitted to the organizers of the competition for the evaluation.

Required: to run the script, Bob toolbox (http://idiap.github.io/bob/), numpy, and scipy are required.
"""

import bob.measure

import sys
import os
import argparse

import numpy
import scipy.io.wavfile
import os.path
import math

import antispoofing.utils.db
import bob.ap
import bob.bio.spear
import bob.io.base
import antispoofing.utils.ml

# setup logging
import bob.core
logger = bob.core.log.setup("BTASLogger")


def read_sample(filename):
    """
    Use scipy to read a given WAV sample
    :param filename: path to WAV sample
    :return: rate in Hz and data cast to float
    """
    if not os.path.isfile(filename):
        logger.error('This sample file does not exist: %s', filename)
        return [None, None]
    #  read the audio file
    rate, audio = scipy.io.wavfile.read(filename)
    # We consider there is only 1 channel in the audio file => data[0]
    data = numpy.cast['float'](audio)

    return rate, data


def compute_VAD(rate, data, win_length=20.0, win_shift=10.0):
    """
    Optional function, not used in this baseline.
    For VAD description, please see
    https://www.idiap.ch/software/bob/docs/latest/bioidiap/bob.bio.spear/master/implemented.html#bob.bio.spear.preprocessor.Mod_4Hz
    :return: VAD labels (either 0 or 1) for each frame
    """
    #  apply VAD based on 4Hz, skip empty sample
    if data is None or not data.size:
        return numpy.zeros(2, dtype=numpy.int8)
    # use Bob's VAD detection based on 4Hz modulation
    preprocessor = bob.bio.spear.preprocessor.Mod_4Hz(win_length_ms=win_length, win_shift_ms=win_shift)
    [labels, energies, mod_4hz] = preprocessor.mod_4hz([rate, data])

    # return computed labels
    return labels


#  compute energy in bands smoothed with either linear or mel-filters
def compute_spectrogram(rate, data, win_length=20.0, win_shift=10.0, freq_max=8000, n_filters=20, pre_emph=1.0, mel_scale=False):
    """
    For parameters description, please see documentation about Spectrogram at:
    https://www.idiap.ch/software/bob/docs/latest/bioidiap/bob.ap/master/py_api.html#bob.ap.Spectrogram
    """
    if not rate:
        return None
    if data is None or not data.size:
        return None

    #  in bob, energy bands computation is in Spectrogram function
    c = bob.ap.Spectrogram(rate, win_length_ms=win_length, win_shift_ms=win_shift, n_filters=n_filters,
                           f_min=0.0, f_max=freq_max, pre_emphasis_coeff=pre_emph, mel_scale=mel_scale)
    # energy power spectrum
    c.energy_filter = True  # ^2 of FFT spectrum
    # we take no log
    c.log_filter = False
    c.energy_bands = True  # band filtering

    spectrogram = c(data)
    logger.debug("Spectrogram's shape {0}".format(spectrogram.shape))
    return spectrogram


def preprocessing(sample_obj, db_directory, feature_directory, n_bands,
                  win_length=20.0, win_shift=10.0, freq_max=8000, pre_emph=1.0, mel_scale=False):
    """
    Prepare sample for feature extraction. In this implementation, we just compute a Spectrogram
    For parameters description, please see documentation about Spectrogram at:
    https://www.idiap.ch/software/bob/docs/latest/bioidiap/bob.ap/master/py_api.html#bob.ap.Spectrogram
    :return: spectrogram of the input audio sample
    """
    input_file = sample_obj.make_path(directory=db_directory, extension='.wav')
    logger.info("Preprocessing file: %s" % input_file)

    # do not recompute features if they are already saved in HDF5 file
    spectrogram = None
    try:
        spectrogram = sample_obj.load(directory=feature_directory, extension='.hdf5')
    except RuntimeError:
        logger.debug("Preprocessing: the file with pre-processed results does not exist, "
                     "commencing pre-processing routine ...")

    if spectrogram is not None and spectrogram.any():
        logger.debug("Preprocessing: pre-processed results for this file already exist, "
                     "so skipping the computations ...")
        return spectrogram

    [rate, data] = read_sample(input_file)
    if rate is None or data is None:
        logger.warn('A file sample %s is corrupt of does not exist. Preprocessing is stopped.', input_file)
        return None
    # VAD detection can be used, if necessary
    # we do not need it in this simple baseline
    # vad_labels = compute_VAD(rate, data, win_length=win_length, win_shift=win_shift)
    spectrogram = compute_spectrogram(rate, data, win_length=win_length, win_shift=win_shift, freq_max=freq_max,
                                      n_filters=n_bands, pre_emph=pre_emph, mel_scale=mel_scale)

    # potentially, some processing can be done with the spectrogram
    filtered_spectrogram = spectrogram

    logger.debug("Preprocessing: filtered bands shape: %s", str(filtered_spectrogram.shape))

    # save the spectrogram for the future use, so we do not recompute every time we run the script
    sample_obj.save(filtered_spectrogram.reshape([1, filtered_spectrogram.size]), directory=feature_directory, extension='.hdf5')

    return filtered_spectrogram


def extraction(sample_obj, feature_directory, preprocessed_features, n_bands, n_ratios):
    """
    This extraction computes ratios between mean values of the neighboring bands in the sample's spectrogram
    :param sample_obj: database object of an audio sample
    :param feature_directory: the directory where the extracted ratios are saved for the future re-use
    :param preprocessed_features: spectrogram of the audio sample computed at the pre-processing step is expected
    :param n_bands: the number of bands in the spectrogram
    :param n_ratios: the number of ratios we want to compute from the spectrogram bands
    :return: Computed ratios
    """
    # do not recompute features if they are already saved in HDF5 file
    ratios = None
    try:
        ratios = sample_obj.load(directory=feature_directory, extension='.hdf5')
    except RuntimeError:
        logger.debug("Extraction: the file with extractded results does not exist, commencing extraction routine ...")

    if ratios is not None and ratios.any():
        logger.debug("Extraction: extracted features already exist, so skipping the computations ...")
        return ratios[0]

    band_length = math.floor(n_bands/n_ratios)
    # first, add ratio between the highest and lowest band
    lower_band = preprocessed_features[:, 0:band_length]
    higher_band = preprocessed_features[:, -band_length:]
    ratios = [numpy.mean(lower_band)/numpy.mean(higher_band)]
    for i in range(1, n_ratios):
        higher_band = preprocessed_features[:, i*band_length:(i+1)*band_length]
        ratios.append(numpy.mean(lower_band)/numpy.mean(higher_band))
        lower_band = higher_band

    ratios = numpy.asarray(ratios, dtype=numpy.float64)
    logger.debug("Extraction: number of ratios: %s", str(ratios.shape))
    # save the spectrogram for the future use
    sample_obj.save(ratios.reshape([1, ratios.size]), directory=feature_directory, extension='.hdf5')
    return ratios


def _check_feature(feature, machine=None, projected=False):
    """Checks that the features are appropriate."""
    if not isinstance(feature, numpy.ndarray) or feature.ndim != 1 or feature.dtype != numpy.float64:
        raise ValueError("The given feature is not appropriate", feature)
    index = 1 if projected else 0
    if machine is not None and feature.shape[0] != machine.shape[index]:
        logger.warn("The given feature is expected to have %d elements, but it has %d" % (machine.shape[index], feature.shape[0]))
        return False
    return True


def train_projector(training_features, projector_file):
    """
    Train logistic regression classifier on the pre-computed features
    :param training_features: features computed from the training set
    :param projector_file: the file where the classifier's trained model will be stored
    :return: returns the model of the classifier
    """
    if len(training_features) < 2:
        raise ValueError(" - Training: features should contain two lists: real and attack!")

    logger.info(" - Training: number of real features %d", len(training_features[0]))
    logger.info(" - Training: number of attack features %d", len(training_features[1]))
    real_features = numpy.array([feat if _check_feature(feat) else numpy.nan for feat in training_features[0]], dtype=numpy.float64)
    attack_features = numpy.array([feat if _check_feature(feat) else numpy.nan for feat in training_features[1]], dtype=numpy.float64)

    # save the trained model to file for future use
    hdf5file = bob.io.base.HDF5File(projector_file, "w")

    from antispoofing.utils.ml import norm

    # normalize the features
    mean, std = norm.calc_mean_std(real_features, attack_features, nonStdZero=True)
    real_features = norm.zeromean_unitvar_norm(real_features, mean, std)
    attack_features = norm.zeromean_unitvar_norm(attack_features, mean, std)

    # create Logistic Regression Machine
    trainer = bob.learn.linear.CGLogRegTrainer()

    # train the machine using the provided training data
    # negative features go first, positive - second
    machine = trainer.train(attack_features, real_features)

    # if we use PCA, PCA machine is normalizing features already
    if mean is not None and std is not None:
        machine.input_subtract = mean
        machine.input_divide = std

    logger.debug(" - Training: machine shape: %s", str(machine.shape))
    logger.debug(" - Training: machine weights: %s", str(machine.weights))

    hdf5file.cd('/')
    hdf5file.create_group('LogRegProjector')
    hdf5file.cd('LogRegProjector')
    machine.save(hdf5file)
    logger.info(" - Training: saved classifier model into file %s", projector_file)
    return machine


def load_projector(projector_file):
    """
    Loads classifier's model from the given file
    :param projector_file:
    :return:
    """
    hdf5file = bob.io.base.HDF5File(projector_file)
    # read LogRegr Machine model
    hdf5file.cd('/LogRegProjector')
    return bob.learn.linear.Machine(hdf5file)


def project_feature(machine, feature):
    """
    Project a given feature on the classifier's model.
    :param machine: Classifier's model
    :param feature: feature vector for a single audio sample
    :return: For this system, the result is the classification score for the feature
    """
    feature = numpy.asarray(feature, dtype=numpy.float64)
    if _check_feature(feature, machine=machine):
        # Projects the data using LogRegression classifier
        projection = machine(feature)
        return projection
    return numpy.zeros(1, dtype=numpy.float64)


def compute_features(sample_objects, data_directory, preprocess_directory, extraction_directory, n_bands, n_ratios,
                     win_length=20.0, win_shift=10.0, freq_max=8000, pre_emph=1.0, mel_scale=False):
    """
    Compute features for all database sample objects (i.e., audio samples). For pre-processign parameters see
    https://www.idiap.ch/software/bob/docs/latest/bioidiap/bob.ap/master/py_api.html#bob.ap.Spectrogram
    :param sample_objects: database objects for a set of audio samples
    :param data_directory: the root of directory where audio files are stored
    :param preprocess_directory: where, once computed, spectrograms will be stored
    :param extraction_directory: where, once computed, features will be stored
    :param n_bands: the number of bands in the spectrogram
    :param n_ratios: the number of ratios we want to compute from the spectrogram bands
    :return: vector of the computed features
    """
    features = []
    logger.info("Computing features for %d files", len(sample_objects))
    # process each audio file
    for obj in sample_objects:
        spectrogram = preprocessing(obj, data_directory, preprocess_directory, n_bands, win_length=win_length,
                                    win_shift=win_shift, freq_max=freq_max, pre_emph=pre_emph, mel_scale=mel_scale)
        if spectrogram is None:  # if cannot compute spectrogram from this file, give up
            return None
        features.append(extraction(obj, extraction_directory, spectrogram, n_bands, n_ratios))
    return features


def compute_scores(objects, features, scores_directory, machine, settype='test'):
    """
    Compute the scores database sample objects (i.e., audio samples)
    :param objects: data samples
    :param features: pre-computed features
    :param scores_directory: where to write the scores
    :param machine: Classifier's model
    :param settype: 'eval' for test set
    :return: vectors with scores for real and attacks
    """
    if features is None:
        logger.error('Features for set "%s" are empty, so not scores are computed!', settype)
        return None
    #
    # write two files, one with two columns "file score" - this one should be submitted to competition
    # and another with four columns "id type file score" - this can be used to compute EER using bob.measure
    #
    score_file = os.path.join(scores_directory, 'scores-' + settype + '.txt')
    bob.io.base.create_directories_safe(os.path.dirname(score_file))
    f = open(score_file, 'w')
    score_file_fourcolumns = os.path.join(scores_directory, 'scores-' + settype + '-fourcolumns.txt')
    bob.io.base.create_directories_safe(os.path.dirname(score_file_fourcolumns))
    fcolumns = open(score_file_fourcolumns, 'w')

    logger.info("Computing scores and saving them to %s", score_file)
    # first compute real scores and write them into two differently formatted score file
    scores = []
    for i, obj in enumerate(objects):
        file_path = str(obj.make_path())
        score = project_feature(machine, features[i])
        id_str = (str(obj.get_client_id())).zfill(3)
        f.write("%s %.20f\n" % (file_path, score))
        fcolumns.write("%s %s %s %.20f\n" % (id_str, id_str, file_path, score))
        scores.append(score[0])
    f.close()
    fcolumns.close()
    return scores


def main():

    basedir = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))

    # some default parameters for the spectrogram computation
    # for the explanation of the parameters and for other possible values, please refer to the documentation here:
    # https://www.idiap.ch/software/bob/docs/latest/bioidiap/bob.ap/master/py_api.html#bob.ap.Spectrogram
    win_length = 20.0
    win_shift = 10.0
    freq_max = 8000
    pre_emph = 1.0
    mel_scale = False

    INPUT_DIR = os.path.join(basedir, 'database')
    OUTPUT_DIR = os.path.join(basedir, 'features')

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     conflict_handler='resolve')
    parser.add_argument('-n', '--input-dir', metavar='DIR', type=str, dest='inputdir', default=INPUT_DIR,
                        help='Base directory containing the audio files of the database (defaults to "%(default)s")')
    parser.add_argument('-d', '--directory', metavar='DIR', type=str, dest='directory', default=OUTPUT_DIR,
                        help='The output directory (defaults to "%(default)s")')
    parser.add_argument('-t', '--skip-training', action='store_true',
                        help='If you want to skip training (defaults to "%(default)s")')
    parser.add_argument('-e', '--skip-evaluation', action='store_true',
                        help='If you want to skip classification and score computation (defaults to "%(default)s")')
    parser.add_argument('-b', '--filter-bands', type=int, default=40,
                        help='The number if filter bands used in spectrogram computation (defaults to "%(default)s")')
    parser.add_argument('-r', '--ratios-number', type=int, default=10,
                        help='How many ratios will be computed from the spectrogram (defaults to "%(default)s")')

    #######
    # Database specific configuration
    #######
    antispoofing.utils.db.Database.create_parser(parser, implements_any_of='audio')

    # add verbose option
    bob.core.log.add_command_line_option(parser)
    args = parser.parse_args()
    # set verbosity level
    bob.core.log.set_verbosity_level(logger, args.verbose)

    # create temporary processing directories
    preprocess_directory = os.path.join(args.directory, 'preprocess')
    extraction_directory = os.path.join(args.directory, 'extraction')
    projector_file = os.path.join(args.directory, 'projector.hdf5')

    # init database with its own arguments
    database = args.cls(args)

    n_bands = args.filter_bands
    n_ratios = args.ratios_number
    args.inputdir = os.path.join(basedir, args.inputdir)  # append input dir with current dirictory
    
    machine = None
    real_features = []
    attack_features = []
    if not args.skip_training:
        # get genuine (real) and spoofed (attacks) data
        real_objects, attack_objects = database.get_train_data()
        if real_objects == [] or attack_objects == []:
            logger.info('Training set is empty, so a classifier cannot be trained.')
        else:
            logger.info('Starting to compute features for the Train set')
            # compute features for genuine data from the training set
            real_features = compute_features(real_objects, args.inputdir, preprocess_directory, extraction_directory,
                                             n_bands, n_ratios, win_length, win_shift, freq_max, pre_emph, mel_scale)
            # compute features for attacks from the training set
            attack_features = compute_features(attack_objects, args.inputdir, preprocess_directory, extraction_directory,
                                               n_bands, n_ratios, win_length, win_shift, freq_max, pre_emph, mel_scale)

        # train the classifier from the computed features
        machine = []
        try:
            machine = load_projector(projector_file)
            logger.info("Do not train the classifier, since found and "
                        "loaded pre-trained classifier model from file %s", projector_file)
        except RuntimeError:
            logger.debug("The classifier model does not exist, hence, start training it...")

        # train classifier only if it does not exist and we have features from the train set
        if not (real_features == [] or attack_features == []):
            if not machine:
                machine = train_projector([real_features, attack_features], projector_file)
        else:
            logger.info("No features are available to train the classifier!")

    if not args.skip_evaluation:
        # all test data are randomized and recorded in the database as real features (just for convenience)
        test_objects, _ = database.get_test_data()
        if test_objects == []:
            print ('Evaluation set is empty, so skipping the classification and score computation')
            print ("I'm done running!")
            return

        logger.info('Starting to compute features for the Test (Evaluation) set')
        # compute features for data from the test set
        test_features = compute_features(test_objects, args.inputdir, preprocess_directory, extraction_directory,
                                           n_bands, n_ratios, win_length, win_shift, freq_max, pre_emph, mel_scale)

        # make sure we have the classifier available
        if not machine:
            # load the classifier from the file
            try:
                machine = load_projector(projector_file)
                logger.info("Found and loaded the classifier model from file %s", projector_file)
            except RuntimeError:
                print ("The classifier model does not exist, you need to train it "
                             "before trying to run score computation. Exiting ...")
                print ("I'm done running!")
                return

        # compute scores for the all samples from the Evaluation set
        test_scores = compute_scores(test_objects, test_features, args.directory, machine, settype='test')

    print ("I'm done running!")

if __name__ == '__main__':
    main()

