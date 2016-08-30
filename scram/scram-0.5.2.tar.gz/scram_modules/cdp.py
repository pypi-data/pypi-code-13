'''CDP analysis class - for calculation of reads aligning to a reference
sequence as (x,y) coordinates for two sets of sequence files

Created on 25 Feb 2016

@author: steve
'''
from termcolor import colored
from ref_seq import Ref_Seq
import write_to_file as wtf
import analysis_helper as ah
import plot_reads as pr
from dna import DNA
from multiprocessing import Process, JoinableQueue, Manager
#TODO: sort a no csv option
def CDP_shared(seq_1, seq_2, seq_name_1, seq_name_2, ref_file, nt,fileFig, 
               fileName, min_read_size, max_read_size, min_read_no, onscreen,
               no_csv, pub, cores):

    """
    Refactored CDP code shared between CDP and avCDP
    """
    workers = cores
    work_queue = JoinableQueue()
    # done_queue = Queue()
    processes = []
    mgr=Manager()
    count = 0
    counts_by_ref=mgr.dict() #header:(count1, count2)
    refs=Ref_Seq()
    refs.load_ref_file(ref_file)
    print colored("------------------ALIGNING READS------------------\n",'green')
    for header,seq in refs:
        work_queue.put((header,seq,)) 
        count+=1
        if count%10000==0:
            for w in xrange(workers):
                p = Process(target=CDP_worker, args=(work_queue, counts_by_ref, 
                                                     seq_1, 
                                                     seq_2,
                                                     nt))
                p.start()
                processes.append(p)       

            for p in processes:
                p.join()
    for w in xrange(workers):
        p = Process(target=CDP_worker, args=(work_queue, counts_by_ref, 
                                             seq_1, 
                                             seq_2, 
                                             nt))
        p.start()
        processes.append(p)       

    for p in processes:
        p.join()
    if len(counts_by_ref)==0: 
        print "\nNo reads aligned to any reference sequence. \
        Output files not generated\n"
    else:
        CDP_output(counts_by_ref.copy(), fileFig, fileName, onscreen, no_csv, seq_name_1, 
               seq_name_2, ref_file, nt, pub)   


def CDP_worker(work_queue, counts_by_ref, seq_1, seq_2, nt):
    """
    Worker process - get ref from work queue, aligns reads from seq_1 and seq_2,
    and adds as (x,y) coords to counts_by_ref if there are alignments.  
    """
    try:
        while not work_queue.empty():
            both_aligned = CDP_single(work_queue.get(), seq_1, seq_2, nt)
            if both_aligned is not None:
                counts_by_ref[both_aligned[0]]=(both_aligned[1],both_aligned[2])
    except Exception, e:
        print e
    return True  


def CDP_single(single_ref, seq_1, seq_2, nt):
    """
    Count for boths seqs aligned to single ref
    """

    single_alignment_1 = count_align_reads_to_seq(seq_1, 
                                                        single_ref[1], nt)
    single_alignment_2 = count_align_reads_to_seq(seq_2, 
                                                        single_ref[1], nt)        
    if single_alignment_1 != 0 or single_alignment_2 !=0:
        return (single_ref[0], single_alignment_1, single_alignment_2,)


def CDP_split_shared(seq_1, seq_2, seq_name_1, seq_name_2, ref_file, 
                     nt, fileFig, fileName,min_read_size, max_read_size, 
                     min_read_no, onscreen, no_csv, pub, cores): 
    """
    Refactored CDP code shared between CDP_split and avCDP_split
    """
       
    workers = cores
    work_queue = JoinableQueue()
    processes = []
    mgr=Manager()
    count = 0
    
    refs=Ref_Seq()
    refs.load_ref_file(ref_file)
    
    alignment_dict_1=mgr.dict() #header:aligned_sRNAs
    alignment_dict_2=mgr.dict()
    
    print colored("------------------ALIGNING READS------------------\n",'green') 
    for header,seq in refs:
        work_queue.put((header,seq,)) 
        count+=1
        if count%10000==0:
            for w in xrange(workers):
                p = Process(target=split_CDP_worker, 
                            args=(work_queue, 
                                  alignment_dict_1, 
                                  alignment_dict_2, 
                                  seq_1, 
                                  seq_2,
                                  nt))
                p.start()
                processes.append(p)       

            for p in processes:
                p.join()
    for w in xrange(workers):
        p = Process(target=split_CDP_worker, 
                    args=(work_queue, 
                          alignment_dict_1, 
                          alignment_dict_2, 
                          seq_1, 
                          seq_2, 
                          nt))
        p.start()
        processes.append(p)       

    for p in processes:
        p.join()
       
    alignment_dict_1=alignment_dict_1.copy()
    alignment_dict_2=alignment_dict_2.copy()     

    times_align_1=times_read_aligns(alignment_dict_1)
    times_align_2=times_read_aligns(alignment_dict_2)
    
    header_split_count_1=split_reads_for_header(alignment_dict_1, 
                                                    times_align_1, 
                                                    seq_1)
    header_split_count_2=split_reads_for_header(alignment_dict_2, 
                                                    times_align_2, 
                                                    seq_2)  
    
    
    counts_by_ref = header_x_y_counts(header_split_count_1, 
                                          header_split_count_2, 
                                          refs)  
    if len(counts_by_ref)==0: 
        print "\nNo reads aligned to any reference sequence. \
        Output files not generated\n"
    else:
        CDP_output(counts_by_ref, fileFig, fileName, onscreen, no_csv, seq_name_1, 
               seq_name_2, ref_file, nt, pub)
    

def split_CDP_worker(work_queue, alignment_dict_1, alignment_dict_2, seq_1, 
                     seq_2, nt):
    #calc aligned sRNAs for each header, duplicate if necessary
    
    try:
        while not work_queue.empty():
            single_ref=work_queue.get()
            aligned_reads_1 = dict_align_reads_to_seq_split(seq_1, 
                                                            single_ref[1], nt)
            aligned_reads_2 = dict_align_reads_to_seq_split(seq_2, 
                                                            single_ref[1], nt)
            if len(aligned_reads_1) !=0: #FIX
                alignment_dict_1[single_ref[0]] = aligned_reads_1
            if len(aligned_reads_2) !=0: #FIX
                alignment_dict_2[single_ref[0]] = aligned_reads_2
    except Exception, e:
        print e
    return True    
    

def count_align_reads_to_seq(seq_dict, ref, sRNA_length):
    """
    For non-split alignments!
    
    Return mapped reads for a single ref_seq
    pos is 5' end of read relative to 5' end of fwd strand

    returns an integer
    """
    #start = time.clock()
    
    aligned_count = 0 #number of reads aligned

    count_start = 0
    # indv_seq_align_count = 0

    ref_complement = ref.complement()

    while count_start < (len(ref) - (sRNA_length - 1)):
        query_seq_fwd = DNA(ref[count_start:(count_start + sRNA_length)])
        query_seq_rvs = DNA(ref_complement[count_start:(count_start + sRNA_length)])
        
        if query_seq_fwd in seq_dict:
            aligned_count += seq_dict[query_seq_fwd]
        if query_seq_rvs in seq_dict:
            aligned_count += seq_dict[query_seq_rvs]
        count_start += 1

    return aligned_count


def list_align_reads_to_seq_split(seq_dict, ref, sRNA_length):
    #TODO: this is wrong
    """
    Return mapped reads for a single ref_seq
    pos is 5' end of read relative to 5' end of fwd strand

    returns an integer
    alignment_list --> [sRNA,sRNA,]
    
    """
    count_start = 0
    ref_complement = ref.complement()
    alignment_list = [] #aligned sRNAs
    while count_start < (len(ref) - (sRNA_length - 1)):
        query_seq_fwd = DNA(ref[count_start:(count_start + sRNA_length)])
        query_seq_rvs = DNA(ref_complement[count_start:(count_start + sRNA_length)])
        if query_seq_fwd in seq_dict:
            alignment_list.append(query_seq_fwd)
        if query_seq_rvs in seq_dict:
            alignment_list.append(query_seq_rvs)
        count_start += 1  
    return alignment_list 

def dict_align_reads_to_seq_split(seq_dict, ref, sRNA_length):
    """
    Returns a dictionary with the number of times a read aligns to single
    reference sequence
    Out --> {read:times_aligned}
    
    """
    count_start = 0
    ref_complement = ref.complement()
    split_alignment_dict = {} #aligned sRNAs
    while count_start < (len(ref) - (sRNA_length - 1)):
        query_seq_fwd = DNA(ref[count_start:(count_start + sRNA_length)])
        query_seq_rvs = DNA(ref_complement[count_start:(count_start + sRNA_length)])
        if query_seq_fwd in seq_dict and query_seq_fwd in split_alignment_dict:
            split_alignment_dict[query_seq_fwd]+=1
        elif query_seq_fwd in seq_dict and query_seq_fwd\
         not in split_alignment_dict:
            split_alignment_dict[query_seq_fwd]=1
        if query_seq_rvs in seq_dict and query_seq_rvs in split_alignment_dict:
            split_alignment_dict[query_seq_rvs]+=1
        elif query_seq_rvs in seq_dict and query_seq_rvs\
         not in split_alignment_dict:
            split_alignment_dict[query_seq_rvs]=1
        count_start += 1  
    return split_alignment_dict 

def times_read_aligns(split_alignment_dict):
    """
    Dict. of times a read aligns to all references
    {read: times aligned} 
    """
       
    sRNA_align_counts={}
    for aligned_sRNAs in split_alignment_dict.values():
        for aligned_sRNA, count in aligned_sRNAs.iteritems():
            if aligned_sRNA in sRNA_align_counts:
                sRNA_align_counts[aligned_sRNA] += count
            else:
                sRNA_align_counts[aligned_sRNA] = count
    return sRNA_align_counts


def split_reads_for_header(split_align_dict, split_align_count_dict, seq_dict):
    """
    Dict -->Even split read aligned counts, so total reads aligned = read count
    in original seq file
    {header:split_count}
    """
    
    header_split_count = {}
    for header, sRNA_dict in split_align_dict.iteritems():
        header_split_count[header] = 0
        for sRNA in sRNA_dict:
            header_split_count[header]\
             += ((seq_dict[sRNA]/split_align_count_dict[sRNA])\
                 *split_align_dict[header][sRNA])
    return header_split_count


def header_x_y_counts(header_split_count_1, header_split_count_2, refs):
    """
    For each header in reference that has > 0 alignments in 1 file
    
    dict --> {header: (split counts 1:split counts 2)}
    """
    #construct x,y counts for each header
    counts_by_ref = {}
    for header in refs.headers():
        if header in header_split_count_1 and header in header_split_count_2:
            counts_by_ref[header] = (header_split_count_1[header], 
                                     header_split_count_2[header])
        elif header in header_split_count_1 and header \
        not in header_split_count_2:
            counts_by_ref[header] = (header_split_count_1[header], 0)
        elif header not in header_split_count_1 and header in \
        header_split_count_2:
            counts_by_ref[header] = (0, header_split_count_2[header])
    return counts_by_ref 


def CDP_output(counts_by_ref, fileFig, fileName, onscreen, no_csv, seq_name_1, 
               seq_name_2, ref_file, nt, pub):
    """
    Organise csv or pdf output for CDP analysis
    """
    
    if fileFig or onscreen:
        ref_name = ah.single_file_output(ref_file)
        if fileName == "auto":
            fileName = ah.cdp_file_output(seq_name_1, 
                                       seq_name_2, 
                                       ref_name,
                                       nt, 
                                       "pdf")
        pr.cdp_plot(counts_by_ref, 
                            seq_name_1, 
                            seq_name_2,
                            nt,
                            onscreen,
                            fileFig,
                            fileName,
                            pub)
    
    if no_csv:
        out_csv_name = ah.cdp_file_output(seq_name_1, 
                                           seq_name_2, 
                                           ref_name,
                                           nt, 
                                           "csv")
        
        wtf.cdp_output(counts_by_ref, 
                                 seq_name_1, 
                                 seq_name_2,
                                 out_csv_name) 
