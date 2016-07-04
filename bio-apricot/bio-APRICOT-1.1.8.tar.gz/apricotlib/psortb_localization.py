#!/usr/bin/env python
# Description = Predict subcellular localization based on PsortB

import os
import subprocess
from collections import defaultdict


class PsortbSubcellularLocalization(object):
    def __init__(self, selected_proteins, psortb_path,
                 fasta_path, outpath):
        self._selected_proteins = selected_proteins
        self._psortb_path = psortb_path
        self._fasta_path = fasta_path
        self._outpath = outpath
        
        self._selected_protein_set = set()
        self._localization_dict = defaultdict(
            lambda: defaultdict(float))
        
    def streamline_psortb_localization_analysis(self):
        '''To call from apricot'''
        self.parse_selected_data()
        self.run_psortb_analysis()
        self.parse_psort_outfiles()
        self.store_compiled_data()
        self.create_job_completion_file()
        
    def parse_selected_data(self):
        '''Parses selected data for Uids'''
        with open(self._selected_proteins, 'r') as in_fh:
            for entry in in_fh:
                if not entry.startswith('Entry'):
                    self._selected_protein_set.add(entry.split('\t')[0])
        return self._selected_protein_set
    
    def run_psortb_analysis(self):
        '''Runs PsortB for identifying subcellular
        localization information of the query proteins'''
        for files in os.listdir(self._fasta_path):
            if files.split('.')[0] in self._selected_protein_set:
                print("Psortb subcellular localization analysis for %s" % files)
                subprocess.Popen(
                ["perl %s -n %s/%s > %s/%s_localization.csv" %
                 (self._psortb_path, self._fasta_path,
                  files, self._outpath, files.split('.')[0])], shell=True).wait()
                
    def parse_psort_outfiles(self):
        '''Parses PsortB output files for compiling information'''
        for files in os.listdir(self._outpath):
            protein = files.split('_')[0]
            with open(self._outpath+'/'+files, 'r') as in_fh:
                for result in in_fh.read().split('Final'):
                    if "Prediction:" in result:
                        prediction = result.split('\n')[1].replace(' ', '')
                        #print(prediction)
                        if 'Cytoplasmic' in prediction:
                            if not 'Membrane' in prediction:
                                localization = 'Cytoplasmic'
                                score = prediction.split('Cytoplasmic')[1]
                            else:
                                localization = 'Cytoplasmic-Membrane'
                                score = prediction.split('CytoplasmicMembrane')[1]
                        elif 'Periplasmic' in prediction:
                            localization = 'Periplasmic'
                            score = prediction.split('Periplasmic')[1]
                        elif 'Extracellular' in prediction:
                            localization = 'Extracellular'
                            score = prediction.split('Extracellular')[1]
                        elif 'OuterMembrane' in prediction:
                            localization = 'OuterMembrane'
                            score = prediction.split('OuterMembrane')[1]
                        elif 'Unknown' in prediction:
                            localization = 'Unknown'
                            score = '-'
                        else:
                            print("this entry's localization is not listed: %s" % prediction)
                        self._localization_dict[localization][protein] = score
                        
        return self._localization_dict
    
    def store_compiled_data(self):
        '''Creates output file with PsortB derived information'''
        outfile = self._outpath+'/psortb_data_summary.csv'
        with open(outfile, 'w') as out_fh:
            out_fh.write("localization prediction by PSORTB:\nProteins\tLocalization\tScore\n")
            for entry in self._localization_dict.items():
                localization = entry[0]
                out_fh.write("Localization: %s\tscore\n" % localization)
                print(localization, len(self._localization_dict[localization]))
                for protein in entry[1].keys():
                    score = self._localization_dict[localization][protein]
                    out_fh.write('%s\t%s\t%s\n' % (protein, localization, score))
        print("Data save is %s.\nPlease check %s for the summary." % (
            self._outpath, outfile))
    
    def create_job_completion_file(self):
        with open(self._outpath+'/psortb_analysis.txt', 'w') as out_fh:
            out_fh.write("Localization for the selected proteins are predicted by PsortB.\n")
            out_fh.write("The files generated by the analysis:.\n")
            out_fh.write('\n'.join(os.listdir(self._outpath)))

