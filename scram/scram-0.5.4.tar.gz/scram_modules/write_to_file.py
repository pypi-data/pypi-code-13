'''
Created on 22 Jan 2016

@author: steve
'''
"""
Write results to file (csv format)
"""

import csv

def csv_output(alignment_dict, nt, seq_file_name, header):
    """
    Write to file --> csv
    sRNA,pos,count 
    """
    alignment_list=[]
    
    for sRNA, alignment in alignment_dict:
        for i in alignment:
            alignment_list.append((sRNA,i[0],i[1]))
    alignment_list.sort(key=lambda tup : tup[1])
    with open(header+'_'+seq_file_name+'_'+str(nt)\
              +'.csv', 'wb') as csvfile:
        mycsv = csv.writer(csvfile, delimiter=',')
        mycsv.writerow(['sRNA','5-prime nuc. position', 'Count'])
        for alignment in alignment_list:
            out=[str(alignment[0]),alignment[1]+1,alignment[2]]
            mycsv.writerow(out)
    csvfile.close()


def mnt_csv_output(alignment_dict_21, alignment_dict_22, alignment_dict_24,
                    seq_file_name, header):
    """
    For mnt - write 3 seperate csvs for 21,22,24 nt sRNA lengths
    """
    csv_output(alignment_dict_21, 21, seq_file_name, header)
    csv_output(alignment_dict_22, 22, seq_file_name, header)
    csv_output(alignment_dict_24, 24, seq_file_name, header)        

def cdp_output(counts_by_ref, header1, header2, out_file):
    """
    Write to file --> csv
    sRNA, seq1_count, seq2_count
    """
    results_list=[]
    for header, counts in counts_by_ref.iteritems():
        results_list.append((header, counts[0], counts[1]))
    with open(out_file, 'wb') as csvfile:
        mycsv = csv.writer(csvfile, delimiter=',')
        mycsv.writerow(['',header1, header2])
        for result in results_list:
            out=[result[0],result[1], result[2]]
            mycsv.writerow(out)

    csvfile.close()




