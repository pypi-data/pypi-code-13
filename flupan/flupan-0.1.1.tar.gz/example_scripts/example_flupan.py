#!/usr/bin/env python
from  __future__  import print_function
import flupan


    
def get_full_annotation(passage):
        '''
        Test example case
        '''

        pp = flupan.PassageParser()
        p = pp.parse_passage(passage)

        print("The input passage:",p.original, sep="\n")
        print("Reformatted passage:",p.plain_format, sep="\n")
        print("Attempted simplified format:", p.coerced_format, sep="\n")
        print("Summary information:", p.summary, sep="\n")
        print("The order of passage rounds:",p.ordered_passages, sep="\n")
        print("Total number of passages:", p.total_passages, sep="\n")
        print("Minimum number of passages:", p.min_passages, sep="\n")
        print("General passage type(s) of each passage round:",p.general_passages, sep="\n")
        print("More specific passage type(s):",p.specific_passages, sep="\n")
        print("Each round of passage:", p.passage_series, sep="\n")
        
def get_nth_passage(passage, n):
        pp = flupan.PassageParser()
        p = pp.parse_passage(passage, n)
        print("The ", str(n), "rd passage is ", p.nth_passage, sep="")    
       

 
if __name__ == "__main__":

    print("EXAMPLE 1")
    print("Get annotations for passage M1_S3")
    get_full_annotation("M1_S3")

    print("\n---------------------------")
    print("EXAMPLE 2")
    print("Get annotations for passage MX_S1 w/ indeterminate # of rounds of passages")
   
    get_full_annotation("MX_S1")

    print("\n---------------------------")
    print("EXAMPLE 3")
    print("Get annotations for passage m1_s1+2 w/ assumption that s1+2 = s3")
   
    get_full_annotation("m1_s1+2")

    print("\n---------------------------")
    print("EXAMPLE 4")
    print("Get the 3rd round of passage fo M1_S2")
    get_nth_passage("M1_S2", 3)


   

