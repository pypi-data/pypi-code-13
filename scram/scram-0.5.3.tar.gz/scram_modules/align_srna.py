'''
Created on 4 Apr 2016

@author: steve
'''
import operator
from dna import DNA

class Align_sRNA(object):
    
    def __init__(self):
        self._internal_dict = {}
    
    def __setitem__(self, sRNA, alignment):
        self._internal_dict[sRNA]=alignment
    
    def __getitem__(self, sRNA):
        return self._internal_dict[sRNA]
    
    def __iter__(self):
        return self._internal_dict.iteritems()
    
    def __len__(self):
        return len(self._internal_dict)

    def sRNAs(self):
        return self._internal_dict.keys()

    def alignments(self):
        return self._internal_dict.values()     
        
    def align_reads_to_seq(self, seq_dict, ref, sRNA_length):
        """
        
        Aligns reads from a srna_seq object to a ref_seq object
        
        Returns {query seq: [position, count]} 
        """ 
        count_start = 0

        ref_complement = ref.complement()
    
        while count_start < (len(ref) - (sRNA_length - 1)):
            query_seq_fwd = DNA(ref[count_start:(count_start + sRNA_length)])
            query_seq_rvs = DNA(ref_complement[count_start:(count_start + sRNA_length)])
            if query_seq_fwd in seq_dict and query_seq_fwd not in self._internal_dict:
                self._internal_dict[query_seq_fwd] = [
                    [count_start, seq_dict[query_seq_fwd]]]
            elif query_seq_fwd in seq_dict and query_seq_fwd in self._internal_dict:
                self._internal_dict[query_seq_fwd].append(
                    [count_start, seq_dict[query_seq_fwd]])
            if query_seq_rvs in seq_dict and query_seq_rvs not in self._internal_dict:
                self._internal_dict[query_seq_rvs] = [
                    [len(ref)-count_start-1, 0 - seq_dict[query_seq_rvs]]]
            elif query_seq_rvs in seq_dict and query_seq_rvs in self._internal_dict:
                self._internal_dict[query_seq_rvs].append(
                    [len(ref)-count_start-1, 0 - seq_dict[query_seq_rvs]])
            count_start += 1       

    def split(self):
        """
        Splits the alignment count for a read by the number of times it has aligned.
        
        Returns an alignment object
        """
        for alignments in self._internal_dict.values():
            for alignment in alignments:
                alignment[1]/=len(alignments)
        
    
    
    def aln_by_ref_pos(self):
        """
        Create 2 lists - fwd alignment and rvs alignment
        Each contains tuple(pos,count)
        Returned as ordered.
        """
    
        fwd_alignment={}
        rvs_alignment={}
        aln_count = 0
        for alignment in self._internal_dict.itervalues():
            for i in alignment:
                if i[1] > 0:
                    fwd_alignment[i[0]]=i[1] # pos,count
                    aln_count += i[1]
                elif i[1] < 0: 
                    rvs_alignment[i[0]]=i[1] #pos:count
                    
                    aln_count -= i[1]
    
    
        sorted_fwd_alignment = sorted(fwd_alignment.items(), 
                                      key=operator.itemgetter(0))
    
    
        sorted_rvs_alignment = sorted(rvs_alignment.items(), 
                                      key=operator.itemgetter(0))
    #    detect_phase(sorted_fwd_alignment, sorted_rvs_alignment)
        print "\n{0} reads per million reads have aligned\n".format(aln_count)
        print "-"*50
        return [sorted_fwd_alignment, sorted_rvs_alignment, aln_count]

    