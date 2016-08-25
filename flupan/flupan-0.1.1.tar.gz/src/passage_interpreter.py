from __future__ import print_function
import re
import logging
import pkgutil

class PassageAnnotation:
    def __init__(self, nth_passage=""): 
        #The raw input ID
        self.original = ""

        #Input ID, capitalized, spec characters removed
        self.plain_format = ""
 
        #Try to get plain_format ID into consistent format
        self.coerced_format = ""
 
        #Convenience list of annotations for a passage
        self.summary = ['','','','','','','']


        #The minimum number of passage round that occurred. Could be higher
        #Ex. SIAT3_EGG had to have been passaged at least 4 times
        self.min_passages = ""

        #If possible to determine, the exact total annotated rounds of passaging
        self.total_passages = ""

        #If requested, get the identity of the nth passage
        self.nth_passage = ""

        #Each round of passaging, separated into a list
        #Ex. ["MDCK3", "RH3"]
        self.ordered_passages = []

        #The species/general type of the passages
        #Ex. CANINECELL, MONKEYCELL
        self.general_passages= []

        #More specific type of passage, if known
        #["MDCK", "RHMK"], etc.
        self.specific_passages = []

        #The order of specific passages
        #Ex. [[1, 'SIAT'], [2, 'SIAT'], [3, 'EGG'], [4, 'EGG']]
        self.passage_series = []


        
 

class PassageParser:
    def __init__(self): 
        '''
        Set up logging, open reference tables
        '''
  
        #Set up logging
        LOG_FILENAME = 'flupan.log'

        self.logger = logging.getLogger()
        filehandler = logging.FileHandler(LOG_FILENAME, mode="a")
        formatter = logging.Formatter('Line %(lineno)d: %(message)s')

        filehandler.setFormatter(formatter)
 
        if not self.logger.handlers:
            self.logger.addHandler(filehandler)


        self.logger.setLevel(logging.INFO)

        #Open reference table for coerce_format()
        replacements_file = pkgutil.get_data('flupan.tables', 'coerce_format.txt')
       
        #pkgutil get_data mysteriously adds extra blank line 
        self.replacements = replacements_file.split("\n")[:-1]
       
 
        #Open reference table for main passage parsing               
        lookup_file = pkgutil.get_data('flupan.tables', 'passage_lookup.txt')
        self.lookuptable = {}    

        for raw_entry in lookup_file.split("\n"):

            entry = raw_entry.rstrip("\n")
            entry_list = entry.split(",")

            self.lookuptable[entry_list[0]]=entry_list[1:4]
            


    def spec_char_strip(self, ID):
        ''' 
        Replaces special characters with underscores
        Compresses redundant series of underscores with a single underscore
        Replaces uninformative words 
        ''' 
        # Because a hyphen (-) most always appears between a passage type and # of rounds    
        # Remove hyphens 
        # Ex. EGG-4 -> EGG4
        record_strip = ID.replace("-", "")

        #Replace things that aren't alphanumeric with an underscore
        record_strip = re.sub('[^A-Z0-9\|]', '_', record_strip)
        #Remove not useful words
        record_strip = re.sub('PASSAGE_DETAILS_|_AND_|ST_PASSAGE|ND_PASSAGE|PASSAGING|_PASSAGE|_PASSAGES|_PASSAGE_|_PASSAGES_|_CELLS', '', record_strip)
        #Get rid of repeated underscores from replacements and deletions
        while "__" in record_strip:
            record_strip = record_strip.replace("__", "_")

        if len(record_strip) > 0:
            #Get rid of leading and trailing underscores
            if record_strip[0] == "_":
                record_strip = record_strip[1:]
            if record_strip[-1] == "_":
                record_strip = record_strip[:-1]

        return record_strip

    def format_ID(self, ID):
        '''
        Gets passage annotation into a consistent format for lookup
        Asserts that ID is a string
        '''

        assert type(ID)==str
        uppercase_ID = ID.upper()
        formatted_ID = self.spec_char_strip(uppercase_ID)
        

        return formatted_ID

    def coerce_annotation_format(self, annotation_list):
        '''
        This function coerces the most common passage IDs into a more standard format
        Removes underscores which occur inside a single annotation
        If a set of passaging annotation standards are released, this 
        will be the function to make old annotations consistent with them
        '''
        msg = "---Coerced into standard format---"
        self.logger.info(msg)
 
        coerced_format_list = []
        for annot in annotation_list:
             for replacement in self.replacements:
                rep_list = replacement.split(" ")
                annot = annot.replace(rep_list[0], rep_list[1].rstrip("\n"))

                annot = annot.replace("_", "")                    
                 
             coerced_format_list.append(annot)  





        msg = "Precoerced format list: " + str(annotation_list)
        self.logger.info(msg)
        msg = "Coerced format list: " +  str(coerced_format_list)
            
        self.logger.info(msg)
        coerced_format = "_".join(coerced_format_list)
        msg = "Final coerced format: " +  coerced_format
        self.logger.info(msg)

              
              
 
        return coerced_format



    def make_annotation(self, annotation_list):
       '''
       This function takes a list of passage IDs found in 
       the full passage ID, and then consolidates their annotations 
       It needs the dictionary from lookup_table.txt as a reference to 
       lookup annotations
       '''
       concat_general_passage = ""
       concat_specific_passage = ""
       cumulative_num_passages= ""
       qualifier = "exactly"

       msg = "---Consolidate annotations---"
       self.logger.info(msg)
 
       msg = "Passage List: " + str(annotation_list)
       self.logger.info(msg)
  
       assert type(annotation_list)== list
       assert type(self.lookuptable) == dict
       for passage in annotation_list:
            annot = self.lookuptable[passage]
            msg = "Individual passage:" + passage + " " + str(annot)
            self.logger.info(msg)
            
            tmp_passage = passage.replace("_", "")
            #Consolidate the general passage summary
 
            #If it's the first passage in the list

            if concat_general_passage == "":
                concat_general_passage = annot[0]

            #If the passage has already occurred, don't change anything
            elif annot[0] in concat_general_passage:
                concat_general_passage = concat_general_passage

            #If the ID is just a number, assume it was in the passage condition of
            #the previous ID. 
            #Ex. EGG5_1 = EGG6 essentially. 
            elif tmp_passage in ["1","2","3","4","5","6","7","9","10","11","12"]:
                concat_general_passage = concat_general_passage

            elif annot[0] == "":
                concat_general_passage = ""

            else:
                concat_general_passage = "+".join([concat_general_passage, annot[0]])



            #Consolidate the specific passage summary
            #Same idea as above 



            if concat_specific_passage == "":
                concat_specific_passage = annot[1]
            elif annot[1] in concat_specific_passage:
                concat_specific_passage = concat_specific_passage
            elif tmp_passage in ["1","2","3","4","5","6","7","9","10","11","12"]:
                concat_specific_passage = concat_specific_passage
            elif annot[1] == "":
                concat_specific_passage = ""
            else:
                concat_specific_passage = "+".join([concat_specific_passage, annot[1]])
 

            msg = "---Add up number of passages---"
            self.logger.info(msg)
        
            #Add up numbers of passages
            #Some annotations don't have numbers, so can't be added
            if str(annot[2]) == "":
         
                qualifier  = "atleast"

            if cumulative_num_passages == "":
                try:
                   cumulative_num_passages = str(eval(annot[2]))
                   


                except:
                   #indeterminate passages happen at least once
                   cumulative_num_passages = "1"
                   qualifier = "atleast"                
            else:
                try:
                   cumulative_num_passages = str(eval(cumulative_num_passages) + eval(annot[2])) 

                except:
                   #if any passage has an indeterminate number of rounds,
                   #it happened at least once
                   qualifier = "atleast"                
                   cumulative_num_passages = str(eval(cumulative_num_passages) + 1) 

       general_passages_list = concat_general_passage.split("+")
       assert type(general_passages_list) == list

       specific_passages_list = concat_specific_passage.split("+")
       assert type(specific_passages_list) == list

       coerced_format = self.coerce_annotation_format(annotation_list)
       assert type(coerced_format) == str

       min_passages = eval(cumulative_num_passages)

       #If any of  passage doesn't have a number, can't get exact total 
       if  qualifier == "atleast":
            total_passages = ""

       #Can only get total number of rounds if there's an exact count
       elif qualifier == "exactly":
            total_passages = eval(cumulative_num_passages)

       summary =  [coerced_format, concat_general_passage, concat_specific_passage, qualifier, cumulative_num_passages]
       msg = "Summary: " + str(summary)
       self.logger.info(msg)

       return summary, coerced_format, general_passages_list, specific_passages_list, min_passages, total_passages  



    def get_nth_passage(self, n, passage_series):
        '''
        Get the type of the nth round of passaging
        '''
        #If an n is provided by user...
        if n != "":
            #If a passage series could be determined by get_series()...
            if passage_series is not []:
               for entry in passage_series:  
                    #Get the nth passage
                    if entry[0] == n:
                        nth_passage = entry[1]
               return nth_passage

    def get_series(self, annotation_list):
       '''

       Get a series of passage rounds, 
       EGG2_M1 => [1, EGG], [2,EGG], [3,MDCK], etc.
       Setup for getting the nth passage function
       '''
       msg = "---get series of passaging rounds---"
       self.logger.info(msg)
 

       prev_annot = ""
       prev_i = 0
       passage_series = []
       for passage in annotation_list:
            annot = self.lookuptable[passage]
            #If any annot[2] (num_passage) is not a number,
            #will cause exception and just return nothing
            try: 
                #num passages
                #self.logger.info(annot[2]) 
                #for round in number of passages that occur
                for i in range(1, eval(annot[2])+1):

                   #If there's a passage type, use it
                   if annot[1] != "":
                        passage_series.append([ i + prev_i, annot[1]])
                        prev_annot = annot[1]

                   #Else, if the previous annotation's passage type isn't empty, 
                   #use previous annotation
                   elif prev_annot != "":
                        passage_series.append([i + prev_i, prev_annot])
                #Keep track of cumulative number of rounds    
                prev_i = eval(annot[2])
            except:
                return passage_series
       return passage_series
                                   




    def match_known_passage(self, formatted_ID):
        '''
        This function looks for known passage annotations within 
        ihe formatted input passage identifiers
        If the full passage can't be accounted for,
        ""s are returned
        '''
 
        msg = "---Search for known passage annotations in input passage ID---"
        self.logger.info(msg)
        
        tmp_ID = formatted_ID
        longest_match = ""
        matches = []
        msg = "Input ID: " + formatted_ID
        self.logger.info(msg)
        #Searches for up to different 5 passage rounds
        for i in [1,2,3,4, 5]:

            msg = "Search round: " + str(i)
            self.logger.info(msg)
   
            #find the longest known passage in input passage ID
            for key in self.lookuptable.keys():
               if key in tmp_ID:
                   if len(key) > len(longest_match):
                       longest_match = key
                       msg = "current longest match: " + str(key)
                       self.logger.info(msg)
            #If no match, try getting rid of underscores
            if longest_match == "":
                tmp_ID = tmp_ID.replace("_", "")
                for key in self.lookuptable.keys():
                    if key in tmp_ID:
                        if len(key) > len(longest_match):
                            longest_match = key
                            msg = "current longest match: " + str(key)
                            self.logger.info(msg)
            #If the full passage ID is accounted for
            if len(tmp_ID)==0: 
               continue 
            #The full passage ID is accounted for if only _ 's are left
            if len(tmp_ID.replace("_", "")) == 0:
               continue     

            #The full passage ID is accounted for if only a single number left
            if tmp_ID.replace("_", "") in [1,2,3,4,5,6,7,8,9] :
               continue     

              
 
            #Make list of matches
            matches.append(longest_match)

            #Get rid of current match to search rest of ID for more matches            
            tmp_ID = tmp_ID.replace(longest_match, "", 1)
            longest_match = "" 
            msg = "Remaining ID to parse: " + tmp_ID
            self.logger.info(msg)
        #If the full passage can't be parsed, return ""           


        #If full passage can't be accounted for, return ""s
        if len(tmp_ID.replace("_", "")) > 0 and tmp_ID.replace("_", "") not in [1,2,3,4,5,6,7,8,9]:
            return ""



        else:
            #Need to get ordering of the found matches within input ID
            self.logger.info(matches)
            match_order = []
            msg = "---Determine order of matches--"
            self.logger.info(msg)
            msg = "Unordered passages: " + str(matches)
            self.logger.info(msg)
 
            for match in matches:
                 match_order.append(formatted_ID.find(match))

            msg = "Order of matches: " + str(match_order)
            self.logger.info(msg)
 
            #Get matches are in the same order as they appear in the ID    
            
            ordered_passages = [x for y, x in sorted(zip(match_order, matches))]  
            msg = "Final passage  order: " + str(ordered_passages)
            self.logger.info(msg)
            self.logger.info("done ordering")
            return ordered_passages    



    def parse_passage(self, ID, n = ""):
        '''
        control function 
        '''
        #Start logging

        ID = ID.rstrip("\n")
  
        pa = PassageAnnotation() 

        #Store input ID
        pa.original = ID

        msg = "---Begin parsing annotation---"
        self.logger.info(msg)

        
        msg = "Starting input Passage ID: " + ID
        self.logger.info(msg)



        #If there is no annotation, return default values
        if ID == "":
             return pa

        #Make the ID all caps, remove special characters
        formatted_ID = self.format_ID(ID)

        #Store plain format
        pa.plain_format = formatted_ID
      
        #Match a formatted ID to its composite passage types

        ordered_passages  =  self.match_known_passage(formatted_ID)


        pa.ordered_passages = ordered_passages



        if ordered_passages:

            annot_series = self.get_series(ordered_passages)  
            pa.passage_series = annot_series

            annotation = self.make_annotation(ordered_passages)
            if annotation:

                output = annotation[0]
                #Convenience output list
                summary = [ID, formatted_ID, output[0], output[1], output[2], output[3], output[4]]
 
                pa.summary = summary
                pa.coerced_format = annotation[1]
                pa.general_passages = annotation[2]
                pa.specific_passages = annotation[3]
                pa.min_passages = annotation[4]
                pa.total_passages = annotation[5]

                msg = "Successful annotation" + str(pa.summary)
                self.logger.info(msg)


                pa.nth_passage = self.get_nth_passage(n, annot_series)
        else:
            pa.summary = [ID, formatted_ID,'','','','','']
            msg = "Failed annotation" + str(pa.summary)
            self.logger.info(msg)

               
        return pa        








