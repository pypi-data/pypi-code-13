# -*- coding: utf-8 -*-
#
# This file is part of SIDEKIT.
#
# SIDEKIT is a python package for speaker verification.
# Home page: http://www-lium.univ-lemans.fr/sidekit/
#
# SIDEKIT is a python package for speaker verification.
# Home page: http://www-lium.univ-lemans.fr/sidekit/
#    
# SIDEKIT is free software: you can redistribute it and/or modify
# it under the terms of the GNU LLesser General Public License as 
# published by the Free Software Foundation, either version 3 of the License, 
# or (at your option) any later version.
#
# SIDEKIT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with SIDEKIT.  If not, see <http://www.gnu.org/licenses/>.

"""
Copyright 2014-2016 Sylvain Meignier and Anthony Larcher

    :mod:`features_server` provides methods to manage features

"""
import numpy
import logging
import h5py

from sidekit.frontend.features import pca_dct, shifted_delta_cepstral, compute_delta, framing, dct_basis
from sidekit.frontend.vad import label_fusion
from sidekit.frontend.normfeat import cms, cmvn, stg, cep_sliding_norm, rasta_filt
from sidekit.sv_utils import parse_mask


__license__ = "LGPL"
__author__ = "Anthony Larcher & Sylvain Meignier"
__copyright__ = "Copyright 2014-2016 Anthony Larcher"
__maintainer__ = "Anthony Larcher"
__email__ = "anthony.larcher@univ-lemans.fr"
__status__ = "Production"
__docformat__ = 'reStructuredText'


class FeaturesServer(object):
    """
    Management of features. FeaturesServer instances load datasets from a HDF5 files
    (that can be read from disk or produced by a FeaturesExtractor object)
    Datasets read from one or many files are concatenated and processed
    """

    def __init__(self,
                 features_extractor=None,
                 feature_filename_structure=None,
                 sources=None,
                 dataset_list=None,
                 mask=None,
                 feat_norm=None,
                 global_cmvn=None,
                 dct_pca=False,
                 dct_pca_config=None,
                 sdc=False,
                 sdc_config=None,
                 delta=None,
                 double_delta=None,
                 delta_filter=None,
                 context=None,
                 traps_dct_nb=None,
                 rasta=None,
                 keep_all_features=True):
        """
        Initialize a FeaturesServer for two cases:
        1. each call to load will load datasets from a single file. This mode requires to provide a dataset_list
        (lists of datasets to load from each file.
        2. each call to load will load datasets from several files (possibly several datasets from each file)
        and concatenate them. In this mode, you should provide a FeaturesServer for each source, thus, datasets
        read from each source can be post-processed independently before being concatenated with others. The dataset
        resulting from the concatenation from all sources is then post-processed.

        :param features_extractor: a FeaturesExtractor if required to extract features from audio file
        if None, data are loaded from an existing HDF5 file
        :param feature_filename_structure: structure of the filename to use to load HDF5 files
        :param sources: tuple of sources to load features different files (optional: for the case where datasets
        are loaded from several files and concatenated.
        :param dataset_list: string of the form '["cep", "fb", vad", energy", "bnf"]' (only when loading datasets
        from a single file) list of datasets to load.
        :param mask: string of the form '[1-3,10,15-20]' mask to apply on the concatenated dataset
        to select specific components. In this example, coefficients 1,2,3,10,15,16,17,18,19,20 are kept
        In this example,
        :param feat_norm: tpye of normalization to apply as post-processing
        :param global_cmvn: boolean, if True, use a global mean and std when normalizing the frames
        :param dct_pca: if True, add temporal context by using a PCA-DCT approach
        :param dct_pca_config: configuration of the PCA-DCT, default is (12, 12, none)
        :param sdc: if True, compute shifted delta cepstra coefficients
        :param sdc_config: configuration to compute sdc coefficients, default is (1,3,7)
        :param delta: if True, append the first order derivative
        :param double_delta: if True, append the second order derivative
        :param delta_filter: coefficients of the filter used to compute delta coefficients
        :param context: add a left and right context, default is (0,0)
        :param traps_dct_nb: number of DCT coefficients to keep when computing TRAP coefficients
        :param rasta: if True, perform RASTA filtering
        :param keep_all_features: boolean, if True, keep all features, if False, keep frames according to the vad labels
        :return:
        """
        self.features_extractor = None
        self.feature_filename_structure = '{}'
        self.sources = ()
        self.dataset_list = None

        # Post processing options
        self.mask = None
        self.feat_norm = None
        self.global_cmvn = None
        self.dct_pca = False
        self.dct_pca_config = (12, 12, None)
        self.sdc = False
        self.sdc_config = (1, 3, 7)
        self.delta = False
        self.double_delta = False
        self.delta_filter = numpy.array([.25, .5, .25, 0, -.25, -.5, -.25])
        self.context = (0, 0)
        self.traps_dct_nb = 0
        self.rasta = False
        self.keep_all_features = True

        if features_extractor is not None:
            self.features_extractor = features_extractor
        if feature_filename_structure is not None:
            self.feature_filename_structure = feature_filename_structure
        if sources is not None:
            self.sources = sources
        if dataset_list is not None:
            self.dataset_list = dataset_list
        if mask is not None:
            self.mask = parse_mask(mask)
        if feat_norm is not None:
            self.feat_norm = feat_norm
        if global_cmvn is not None:
            self.global_cmvn = global_cmvn
        if dct_pca is not None:
            self.dct_pca = dct_pca
        if dct_pca_config is not None:
            self.dct_pca_config = dct_pca_config
        if sdc is not None:
            self.sdc = sdc
        if sdc_config is not None:
            self.sdc_config = sdc_config
        if delta is not None:
            self.delta = delta
        if double_delta is not None:
            self.double_delta = double_delta
        if delta_filter is not None:
            self.delta_filter = delta_filter
        if context is not None:
            self.context = context
        if traps_dct_nb is not None:
            self.traps_dct_nb = traps_dct_nb
        if rasta is not None:
            self.rasta = rasta
        if keep_all_features is not None:
            self.keep_all_features = keep_all_features

        self.show = 'empty'
        self.input_feature_filename = 'empty'
        self.start_stop = (None, None)
        self.previous_load = None

    def __repr__(self):
        """

        :return: a string to display the object
        """
        ch = '\t show: {} \n\n'.format(self.show)
        ch += '\t input_feature_filename: {} \n\n'.format(self.input_feature_filename)
        ch += '\t feature_filename_structure: {} \n'.format(self.feature_filename_structure)
        ch += '\t  \n'
        ch += '\t  \n\n'
        ch += '\t Post processing options: \n'
        ch += '\t\t mask: {}  \n'.format(self.mask)
        ch += '\t\t feat_norm: {} \n'.format(self.feat_norm)
        ch += '\t\t dct_pca: {}, dct_pca_config: {} \n'.format(self.dct_pca,
                                                               self.dct_pca_config)
        ch += '\t\t sdc: {}, sdc_config: {} \n'.format(self.sdc,
                                                       self.sdc_config)
        ch += '\t\t delta: {}, double_delta: {}, delta_filter: {} \n'.format(self.delta,
                                                                             self.double_delta,
                                                                             self.delta_filter)
        ch += '\t\t rasta: {} \n'.format(self.rasta)
        ch += '\t\t keep_all_features: {} \n'.format(self.keep_all_features)

        return ch

    def post_processing(self, feat, label, global_mean=None, global_std=None):
        """
        After cepstral coefficients, filter banks or bottleneck parameters are computed or read from file
        post processing is applied.

        :param feat: the matrix of acoustic parameters to post-process
        :param label: the VAD labels for the acoustic parameters
        :param global_mean: vector or mean to use for normalization
        :param global_std: vector of standard deviation to use for normalization

        :return: the matrix of acoustic parameters ingand their VAD labels after post-process
        """
        # Apply a mask on the features
        if self.mask is not None:
            feat = self._mask(feat)

        # Perform RASTA filtering if required
        if self.rasta:
            feat, label = self._rasta(feat, label)

        # Add temporal context
        if self.delta or self.double_delta:
            feat = self._delta_and_2delta(feat)
        elif self.dct_pca:
            feat = pca_dct(feat, self.dct_pca_config[0], self.dct_pca_config[1], self.dct_pca_config[2])
        elif self.sdc:
            feat = shifted_delta_cepstral(feat, d=self.sdc_config[0], P=self.sdc_config[1], k=self.sdc_config[2])

        # Smooth the labels and fuse the channels if more than one.
        logging.debug('Smooth the labels and fuse the channels if more than one')
        label = label_fusion(label)
        
        # Normalize the data
        if self.feat_norm is None:
            logging.debug('no norm')
        else:
            self._normalize(label, feat, global_mean, global_std)

        # if not self.keep_all_features, only selected features and labels are kept
        if not self.keep_all_features:
            logging.debug('no keep all')
            feat = feat[label]
            label = label[label]

        return feat, label

    def _mask(self, cep):
        """
        Keep only the MFCC index present in the filter list
        :param cep: acoustic parameters to filter

        :return: return the list of MFCC given by filter list
        """
        if len(self.mask) == 0:
            raise Exception('filter list is empty')
        logging.debug('applied mask')
        return cep[:, self.mask]

    def _normalize(self, label, cep, global_mean=None, global_std=None):
        """
        Normalize acoustic parameters in place

        :param label: vad labels to use for normalization
        :param cep: acoustic parameters to normalize
        :param global_mean: mean vector to use if provided
        :param global_std: standard deviation vector to use if provided
        """
        # Perform feature normalization on the entire session.
        if self.feat_norm is None:
            logging.debug('no norm')
            pass
        elif self.feat_norm == 'cms':
            logging.debug('cms norm')
            cms(cep, label, global_mean)
        elif self.feat_norm == 'cmvn':
            logging.debug('cmvn norm')
            cmvn(cep, label, global_mean, global_std)
        elif self.feat_norm == 'stg':
            logging.debug('stg norm')
            stg(cep, label=label)
        elif self.feat_norm == 'cmvn_sliding':
            logging.debug('sliding cmvn norm')
            cep_sliding_norm(cep, label=label, win=301, center=True, reduce=True)
        elif self.feat_norm == 'cms_sliding':
            logging.debug('sliding cms norm')
            cep_sliding_norm(cep, label=label, win=301, center=True, reduce=False)
        else:
            logging.warning('Wrong feature normalisation type')

    def _delta_and_2delta(self, cep):
        """
        Add deltas and double deltas.
        :param cep: a matrix of cepstral cefficients

        :return: the cepstral coefficient stacked with deltas and double deltas
        """
        if self.delta:
            logging.debug('add delta')
            delta = compute_delta(cep, filt=self.delta_filter)
            cep = numpy.column_stack((cep, delta))
            if self.double_delta:
                logging.debug('add delta delta')
                double_delta = compute_delta(delta, filt=self.delta_filter)
                cep = numpy.column_stack((cep, double_delta))
        return cep

    def _rasta(self, cep, label):
        """
        Performs RASTA filtering if required.
        The two first frames are copied from the third to keep
        the length consistent
        !!! if vad is None: label[] is empty

        :param cep: the acoustic features to filter
        :param label: the VAD label
        :return:
        """
        if self.rasta:
            logging.debug('perform RASTA %s', self.rasta)
            cep = rasta_filt(cep)
            cep[:2, :] = cep[2, :]
            label[:2] = label[2]
        return cep, label

    def get_context(self, feat, start=None, stop=None, label=None):
        """
        Add a left annd right context to each frame.
        First and last frames are duplicated to provide context at the begining and at the end

        :param feat: sequence of feature frames (one fame per line)
        :param start: index of the first frame of the selected segment
        :param stop: index of the last frame of the selected segment
        :param label: vad label if available

        :return: a sequence of frames with their left and right context
        """
        if start is None:
            start = 0
        if stop is None:
            stop = feat.shape[0]
        context_feat = framing(
            numpy.pad(feat,
                      ((max(self.context[0] - start, 0), max(stop - feat.shape[0] + self.context[1] + 1, 0)),
                       (0, 0)),
                      mode='edge')[start - self.context[0] + max(self.context[0] - start, 0)
            :stop + self.context[1] + max(self.context[0] - start, 0), :],
            win_size=1+sum(self.context)
        ).reshape(-1, (1+sum(self.context)) * feat.shape[1])

        if label is not None:
            context_label = label[start:stop]
        else:
            context_label = None

        return context_feat, context_label

    def get_traps(self, feat, start=None, stop=None, label=None):
        """
        Compute TRAP parameters. The input frames are concatenated to add their left and right context,
        a Hamming window is applied and a DCT reduces the dimensionality of the resulting vector.

        :param feat: input acoustic parameters to process
        :param start: index of the first frame of the selected segment
        :param stop: index of the last frame of the selected segment
        :param label: vad label if available

        :return: a sequence of TRAP parameters
        """

        if start is None:
            start = 0
        if stop is None:
            stop = feat.shape[0]

        context_feat = framing(
            numpy.pad(
                      feat, 
                      ((self.context[0]-start, stop - feat.shape[0] + self.context[1] + 1), (0, 0)),
                      mode='edge'
                      )[start-self.context[0]
                        + max(self.context[0]-start, 0):stop + self.context[1] + max(self.context[0]-start, 0),:],
            win_size=1+sum(self.context)
        ).transpose(0, 2, 1)
        hamming_dct = (dct_basis(self.traps_dct_nb, sum(self.context) + 1)
                       * numpy.hamming(sum(self.context) + 1)).T

        if label is not None:
            context_label = label[start:stop]
        else:
            context_label = None

        return numpy.dot(
            context_feat.reshape(-1, hamming_dct.shape[0]),
            hamming_dct
        ).reshape(context_feat.shape[0], -1), context_label

    def load(self, show, channel=0, input_feature_filename=None, label=None, start=None, stop=None):
        """
        Depending of the setting of the FeaturesServer, can either:

        1. Get the datasets from a single HDF5 file
            The HDF5 file is loaded from disk or processed on the fly
            via the FeaturesExtractor of the current FeaturesServer

        2. Load datasets from multiple input HDF5 files. The datasets are post-processed separately, then concatenated
            and post-process

        :param show: ID of the show to load (should be the same for each HDF5 file to read from)
        :param channel: audio channel index in case the parameters are extracted from an audio file
        :param input_feature_filename: name of the input feature file in case it is independent from the ID of the show
        :param label: vad labels
        :param start: index of the first frame of the selected segment
        :param stop: index of the last frame of the selected segment

        :return: acoustic parameters and their vad labels
        """

        # In case the name of the input file does not include the ID of the show
        # (i.e., feature_filename_structure does not include {})
        # self.audio_filename_structure is updated to use the input_feature_filename
        if self.show == show \
                and self.input_feature_filename == input_feature_filename\
                and self.start_stop == (start, stop)  \
                and self.previous_load is not None:
            logging.debug('return previous load')
            return self.previous_load

        self.show = show
        self.input_feature_filename = input_feature_filename
        self.start_stop = (start, stop)

        feature_filename = None
        if input_feature_filename is not None:
            self.feature_filename_structure = input_feature_filename
            feature_filename = self.feature_filename_structure.format(show)

        if self.dataset_list is not None:
            self.previous_load = self.get_features(show,
                                                   channel=channel,
                                                   input_feature_filename=feature_filename,
                                                   label=label,
                                                   start=start, stop=stop)
        else:
            logging.info('Extract tandem features from multiple sources')
            self.previous_load = self.get_tandem_features(show,
                                                          channel=channel,
                                                          label=label,
                                                          start=start, stop=stop)
        return self.previous_load

    def get_features(self, show, channel=0, input_feature_filename=None, label=None, start=None, stop=None):
        """
        Get the datasets from a single HDF5 file
        The HDF5 file is loaded from disk or processed on the fly
        via the FeaturesExtractor of the current FeaturesServer

        :param show: ID of the show
        :param channel: index of the channel to read
        :param input_feature_filename: name of the input file in case it does not include the ID of the show
        :param label: vad labels
        :param start: index of the first frame of the selected segment
        :param stop: index of the last frame of the selected segment

        :return: acoustic parameters and their vad labels
        """
        """
        Si le nom du fichier d'entrée est totalement indépendant du show
        -> si feature_filename_structure ne contient pas "{}"
        on peut mettre à jour: self.audio_filename_structure pour entrer directement le nom du fichier de feature
        """
        if input_feature_filename is not None:
            self.feature_filename_structure = input_feature_filename

        # If no extractor for this source, open hdf5 file and return handler
        if self.features_extractor is None:
            h5f = h5py.File(self.feature_filename_structure.format(show), "r")

        # If an extractor is provided for this source, extract features and return an hdf5 handler
        else:
            h5f = self.features_extractor.extract(show, channel, input_audio_filename=input_feature_filename)

         #logging.debug("*** show: "+show)

        # Get the selected segment
        dataset_length = h5f[show + "/" + next(h5f[show].__iter__())].shape[0]
        # Deal with the case where start < 0 or stop > feat.shape[0]
        if start is None:
            start = 0
        pad_begining = -start if start < 0 else 0
        start = max(start, 0)

        if stop is None:
            stop = dataset_length
        pad_end = stop - dataset_length if stop > dataset_length else 0
        stop = min(stop, dataset_length)

        global_cmvn =  self.global_cmvn and not (start is None or stop is None)

        # Get the data between start and stop
        # Concatenate all required datasets
        feat = []
        global_mean = []
        global_std = []
        if "energy" in self.dataset_list:
            feat.append(h5f["/".join((show, "energy"))].value[start:stop, numpy.newaxis])
            global_mean.append(h5f["/".join((show, "energy_mean"))].value)
            global_std.append(h5f["/".join((show, "energy_std"))].value)
        if "cep" in self.dataset_list:
            feat.append(h5f["/".join((show, "cep"))][start:stop, :])
            global_mean.append(h5f["/".join((show, "cep_mean"))].value)
            global_std.append(h5f["/".join((show, "cep_std"))].value)
        if "fb" in self.dataset_list:
            feat.append(h5f["/".join((show, "fb"))][start:stop, :])
            global_mean.append(h5f["/".join((show, "fb_mean"))].value)
            global_std.append(h5f["/".join((show, "fb_std"))].value)
        if "bnf" in self.dataset_list:
            feat.append(h5f["/".join((show, "bnf"))][start:stop, :])
            global_mean.append(h5f["/".join((show, "bnf_mean"))].value)
            global_std.append(h5f["/".join((show, "bnf_std"))].value)
        feat = numpy.hstack(feat)
        global_mean = numpy.hstack(global_mean)
        global_std = numpy.hstack(global_std)

        if label is None:
            if "/".join((show, "vad")) in h5f:
                label = h5f.get("/".join((show, "vad"))).value.astype('bool').squeeze()[start:stop]
            else:
                label = numpy.ones(feat.shape[0], dtype='bool')

        # Pad the segment if needed
        feat = numpy.pad(feat, ((pad_begining, pad_end), (0, 0)), mode='edge')
        label = numpy.pad(label, ((pad_begining, pad_end)), mode='edge')
        stop += pad_begining + pad_end

        h5f.close()
        # Post-process the features and return the features and vad label
        if global_cmvn:
            feat, label = self.post_processing(feat, label, global_mean, global_std)
        else:
            feat, label = self.post_processing(feat, label)

        return feat, label

    def get_tandem_features(self, show, channel=0, label=None, start=None, stop=None):
        """
        Read acoustic parameters from multiple HDF5 files (from disk or extracted by FeaturesExtractor objects).

        :param show: Id of the show
        :param channel: index of the channel
        :param label: vad labels
        :param start: index of the first frame of the selected segment
        :param stop: index of the last frame of the selected segment

        :return: acoustic parameters and their vad labels
        """
        # Each source has its own sources (including subserver) that provides features and label
        features = []
        for features_server, get_vad in self.sources:
            # Get features from this source
            feat, lbl = features_server.get_features(show, channel=channel, label=label, start=start, stop=stop)
            if get_vad:
                label = lbl
            features.append(feat)

        features = numpy.hstack(features)

        # If the VAD is not required, return all labels at True
        if label is None:
            label = numpy.ones(feat.shape[0], dtype='bool')

        # Apply the final post-processing on the concatenated features
        return self.post_processing(features, label)

    def mean_std(self, show, channel=0, start=None, stop=None):
        """
        Compute the mean and standard deviation vectors for a segment of acoustic features

        :param show: the ID of the show
        :param channel: the index of the channel
        :param start: index of the first frame of the selected segment
        :param stop: index of the last frame of the selected segment

        :return: the number of frames, the mean of the frames and their standard deviation
        """
        feat, _ = self.load(show, channel=channel, start=start, stop=stop)
        return feat.shape[0], feat.sum(axis=0), numpy.sum(feat**2, axis=0)
