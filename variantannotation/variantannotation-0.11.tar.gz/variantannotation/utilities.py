import pandas
import re
import collections
import subprocess
import shlex

def split_string(dataframe, column):
    """ General Split String Function"""
    dataframe[column] = dataframe[column].str.split(pat=';', expand=False)


def to_float(dataframe, column):
    """General Function to return floats"""
    dataframe[column] = dataframe[column].dropna().astype(float)
    dataframe[column] = dataframe[column].where(pandas.notnull(dataframe[column]), None)
    return dataframe[column]


def cell_to_dict(s):
    """When separators are '=' and ';'"""
    as_dict = dict(item.split("=") for item in s.split(";"))
    as_dict["Score"] = float(as_dict["Score"])
    return as_dict

def split_cytoband(x):
    """Specific for splitting cytoband"""
    letters = ['X', 'Y', 'p', 'q']     #Possible letters: Chrm X,Y, or arm regions p (short), or q (long)
    spliced = re.split('(\D+)', x)     #Split letters and numbers
    spliced = filter(None, spliced)
    if any(letter in spliced[0] for letter in letters): spliced[0] = map(None, spliced[0])

    if type(spliced[0]) == type(letters):
        first = spliced[0][0]
        second = spliced[0][1]
        spliced[0] = first
        spliced.insert(1,second)
    return spliced

def lists_to_dict(x):
    """Specific for cytoband. See tests for clearer visualization of the modifications being done"""
    cyto_dict = {'Chromosome': None, 'Arm': None, 'Region': None, 'Band': None, 'Sub_Band': None}
    cyto_dict['Chromosome'] = x[0]
    del x[0]
    cyto_dict['Arm'] = x[0]
    del x[0]

    if '.' in x:
        cyto_dict['Sub_Band'] = int(x[-1])
        del x[-2::]
        if len(x[0]) == 2:
            cyto_dict['Region'] = int(x[0][0])
            cyto_dict['Band'] = int(x[0][1])
        else:
            cyto_dict['Region'] = int(x[0])
        clean_dict = {k: v for k, v in cyto_dict.iteritems() if v is not None}
        return clean_dict

    else:
        if len(x[0]) == 2:
            cyto_dict['Region'] = int(x[0][0])
            cyto_dict['Band'] = int(x[0][1])
        else:
            cyto_dict['Region'] = int(x[0])
        clean_dict = {k: v for k, v in cyto_dict.iteritems() if v is not None}
        return clean_dict


def scrub_dict(d):
    """Clean up dict - after converting everything to dict"""
    if type(d) is dict:
        return dict((k, scrub_dict(v)) for k, v in d.iteritems() if v and scrub_dict(v))
    else:
        return d


def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z

def modify_df(df):
    """Replace dot notation by underscore notation in columns. This will allow proper and easy parsing
    to the MongoDB database (dot notation is not allowed)"""
    cols = df.columns
    cols = cols.map(lambda df: df.replace('.', '_') if isinstance(df, (str, unicode)) else df)
    df.columns = cols
    return df


def expand_list(list_ids):
    """Expand list of HGVS IDS when there are duplicate ids as the same list item"""
    for i in range(0, len(list_ids)):
        if ',' in list_ids[i]:
            base = list_ids[i].split('s')
            first = base[1].split(',')[0]
            second = base[1].split(',')[1]
            old = base[0] + 's' + first
            new = base[0] + 's' + second
            list_ids[i] = old
            list_ids.insert(i + 1, new)
            expand_list(list_ids)
    return list_ids


def convert(data):
    """Given a data structure of unicode-type variables, convert to string each piece of data, recursively"""
    try:
        if isinstance(data, basestring):
            return str(data)
        elif isinstance(data, collections.Mapping):
            return dict(map(convert, data.iteritems()))
        elif isinstance(data, collections.Iterable):
            return type(data)(map(convert, data))
        else:
            return data
    except:
        pass


def final_joint(list1, list2):
    """Join and update lists of dictionaries"""
    print 'Joining lists ...'
    for i in range(0, len(list2)):
        list1[i].update(list2[i])
    return list2


def run_annovar(annovar_path, input_vcf_path, output_csv_path):
    """Run Annovar as  subprocess"""

    args_str = "sudo perl " + annovar_path + "table_annovar.pl " + input_vcf_path + " " + annovar_path + "humandb/ -buildver hg19 -out " + output_csv_path + " -remove -protocol knownGene,tfbsConsSites,cytoBand,targetScanS,genomicSuperDups,gwasCatalog,esp6500siv2_all,1000g2015aug_all,snp138,ljb26_all,cg46,cg69,popfreq_all,clinvar_20140929,cosmic70,nci60 -operation g,r,r,r,r,r,f,f,f,f,f,f,f,f,f,f -nastring . -vcfinput -csvout"
    args = shlex.split(args_str)
    p = subprocess.Popen(args, stdout=subprocess.PIPE)

    return p.communicate()


#PATHS_path = '/Users/carlomazzaferro/Documents/Bioinformatics Internship/Python Codes/variantannotation/variantannotation/PATHS.txt'
#args_str = "sudo perl /database/annovar/table_annovar.pl /data/Nof1/normal_blood_WGS.vqsr.vcf /database/annovar/humandb/ -buildver hg19 -out /data/ccbb_internal/interns/Carlo/annovar_out/SUBPROCESS -remove -protocol knownGene,tfbsConsSites,cytoBand,targetScanS,genomicSuperDups,gwasCatalog,esp6500siv2_all,1000g2015aug_all,snp138,ljb26_all,cg46,cg69,popfreq_all,clinvar_20140929,cosmic70,nci60 -operation g,r,r,r,r,r,f,f,f,f,f,f,f,f,f,f -nastring . -vcfinput -csvout"


