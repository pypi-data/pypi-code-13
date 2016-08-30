'''
Small RNA storage class

Stores unique sequence and read count in an internal dictionary.  
Automatic normalisation to RPMR once loaded from file

Created on 1 Apr 2016

@author: steve
'''

from dna import DNA
import time

class SRNA_Seq(object):
    def __init__(self):
        self._internal_dict = {} #internal dictionary for class
        
    def __setitem__(self, sequence, count):
        self._internal_dict[sequence]=count #{sequence:count}
    
    def __getitem__(self, sequence):
        return self._internal_dict[sequence] #get count for sequence
    
    def __iter__(self):
        return self._internal_dict.iteritems() #iterable
    
    def __len__(self):
        return len(self._internal_dict) #number of sequences stored

    def __contains__(self, sequence):
        return sequence in self._internal_dict #true if sequence stored

    def sRNAs(self):
        return self._internal_dict.keys() #returns a list of all sequences

    def counts(self):
        return self._internal_dict.values() #returns a list all counts

    def load_seq_file(self, seq_file, sRNA_max_len_cutoff, min_reads, \
        sRNA_min_len_cutoff):
        """
        load a sequence file in .fasta format.
    
        Calculate RPMR and apply in the function
    
        sRNA_len_cutoff --> only reads  of length <= sRNA_len_cutoff
        accepted (including for RPMR calculation)
        min_reads --> only reads >= min_reads accepted
    
        Input format MUST be:
        >x-y
        seq
        
        Where y is the read count and seq is the processed read sequence
        (x is ignored, but is the read count rank in Fastx toolkit processed
        files)
        
        produce SRNA-Seq object --> sRNA:RPMR
        """
        start = time.clock()

        read_count = 0
        with open(seq_file, 'rU') as loaded_seq:
    
            for line in loaded_seq:
                line=line.strip()
                if line[0] == '>':
                    count = int(line.split('-')[1])
                    next_line = True 
                elif check_sRNA_allowed(count, len(line), 
                                        sRNA_min_len_cutoff, 
                                        sRNA_max_len_cutoff, 
                                        min_reads) and next_line:
                    self._internal_dict[DNA(line)] = count
                    read_count += count
                    next_line = False                
                else:
                    pass
    
        loaded_seq.close()

        # final RPMR - could simplify in future
        for sRNA, count in self._internal_dict.iteritems():
            self._internal_dict[sRNA] = count * (float(1000000) / read_count)
        print "\n{0} load time = {1} seconds for {2} reads".format(seq_file.split('/')[-1], 
                                            str((time.clock() - start)), read_count)
        print "-"*50

    def load_seq_file_arg_list(self, seq_file_arg_list, sRNA_max_len_cutoff, 
                               min_reads, sRNA_min_len_cutoff):
        """
        load seq dict from arg_list in fasta format.
    
        Calculate RPMR and apply in the function
    
        sRNA_len_cutoff --> only reads  of length <= sRNA_len_cutoff
        accepted (including for RPMR calculation)
        min_reads --> only reads >= min_reads accepted
    
        Input format MUST be:
        >x-y
        seq
    
        produce seq_dict --> sRNA:RPMR where RPMR is the average count for 
        that read if the read is present in ALL sequence files
        """
        start = time.clock()

        # read_count_1 = 0
        indv_seq_dict_list=[] #list of individual seq_dics
        indv_seq_dict_list_factor=[] #RPMR for each seq. disc

        for seq_file in seq_file_arg_list:
            single_start=time.clock()
            seq_dict={}
            read_count = 0

            with open(seq_file, 'rU') as loaded_seq:
        
                for line in loaded_seq:
                    line=line.strip()
                    if line[0] == '>':
                        count = int(line.split('-')[1])
                        next_line = True 
                    elif check_sRNA_allowed(count, len(line), 
                                            sRNA_min_len_cutoff, 
                                            sRNA_max_len_cutoff, 
                                            min_reads) and next_line:
                        seq_dict[DNA(line)] = count
                        read_count += count
                        next_line = False                
                    else:
                        pass
        
            loaded_seq.close()

            indv_seq_dict_list.append(seq_dict)
            indv_seq_dict_list_factor.append(float(1000000)/read_count)
            print "\n{0} load time = {1} seconds for {2} reads".format(seq_file.split('/')[-1], 
                                            str((time.clock() - single_start)), read_count)
        for sRNA, count in indv_seq_dict_list[0].iteritems():
            if all(sRNA in d for d in indv_seq_dict_list):
                total_count = 0
                for i in range(len(indv_seq_dict_list)):
                    total_count+=(indv_seq_dict_list[i][sRNA]*indv_seq_dict_list_factor[i])


                self._internal_dict[sRNA] = total_count/len(indv_seq_dict_list)

        print "\nTotal sequence file processing time = "\
         + str((time.clock() - start)) + " seconds\n"
        print "-"*50

def check_sRNA_allowed(count, length, sRNA_min_len_cutoff, sRNA_max_len_cutoff, 
                       min_reads):
    """
    Return True if sRNA is between min and max length, and above min count 
    """
    if count >= min_reads and sRNA_min_len_cutoff <= length <= sRNA_max_len_cutoff:
        return True
    return False