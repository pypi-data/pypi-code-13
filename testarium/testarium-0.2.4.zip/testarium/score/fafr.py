#!/usr/bin/env python
'''
Testarium
Copyright (C) 2014 Danila Doroshin, Maxim Tkachenko

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os
import numpy as np
import urlparse
import json


class FafrException(Exception): pass


def fafr(pT, pU):
    # computes false alarms, rejects and corresponding thresholds for a given
    # target and background data
    # INPUTS
    # pT :              target data (where label = +1)
    # pU :              background data  (where label = -1)
    # OUTPUTS
    # FA:               false alarms distribution along thresholds
    # FR:               false rejects distribution along thresholds
    # Thresh             thresholds

    psize = float(pT.shape[0])
    if psize == 0: psize = 1.0
    nsize = float(pU.shape[0])
    if nsize == 0: nsize = 1.0

    con = np.concatenate((pU, pT));
    #con = np.linspace(np.min(con), np.max(con), 200.0)
    s = np.sort(con)
    step = con.shape[0]/200 if len(con) > 200 else 1
    con = s[::step]
    if con[-1] != s[-1]:
        con = np.concatenate([con, [s[-1]]])

    FA = []
    FR = []
    Thresh = []
    prevFP = 0
    prevFA = 0
    first = True

    for a in con:
        FP = np.count_nonzero(pU[pU > a])
        FN = np.count_nonzero(pT[pT <= a])
        
        if first:
            prevFP = FP
            prevFN = FN
            FA.append(float(FP) / (nsize))
            FR.append(float(FN) / (psize))
            Thresh.append(a)
            first = False

        if prevFP != FP or prevFN != FN:
            FA.append(float(FP) / (nsize))
            FR.append(float(FN) / (psize))
            Thresh.append(a)

        prevFP = FP
        prevFN = FN

    return np.array(FA), np.array(FR), np.array(Thresh)


def ScorePosNeg(pos, neg):
    FA, FR, th = fafr(np.array(pos), np.array(neg))
    data = {'fa': FA, 'fr': FR, 't': th}

    # calc EER
    eer = FA[np.argmin(np.abs(FA - FR))]
    minDCF = np.min(100 * FA + FR)
    return {'score': eer, 'minDCF': minDCF, 'graph': data}
    
        
def ScoreDirectory(dir):
    # load pos and neg
    pos = dir + '/pos.txt'
    neg = dir + '/neg.txt'
    try:
        pos = np.loadtxt(pos)
        neg = np.loadtxt(neg)
    except:
        print 'Score: Error: No pos or neg file';
        return -1
    pos = pos[np.logical_not(np.isnan(pos))]
    neg = neg[np.logical_not(np.isnan(neg))]

    # calc fafr
    FA, FR, th = fafr(pos, neg)

    # save cache
    data = [{'x': FA[i], 'y': FR[i], 't': th[i]} for i, x in enumerate(FR)]

    tmp = json.encoder.FLOAT_REPR
    json.encoder.FLOAT_REPR = lambda o: format(o, '.6f')
    j = json.dumps({'xAxis': 'False Alarm', 'yAxis': 'False Reject', 'data': data})
    json.encoder.FLOAT_REPR = tmp
    try:
        open(dir + '/fafr.txt', 'w').write(j)
    except:
        print "Can't save: " + dir + '/fafr.txt'

    # calc EER
    eer = FA[np.argmin(np.abs(FA - FR))]
    minDCF = np.min(100 * FA + FR)
    return {'score': eer, 'minDCF': minDCF}


def ScoreCommit(commit):
    # collect data from commit meta and file db
    pos, neg = [], []
    for _id in commit.meta.GetAllIds():
        probs = commit.meta.GetMeta(_id)['probs']
        targets = commit.filedb.GetFile(_id)['targets']

        for name in probs:  # unpack probs by name
            if targets[name] == 1:
                pos += [probs[name]]
            elif targets[name] == 0:
                neg += [probs[name]]

    # calc fafr
    print 'FAFR: Positive and negative scores count:', len(pos), len(neg)
    pos, neg = np.array(pos), np.array(neg)
    pos = pos[np.logical_not(np.isnan(pos))]
    neg = neg[np.logical_not(np.isnan(neg))]
    FA, FR, th = fafr(pos, neg)

    # save cache
    data = [{'x': FA[i], 'y': FR[i], 't': th[i]} for i, x in enumerate(FR)]
    j = json.dumps({'xAxis': 'False Alarm', 'yAxis': 'False Reject', 'data': data})
    try:
        open(commit.dir + '/fafr.txt', 'w').write(j)
    except:
        print "Can't save: " + commit.dir + '/fafr.txt'

    # calc EER
    eer = FA[np.argmin(np.abs(FA - FR))]
    minDCF = np.min(100 * FA + FR)
    return {'score': eer, 'minDCF': minDCF}

    
def Score(o):
    if isinstance(o, str) or isinstance(o, unicode):
        return ScoreDirectory(o)
    elif isinstance(o, list) and len(o)==2:
        return ScorePosNeg(o[0], o[1])
    else:
        return ScoreCommit(o)

