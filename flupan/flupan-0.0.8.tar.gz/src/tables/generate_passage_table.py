from __future__ import print_function
'''
Creates a file of passage chunks, ie. passage type + # of rounds


Auto generates most, while also incorporating two custom lists of passages: 
 
1. unknown_passages_input.txt
   A single column of uninterpretable passage IDs

2. nonstandard_passages_input.txt
   A set of custom annotations for passages which can't be auto generated

Usage: python generate_passage_table.py

Output is a text file of:
PassageID, General_passage, Specific_passage, # of rounds

ex. RMK5,MONKEYCELL,RHMK,5

'''

def generate_generic():
    '''
    This function generates functional chunks of passaging annotations
    '''


    siat = ["SIAT", "S", "MDCKSIAT"]
    mdck = ["MDCK", "M", "MK"]
    unknowncell = ["C", "X"]
    rhmk = ["RHMK", "RMK", "R", "PRHMK", "RII"]
    tmk = ["TMK"]
    vero = ["VERO", "V"]
    egg = ["AL", "ALLANTOIC", "EGG", "E", "AM", "AMNIOTIC"]
    pigcell = ["PTHYR"]
    chickcell = ["SPFCK", "CK", "PCK"]
    unknown = ["UNKNOWN", "P", "", "NC"]
    rmix = ["R_MIX", "RMIX"]

    minkcell = ["MV_1_LU", "MV1_LU", "MV1_LUNG"]

    caninecell = siat + mdck
 
    monkeycell = rhmk + tmk + vero
    all_cells = caninecell + monkeycell + unknowncell + chickcell + rmix + minkcell

    all_passages = caninecell + monkeycell + egg + unknown + pigcell + unknowncell + chickcell + rmix + minkcell #only_number + minkcell




  
    single_pass = {}
    for num in ["0","1","2","3","4","5","6","7", "8", "9", "10", "X", ""]:
       for passage in all_passages:
          for sep in ["", "_"]:
              #forbidden combos         
              if passage =="X" and num == "X":
                 continue
              if num == "" and sep=="_":
                 continue 
              #if num== "" and sep == "" and passage =="":
              #   continue
              if sep == "_" and num == "X":
                 continue

               
              #annotate specific passage category
              specific_passage = ""
              general_passage= ""


              #Change to a lookup instead of ifs
              if passage in caninecell:

                  if passage in siat:
                       specific_passage = "SIAT"


                  elif passage in mdck:
                       specific_passage = "MDCK"


                  general_passage = "CANINECELL"
              elif passage in monkeycell:

                  if passage in rhmk:
                      specific_passage = "RHMK"

                  elif passage in tmk:
                      specific_passage = "TMK"

                  elif passage in vero:
                      specific_passage = "VERO"
                  general_passage = "MONKEYCELL"

              elif passage in minkcell:
                   specific_passage = "MV1LU"
                   general_passage = "MINKCELL"


              elif passage in chickcell:
                   specific_passage = "CK"
                   general_passage = "CHICKCELL"

              elif passage in pigcell:
                   specific_passage = "PTHYR"
                   general_passage = "PIGCELL"

              elif passage in rmix:
                   specific_passage = "RMIX"
                   general_passage = "RMIX"

              elif passage in unknowncell: 
                   specific_passage = "UNKNOWNCELL"
                   general_passage = "UNKNOWNCELL"


              elif passage in egg: 
                   specific_passage = "EGG"
                   general_passage = "EGG" 


              passage_construct = "".join([passage,sep,num])
              if num == "" or num=="X":
                 num_passages=""
              else:
                 num_passages=num
              annot =  [general_passage, specific_passage, num_passages]

              if annot == "":
                  print("WHAT")
              single_pass[passage_construct]=annot

              #single_pass.append({passage_construct:annot})

    #print(single_pass)
    print(len(single_pass))
    return single_pass



def generate_unpassaged():
    ''' 
    Create annotations for unpassaged sequences
    '''

    unpassaged = ["ORIGINAL_SPECIMEN_UNCULTURED_IN_VTM","OR", "ORIGINAL", "P0", "ISOLATED_DIRECTLY_FROM_HOST_NO", "CLINICAL_SPECIMEN", "NO", "LUNG_1", "LUNG"]
    unpass_dict = {}
    annot  = ["UNPASSAGED", "UNPASSAGED", "0"]

    for desc in unpassaged:
        unpass_dict[desc] = annot
    #print(unpass_dict)
    return unpass_dict


def generate_nonconventional():
    ''' 
    Create annotations for the list of unconventially formatted IDs
    '''

    uncon_dict = {}
 
    with open("nonstandard_passages_input.txt", "r") as nonstandard:
        for line in nonstandard.readlines():
            i = line.rstrip("\n").split(",")
            uncon_dict[i[0]] = i[1:]
 

    #with open("unknown_passages_input.txt", "r") as completely_unknown:
    #    annot = ["", "", ""]
    #    for passage in completely_unknown.readlines():
    #        uncon_dict[passage.rstrip("\n")] = annot


    return uncon_dict


def merge_dicts(*dict_args):
   '''
   from stackoverflow.com/a/26853961
   given any number of dicts, shallow copy and
   merge into a new dict
   '''
   result = {}
   for dictionary in dict_args:
      result.update(dictionary)
   return result


if __name__ == "__main__":
    pass1 = generate_generic()
    unpass = generate_unpassaged()
    uncon = generate_nonconventional()
    #print(pass1)
    #print(uncon)
    full_list = merge_dicts(pass1, unpass, uncon) 
    #print(full_list)
    with open("passage_lookup.txt", "w") as outfile:
         #outfile.write(str(full_list))
        for f in full_list.keys():
           annot = ",".join(str(item) for item in full_list[f])


           outstring = f + "," + annot
           outfile.write(outstring+"\n")







