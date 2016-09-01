'''
Created on 31 Mar 2016

@author: steve
'''
from ref_seq import Ref_Seq
import time
from termcolor import colored
from align_srna import Align_sRNA
import analysis_helper as ah
import numpy
import write_to_file as wtf
import post_process as pp
import plot_reads as pr
from multiprocessing import Process, JoinableQueue, Manager

def ref_coverage(seq, seq_output, ref_file, nt, smoothWinSize, fileFig, 
                 fileName, min_read_size, max_read_size, min_read_no, 
                 onscreen, no_csv, ylim, pub, split):
    """
    Align reads of one length to a single reference sequence
    """
    
    ref = Ref_Seq()
    ref.load_ref_file(ref_file)
    
    if len(ref)>1:
        print "\nMultiple reference sequences in file.\n"
        return 
    ref_output = ah.single_file_output(ref_file)
    #this is a hack    
    for header in ref.headers():
        single_ref=ref[header]
    start = time.clock()
    print colored("------------------ALIGNING READS------------------\n",'green') 
    single_alignment = Align_sRNA()
    single_alignment.align_reads_to_seq(seq, single_ref, nt)
    if split is False:
        single_alignment.split()
    single_sorted_alignemts = single_alignment.aln_by_ref_pos()
    if no_csv:
        wtf.csv_output(single_alignment,
                                 nt,
                                 seq_output,
                                 ref_output)   
    if fileFig or onscreen:
        
        graph_processed = pp.fill_in_zeros(single_sorted_alignemts, 
            len(single_ref), nt)
        x_ref = graph_processed[0]
        y_fwd_smoothed = pp.smooth(numpy.array(graph_processed[1]), 
            smoothWinSize, window='blackman')
        y_rvs_smoothed = pp.smooth(numpy.array(graph_processed[2]), 
            smoothWinSize, window='blackman')
        
        if fileName == "auto":
            fileName = ah.ref_seq_nt_output(seq_output, ref_output, nt, "pdf")
                
        pr.den_plot(x_ref, y_fwd_smoothed, y_rvs_smoothed, nt, fileFig, 
            fileName, onscreen, ref_output, ylim, pub)

def coverage_21_22_24(seq, seq_output, ref_file, smoothWinSize, 
    fileFig, fileName, min_read_size, max_read_size, min_read_no,
    onscreen, no_csv,y_lim, pub, split):     
    """
    Align reads of 21,22 and 24 nt to a single reference seq.
    """
    ref = Ref_Seq()
    ref.load_ref_file(ref_file)
    if len(ref)>1:
        print "\nMultiple reference sequences in file.\n"
        return 
    ref_output = ah.single_file_output(ref_file)
    #this is a hack
    print colored("------------------ALIGNING READS------------------\n",'green')     
    for header in ref.headers():
        single_ref=ref[header]    
    combined_21_22_24(seq, seq_output, ref_output, single_ref, smoothWinSize, 
    fileFig, fileName, min_read_size, max_read_size, min_read_no,
    onscreen, no_csv,y_lim, pub, split)    
       
    
def combined_21_22_24(seq, seq_output, ref_output, single_ref, smoothWinSize, 
    fileFig, fileName, min_read_size, max_read_size, min_read_no,
    onscreen, no_csv,y_lim, pub, split):
    """
    Helper function - Align reads of 21,22 and 24 nt to a single reference 
    sequence
    """
    sRNA_lens = [21,22,24]
    work_queue = JoinableQueue()
    processes = []
    mgr=Manager()
    alignments_dict=mgr.dict()

    non_srt_alignments_dict=mgr.dict() #for csv only
    for x in sRNA_lens:
        work_queue.put(x)
    for w in xrange(3):
        p = Process(target=worker, args=(work_queue, seq, single_ref, split, 
                                         alignments_dict, 
                                         non_srt_alignments_dict, 
                                         no_csv))
        p.start()
        processes.append(p)
    
    for p in processes:
        p.join()    
    

    single_sorted_alignemts_21=alignments_dict[21]

    single_sorted_alignemts_22=alignments_dict[22]

    single_sorted_alignemts_24=alignments_dict[24]

    

    if fileFig or onscreen:
    
        graph_processed_21 = pp.fill_in_zeros(alignments_dict[21], 
            len(single_ref),21)
        graph_processed_22 = pp.fill_in_zeros(alignments_dict[22], 
            len(single_ref),22)
        graph_processed_24 = pp.fill_in_zeros(alignments_dict[24], 
            len(single_ref),24)
    
        x_ref = graph_processed_21[0]
        y_fwd_smoothed_21 = pp.smooth(numpy.array(graph_processed_21[1]), 
            smoothWinSize, window='blackman')
        y_rvs_smoothed_21 = pp.smooth(numpy.array(graph_processed_21[2]), 
            smoothWinSize, window='blackman')
        y_fwd_smoothed_22 = pp.smooth(numpy.array(graph_processed_22[1]), 
            smoothWinSize, window='blackman')
        y_rvs_smoothed_22 = pp.smooth(numpy.array(graph_processed_22[2]), 
            smoothWinSize, window='blackman')
        y_fwd_smoothed_24 = pp.smooth(numpy.array(graph_processed_24[1]), 
            smoothWinSize, window='blackman')
        y_rvs_smoothed_24 = pp.smooth(numpy.array(graph_processed_24[2]), 
            smoothWinSize, window='blackman')
    
        if fileName == "auto":
            fileName = ah.ref_seq_output(seq_output, ref_output, "pdf")
    
        pr.den_multi_plot_3(x_ref, y_fwd_smoothed_21, y_rvs_smoothed_21,
        y_fwd_smoothed_22, y_rvs_smoothed_22, y_fwd_smoothed_24, 
        y_rvs_smoothed_24, fileFig, fileName, onscreen, ref_output, y_lim, pub)
    if no_csv:
        wtf.mnt_csv_output(non_srt_alignments_dict[21], 
                           non_srt_alignments_dict[22], 
                           non_srt_alignments_dict[24],
                           seq_output, 
                           ref_output)

def worker(work_queue, seq, single_ref, split, alignments_dict, 
           non_srt_alignments_dict, 
           no_csv):


    try:
        while not work_queue.empty():
            single_alignment = Align_sRNA()
            sRNA_len = work_queue.get()
            single_alignment.align_reads_to_seq(seq, single_ref, sRNA_len)

            if split is False:
                single_alignment.split()
            if no_csv:
                non_srt_alignments_dict[sRNA_len]=single_alignment
            single_sorted_alignemts = single_alignment.aln_by_ref_pos()
            alignments_dict[sRNA_len] = single_sorted_alignemts
    except Exception, e:
        print e
    return True 


     
        
    