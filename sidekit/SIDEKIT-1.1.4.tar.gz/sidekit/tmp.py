# coding: utf-8
# # Run an i-vector system on NIST SRE10

# author: Anthony Larcher
# 07/07/2016

import copy
from fnmatch import fnmatch
import multiprocessing
import numpy as np
import os
import re
import sidekit
import yaml


# ### Before starting, list all available files
# In the following code, you should write down the directories where to find each database.
#
# The script lists all available audio files according to their extension.
# It creates a dictionary where keys are a session ID and values are the audio file name.


# Set the extension of files to look for (originally .sph for NIST corpora)
audio_extension = 'sph'
existing_file_dictionary = 'existing_nist_files_corpus.yaml'

# Here enter the directories for all databases
corpora_dir = {'sre05': '/lium/corpus/audio/tel/en/SRE05',
               'sre04': '/lium/corpus/audio/tel/en/SRE04',
               'sre06': '/lium/corpus/audio/tel/en/SRE06',
               'sre08': ['/lium/corpus/audio/tel/en/SRE08',
                        '/lium/corpus/audio/tel/en/SRE08_Followup'],
               'sre10': '/lium/corpus/audio/tel/en/SRE10',
               'swb': ['/lium/corpus/audio/tel/en/swb1/',
                       '/lium/corpus/audio/tel/en/SB2P2',
                       '/lium/corpus/audio/tel/en/SB2P3',
                       '/lium/corpus/audio/tel/en/swb_cellP1',
                       '/lium/corpus/audio/tel/en/swb_cellP2']
               }


def search_files(corpora_dir, audio_extension):
    """"""
    corpusList = []
    completeFileList = []
    fileList = []
    file_dict = {}
    for corpus in corpora_dir.keys():
        if not isinstance(corpora_dir[corpus], list):
            dirNameList = [corpora_dir[corpus]]
        else:
            dirNameList = corpora_dir[corpus]
        for dirName in dirNameList:
            print("Scanning {}\n".format(dirName))
            for path, subdirs, files in os.walk(dirName):
                for name in files:
                    if (fnmatch(name, audio_extension.upper())
                            or fnmatch(name, audio_extension.lower())
                            or fnmatch(name, audio_extension)):
                        name = os.path.splitext(name)[0]
                        file_dict[corpus + '/' + os.path.splitext(name)[0].lower()] = os.path.join(path, name)
                        corpusList.append(corpus)
                        completeFileList.append(os.path.join(path, name))
                        fileList.append((corpus + '/' + os.path.splitext(name)[0]).lower())
    return corpusList, completeFileList, fileList, file_dict

# Look for all files
corpusList, completeFileList, sphList, file_dict = search_files(corpora_dir, "*." + audio_extension)

# Create the dictionary
dictionary = dict(zip(sphList, completeFileList))

# Write the dictionary in YAML text format
with open(existing_file_dictionary, 'w') as f:
    yaml.dump(dictionary, f, default_flow_style=False)


# ## Part 1: Extract features to train a FeedForward DNN
#
# Now set your own parameters to extract features.
#
# We extract here acoustic parameters for all shows (sessions) at once


feature_dir = '/lium/spk1/larcher/mfcc_24/' # directory where to store the acoustic parameters
feature_extension = 'h5'  # extension of the feature files to create

# Automatically set the number of parallel process to run.
# The number of threads to run is set equal to the number of cores available
# on the machine minus one or to 1 if the machine has a single core.
nbThread = max(multiprocessing.cpu_count()-1, 1)


# Load the list of sessions to process:
with open("all_sessions.lst", 'r') as f:
    show_list = np.array([fn.rstrip() for fn in f if not os.path.exists(feature_dir + fn.rstrip() + "." + feature_extension)])
print("Number of unique shows: {}".format(len(show_list)))


# Use the dictionary of existing files in order to generate the list of files and channels to process.
# All first channels are going to be extracted in a HDF5 file with extension `_a.h5` while the second channel will use the extension `_b.h5`.
existing_file_dictionary = "existing_nist_files_corpus.yaml"
with open(existing_file_dictionary, 'r') as f:
    efd = yaml.load(f)

# Generate the list of channel extension and nist keys of the sessions to processs
print("Get list of sessions per file")
channel = np.empty(show_list.shape, dtype='int8')
audio_file = np.empty(show_list.shape, dtype='|O')
for idx, sess in enumerate(show_list):
    if re.sub('_a$|_b$', '', sess) in efd.keys():
        if sess.endswith('_a'):
            channel[idx] = 0
        elif sess.endswith('_b'):
            channel[idx] = 1
        else:
            channel[idx] = 0
        audio_file[idx] = efd[re.sub('_a$|_b$', '', sess)] + '.' + audio_extension
channel_list = np.array(channel)
audio_file_list = np.array(audio_file)


# Now that the lists have been created, initialize the FeaturesExtractor and extract the acoustic parameters.
#
# The output feature files will have a name that includes the ID if the show (i.e. ID of the session).
#
# Thus, `feature_filename_structure=feature_dir + '{}.' + feature_extension`.
#
# While the input audio file has a name that migh be independent of the ID of the show. For this reason, we set the `audio_filename_structure` to `''` in order to use the filename from the list `audio_file_list`.
#
# Other parameters of the `FeaturesExtractor` set the frequency band to [200;3800], we use MEL-scale filter banks with 24 filters. 20 Cepstral coefficients are extracted and the Voice Activity Detector uses an algorithm based on the SNR.
#
# The resulting files will include:
# - vad labels
# - log-energy value for each feature
# - cepstral coefficients
# - filter bank coefficients

extractor = sidekit.FeaturesExtractor(audio_filename_structure="",
                                      feature_filename_structure=feature_dir + '{}.' + feature_extension,
                                      sampling_frequency=None,
                                      lower_frequency=200,
                                      higher_frequency=3800,
                                      filter_bank="log",
                                      filter_bank_size=24,
                                      window_size=0.025,
                                      shift=0.01,
                                      ceps_number=20,
                                      vad="snr",
                                      snr=40,
                                      pre_emphasis=0.97,
                                      save_param=["vad", "energy", "cep", "fb"],
                                      keep_all_features=True)

print("Start extracting features")
extractor.save_list(show_list=show_list,
                    channel_list=channel_list,
                    audio_file_list=audio_file_list,
                    num_thread=nbThread)


# ## Part 2: Train a FeedForward DNN for bottleneck features extraction
#
# The following sections of code are used to train a FeedForward neural network using stacked vectors of filter banks coefficients.
#
# Training data include only Switchboard for this example.
#
# The frame alignments used for supervised training are generated by using the standard KALDI recipe with 2304 senones.
bnf_dir = '/lium/spk1/larcher/bnf/'

#Load the labels and get the number of output classes
label_file_name = "swb1_2304.ali"
print("Load training feature labels")
with open(label_file_name, 'r') as inputf:
    lines = [line.rstrip() for line in inputf]
    print(lines[1].split('_')[0] + '_' + lines[1].split('_')[1])
    seg_list = [(line.split('_')[0] + '_' + line.split('_')[1],
        int(line.split('_')[2].split('-')[0]),
        int(line.split(' ')[0].split('_')[2].split('-')[1]),
        np.array([int(x) for x in line.split()[1:]]))
        for line in lines[1:-1]]
    max_list = [seg[3].max() for seg in seg_list]
    nclasses = max(max_list) + 1

print("Number of output classes = {}".format(nclasses))


print("Split the list of segments for training and cross-validation")
idx = np.random.permutation(len(seg_list)).astype('int')
training_seg_list = [seg_list[ii] for ii in idx[:len(seg_list)*0.9]]
cv_seg_list = [seg_list[ii] for ii in idx[len(seg_list)*0.9:]]


# Create the feed-forward neural network by defining the layer structure and the activation functions.

# Create FeaturesServer to load features
features_server = sidekit.FeaturesServer(feature_filename_structure=feature_dir + "{}." + feature_extension,
                                          dataset_list = ["fb"],
                                          mask="[0-23]",
                                          context=(7,7),
                                          feat_norm="cmvn",
                                          global_cmvn=True)


feature_size = 24
input_size = feature_size * (sum(features_server.context) +1)

# Define the structure of the NN
FfNn = sidekit.nnet.FForwardNetwork(input_size=input_size,
            hidden_layer_sizes=(1000, 1000, 80, 1000, 1000),
            layers_activations=("sigmoid", "sigmoid", None, "sigmoid", "sigmoid", "softmax"),
            n_classes=nclasses)


# We now define the FeaturesServer that will load filter-banks parameters to feed THEANO.
# Note that we use only filter-bank parameters (`fb`) and that features from each segment are normalized using the global mean and standard deviation computed on the entire feature file (`feat_norm="cmvn"` and `                global_cmvn=True`).

# Start training of the network
print("Start training")
FfNn.train(training_seg_list=training_seg_list,
           cross_validation_seg_list=cv_seg_list,
           features_server=features_server,
           feature_size=360,
           lr=0.008,
           segment_buffer_size=200,
           batch_size=512,
           max_iters=20,
           tolerance=0.003,
           output_file_name="BNF_1000_1000_80_1000_1000",
           save_tmp_nnet=True,
           traps=False,
           num_thread=10)


# ## Part 3: Extract BottleNeck features using the two first layers of the DNN
#
# BNF are extracted using either the GPU or parallel processing on CPUS.
# GPU are faster but a large number of CPU (>25) will become faster that a single GPU.

# Get the list of features to process
with open("all_sessions.lst", "r") as fh:
    bnf_file_list = np.array([line.rstrip() for line in fh if not os.path.exists(bnf_dir + '{}'.format(line.rstrip()) + feature_extension)])

# Load NN parameters
FfNn = sidekit.FForwardNetwork.read("BNF_1000_1000_80_1000_1000_epoch_9")

# Extract Bottleneck features using the first 2 bottom layers of the network
# Run Bottleneck features computation in parallel on CPU
if "cpu" in os.environ["THEANO_FLAGS"]:
    import multiprocessing

    print("Split the list of files to process")
    sub_lists = [list(l) for l in np.array_split(bnf_file_list, nbThread)]

    print("Extract Bottleneck features in parallel")
    jobs = []
    multiprocessing.freeze_support()
    for idx in range(nbThread):
        # Create argument list for each process
        ff_args = {'layer_number':2,
                 'feature_file_list':sub_lists[idx],
                 'output_file_structure':bnf_dir + "{}.h5",
                 features_server:features_server}
        p = multiprocessing.Process(target=FfNn.feed_forward, kwargs=ff_args)
        jobs.append(p)
        p.start()
    for p in jobs:
        p.join()

# Run Bottleneck features computation on a singleGPU
elif "gpu" in os.environ["THEANO_FLAGS"]:
    FfNn.feed_forward(feature_file_list=bnf_file_list,
                      features_server=features_server,
                      layer_number=2,
                      output_file_structure=bnf_dir + "{}.h5")


# ## Part 4: Train an i-vector system using tandem features (MFCC + BNF)
# First we load all lists to:
# - train the UBM
# - estimate the Total Variability matrix
# - extract i-vectors on all sessions required to run NIST-SRE10 evaluation

# Load lists
gender = ["male", "female"] # Train a gender independent UBM, TV matrix
eval_gender = "male"  # Run tests on the male part only

# Chose databases to train with
database = ["04_tel", "05_tel", "06_tel", "08_tel", "swb_tel", "05_mic", "06_mic", "08_mic"]

# Chose the IdMap to train a male only PLDA model
plda_im = "male_plda_tel_mic.h5"

# set the experiment ID (that will be use as unique identifier to be included in all file names)
expe_id = "tel_mic_04050608swb_12E_BNF"

system_size = 512  # number of Gaussian distributions for each GMM
rank_TV = 400  # rank of the TV matrix

scoring = ['cosine', 'plda']  # type of scoring functions to use

# Create two lists of shows to use to train two gender dependent UBMs
print('Train ubm with:')
ubm_list = [[], []]
for gdr_idx, gdr in enumerate(gender):
    for db in database:
        print("    {} - {}".format(gdr, db))
        with open("nist/lists/ubm_{gdr}_{db}.lst".format(gdr=gdr[0], db=db )) as fh:
            ubm_list[gdr_idx] += [l.rstrip() for l in fh]
    ubm_list[gdr_idx] = np.array(ubm_list[gdr_idx])
print("    {} sessions".format(len(ubm_list)))

# Create an IdMap to train the total variability matrix from the lists of shows
print("Load TV list")
tv_list = []
print("Train Total Variability with:")
for gdr in gender:
    for db in database:
        print("    {} - {}".format(gdr, db))
        with open("nist/lists/tv_{gdr}_{db}.lst".format(gdr=gdr[0], db=db )) as fh:
            tv_list += [l.rstrip() for l in fh]

print("    {} sessions".format(len(tv_list)))
tv_idmap = sidekit.IdMap()
tv_idmap.leftids = np.array(tv_list)
tv_idmap.rightids = np.array(tv_list)
tv_idmap.start =  np.empty(tv_idmap.leftids.shape, dtype='|O')
tv_idmap.stop =  np.empty(tv_idmap.leftids.shape, dtype='|O')
assert tv_idmap.validate(), 'Error for tv_idmap'

# Load the IdMap to train a male only PLDA
print("Load PLDA IdMap {}".format(plda_im))
plda_idmap = sidekit.IdMap("/lium/buster1/larcher/nist/lists/{}".format(plda_im))


# Create an IdMap to extract i-vector for enrollment and test based on the Ndx object
print("Load test lists")
enroll_idmap = sidekit.IdMap("nist/sre10/coreext_{}_sre10_trn.h5".format(eval_gender))

test_ndx = sidekit.Ndx("nist/sre10/coreext_coreext_{}_sre10_ndx.h5".format(eval_gender))
test_idmap = sidekit.IdMap()
test_idmap.rightids = test_ndx.segset
test_idmap.leftids = test_ndx.segset
test_idmap.start = np.empty(test_idmap.leftids.shape, dtype='|O')
test_idmap.stop = np.empty(test_idmap.leftids.shape, dtype='|O')

# Load trial keys
print("Load keys")
keys = []
for cond in range(9):
    keys.append(sidekit.Key('nist/sre10/coreext_coreext_all_sre10_cond{}_key.h5'.format(cond + 1)))


# Create the FeaturesServer to read acoustic parameters.
#
# We create first two FeaturesServers:
# - one to load cepstral coefficients and process them (add first and second order derivatives, perform RASTA filtering...)
# - one to load bottleneck features
#
# The global FeaturesServer will concatenate cepstral coefficients and bottleneck features and post-process them

mfcc_fs = sidekit.FeaturesServer(feature_filename_structure="{dir}/{{}}.{ext}".format(dir=feature_dir, ext=feature_extension),
                                 dataset_list=["energy", "cep", "vad"],
                                 mask="[0-12]",
                                 delta=True,
                                 double_delta=True,
                                 delta_filter=np.array([.25, .5, .25, 0, -.25, -.5, -.25]),
                                 rasta=True,
                                 context=None)

bnf_fs = sidekit.FeaturesServer(feature_filename_structure="{dir}/{{}}.{ext}".format(dir=bnf_dir, ext=feature_extension),
                                dataset_list=["bnf"],
                                mask=None,
                                context=None)

tandem_fs = sidekit.FeaturesServer(sources=((mfcc_fs, True), (bnf_fs, False)),
                                   feat_norm="cmvn",
                                   keep_all_features=False,
                                   context=None)


# #### Train the UBM
# Now train two gender dependent UBM that will be merged to create a gender independent UBM.

print('Train the UBM by EM')
ubm_gdr = []
for gdr_idx, gdr in enumerate(gender):
    ubm_gdr.append(sidekit.Mixture())
    llk = ubm_gdr[-1].EM_split(tandem_fs,
                               ubm_list[gdr_idx][:500],
                               system_size//2,
                               num_thread=nbThread,
                               save_partial='gmm/ubm_{}_{}_{}'.format(gdr, system_size, expe_id))
    ubm_gdr[gdr_idx].write('gmm/ubm_{}_{}_{}.h5'.format(gdr, system_size, expe_id))

print('Load male UBM')
ubm_m = sidekit.Mixture('gmm/ubm_{}_{}_{}.h5'.format(gender[0], system_size//2, expe_id))
print('Load female UBM')
ubm_f = sidekit.Mixture('gmm/ubm_{}_{}_{}.h5'.format(gender[1], system_size//2, expe_id))
print('Merge both UBMs')
ubm = sidekit.Mixture()
ubm.merge([ubm_m, ubm_f])


# #### Compute the sufficient statistics

print('Compute the sufficient statistics')
# Create a StatServer for the enrollment data and compute the statistics
enroll_stat = sidekit.StatServer(enroll_idmap, ubm)
enroll_stat.accumulate_stat(ubm=ubm,
                            feature_server=tandem_fs,
                            seg_indices=range(enroll_stat.segset.shape[0]),
                            num_thread=nbThread)
enroll_stat.write('data/stat_sre10_coreX-coreX_{}_enroll_{}_{}.h5'.format(eval_gender[0], system_size, expe_id))

tv_stat = sidekit.StatServer(tv_idmap, ubm)
tv_stat.accumulate_stat(ubm=ubm,
                        feature_server=tandem_fs,
                        seg_indices=range(tv_stat.segset.shape[0]), num_thread=nbThread)
tv_stat.write('data/stat_{}_tv_{}_{}.h5'.format("_".join(gender), system_size, expe_id))

plda_stat = sidekit.StatServer(plda_idmap, ubm)
plda_stat.accumulate_stat(ubm=ubm,
                          feature_server=tandem_fs,
                          seg_indices=range(plda_stat.segset.shape[0]),
                          num_thread=nbThread)
plda_stat.write('data/stat_{}_plda_{}_{}.h5'.format("_".join(gender), system_size, expe_id))

test_stat = sidekit.StatServer(test_idmap, ubm)
test_stat.accumulate_stat(ubm=ubm,
                          feature_server=tandem_fs,
                          seg_indices=range(test_stat.segset.shape[0]),
                          num_thread=nbThread)
test_stat.write('data/stat_sre10_coreX-coreX_{}_test_{}_{}.h5'.format(eval_gender[0], system_size, expe_id))

# Remove lines with zeros in the StatServers
sidekit.sv_utils.clean_stat_server(enroll_stat)
sidekit.sv_utils.clean_stat_server(tv_stat)
sidekit.sv_utils.clean_stat_server(plda_stat)
sidekit.sv_utils.clean_stat_server(test_stat)


# #### Train the Total Variability Matrix
print('Estimate Total Variability Matrix')
tv_mean, tv, _, __, tv_sigma = tv_stat.factor_analysis(rank_f = rank_TV,
                                                       rank_g = 0,
                                                       rank_h = None,
                                                       re_estimate_residual = False,
                                                       it_nb = (10,0,0),
                                                       min_div = True,
                                                       ubm = ubm,
                                                       batch_size = 1000,
                                                       num_thread = nbThread,
                                                       save_partial = "data/TV_{}_{}_{}".format("_".join(gender),
                                                                                                system_size,
                                                                                                expe_id))


# #### Extract i-vectors
print('Extraction of i-vectors')
enroll_iv = enroll_stat.estimate_hidden(tv_mean, tv_sigma, V=tv, U=None, D=None, num_thread=nbThread)[0]
enroll_iv.write('data/iv_sre10_coreX-coreX_{}_enroll_{}_{}.h5'.format(eval_gender[0], system_size, expe_id))

test_iv = test_stat.estimate_hidden(tv_mean, tv_sigma, V=tv, U=None, D=None, num_thread=nbThread)[0]
test_iv.write('data/iv_sre10_coreX-coreX_{}_test_{}_{}.h5'.format(eval_gender[0], system_size, expe_id))

plda_iv = plda_stat.estimate_hidden(tv_mean, tv_sigma, V=tv, U=None, D=None, num_thread=nbThread)[0]
plda_iv.write('data/iv_{}_plda_{}_{}.h5'.format("_".join(gender), system_size, expe_id))


# #### Run NIST-SRE10 male experiment
# Run the test using Cosine distance (no LDA, no WCCN in this example) and PLDA (after Spherical Nuisance Normalization)

print('Run Cosine scoring evaluation without WCCN')
scores_cos = sidekit.iv_scoring.cosine_scoring(enroll_iv, test_iv, test_ndx, wccn = None)

print('Run PLDA scoring evaluation')
# Estimate the normalization parameters for 1 iteration of Spherical Nuisance Normalization
meanSN, CovSN = plda_iv.estimate_spectral_norm_stat1(1, 'sphNorm')

# Normalize the i-vectors
plda_iv.spectral_norm_stat1(meanSN[:1], CovSN[:1])
enroll_iv.spectral_norm_stat1(meanSN[:1], CovSN[:1])
test_iv.spectral_norm_stat1(meanSN[:1], CovSN[:1])

# Estimate PLDA model
plda_rank = 400
plda_iv_sn1 = copy.deepcopy(plda_iv)
mean, F, G, H, Sigma = plda_iv_sn1.factor_analysis(rank_f=plda_rank, rank_g=0, rank_h=None,
            re_estimate_residual=True,
            it_nb=(10,0,0), min_div=True, ubm=None,
            batch_size=1000, num_thread=nbThread)

# Compute PLDA scores
scores_plda = sidekit.iv_scoring.PLDA_scoring(enroll_iv, test_iv, test_ndx, mean, F, G, Sigma)


# #### plot DET curve and display EER and minDCF
# Plot only DET curves for Condition 5
print("Evaluate and display EER and minDCF")
prior = sidekit.effective_prior(0.001, 1, 1)  # SRE10 prior
dp = sidekit.DetPlot(window_style='sre10', plot_title='I-Vectors SRE 2010 {}'.format(eval_gender))


print('Plot DET curves')
prior = sidekit.effective_prior(0.001, 1, 1)
dp = sidekit.DetPlot(window_style='sre10', plot_title='SRE 2010 {}, Condition 5'.format(eval_gender))

dp.set_system_from_scores(scores_cos, keys[4], sys_name='Cond 5')
dp.set_system_from_scores(scores_plda, keys[4], sys_name='Cond 5')

# Display EER and minDCF
minDCF_cos, Pmiss_cos, Pfa_cos, prbep_cos, eer_cos = sidekit.bosaris.detplot.fast_minDCF(dp.__tar__[0],
                                                                                         dp.__non__[0],
                                                                                         prior,
                                                                                         normalize=False)
minDCF_plda, Pmiss_plda, Pfa_plda, prbep_plda, eer_plda = sidekit.bosaris.detplot.fast_minDCF(dp.__tar__[1],
                                                                                         dp.__non__[1],
                                                                                         prior,
                                                                                         normalize=False)

print("Cosine similarity: Condition 5; minDCF = {}, eer = {}".format(minDCF_cos, eer_cos))
print("PLDA: Condition 5; minDCF = {}, eer = {}".format(minDCF_plda, eer_plda))

# Plot the curves
dp.create_figure()
dp.plot_rocch_det(0)
dp.plot_rocch_det(1)
dp.plot_DR30_both(idx=1)
dp.plot_mindcf_point(prior, idx=1)

