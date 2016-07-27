import os
import sys
#sys.path.append('/Users/carlomazzaferro/Documents/Code/variantannotation-master')

from variantannotation import annotate_batch
from variantannotation import myvariant_parsing_utils
from variantannotation import mongo_DB_export
from variantannotation import utilities



"""
from variantannotation import csv_to_df
LOL = csv_to_df.open_and_parse(csv_file)
dft = csv_to_df.parse_to_df(LOL)
"""

#set paths
filepath = "/Users/carlomazzaferro/Desktop/CSV to be tested"
csv_file = "Tumor_targeted_processed.csv"
vcf_file = "Tumor_targeted_seq.vqsr.vcf"
os.chdir(filepath)


#ANNOVAR_PATH = '/database/annovar/'
#IN_PATH = '/data/Nof1/file.vcf'
#OUT_PATH = '/data/ccbb_internal/interns/Carlo/annovar_results'

#1. Get csv file: run annovar
#utilities.run_annovar(ANNOVAR_PATH, IN_PATH, OUT_PATH)


#METHOD 1: by chunks, iteratively.
chunksize = 1000
step = 0
collection_name = 'ANNOVAR_MyVariant_chunks'
db_name = 'My_Variant_Database'

#Get variant list. Should always be the first step after running ANNOVAR
open_file = myvariant_parsing_utils.VariantParsing()
list_file = open_file.get_variants_from_vcf(vcf_file)

#Run process, export to MongoDB in-built
as_batch = annotate_batch.AnnotationMethods()
as_batch.by_chunks(list_file, chunksize, step, csv_file, collection_name, db_name)


#---------------#--------------#---------------#--------------#---------------#--------------#---------------#

#METHOD 2: usign full file, and holding it in memory (OK for smaller files)   ##TEST THIS##

#get variant list. Should always be the first step after running ANNOVAR
open_file = myvariant_parsing_utils.VariantParsing()
list_file = open_file.get_variants_from_vcf(vcf_file)

#Run process, data saved to joint_list
as_one_file = annotate_batch.AnnotationMethods()
joint_list = as_one_file.full_file(list_file, csv_file)

#Name Collection & DB
collection_name = 'ANNOVAR_MyVariant_full'
db_name = 'My_Variant_Database'

#Export
exporting_function = mongo_DB_export.export
exporting_function(joint_list, collection_name, db_name)


#---------------#--------------#---------------#--------------#---------------#--------------#---------------#
#METHOD 3: ignore annovar, get data solely from myvariant (much faster, requires nothing but a VCF file.
#will however be incomplete (some variants will have no information).

#Get variant list form vcf file
open_file = myvariant_parsing_utils.VariantParsing()
list_file = open_file.get_variants_from_vcf(vcf_file)

#Run process
my_variants = annotate_batch.AnnotationMethods()
myvariant_data = my_variants.my_variant_at_once(list_file)

#Name Collection & DB
collection_name = 'My_Variant_Info_Collection_Full'
db_name = 'My_Variant_Database'

#Export
exporting_function = mongo_DB_export.export
exporting_function(myvariant_data, collection_name, db_name)

#---------------#--------------#---------------#--------------#---------------#--------------#---------------#
#METHOD 4: ignore annovar, Get data solely from myvariant (much faster, requires nothing but a VCF file.
#will however be incomplete (some variants will have no information).
#Do so BY CHUNKS. Export function is built in the methods myvariant_chunks

chunksize = 1000
step = 0

#Get variant list from vcf file
open_file = myvariant_parsing_utils.VariantParsing()
list_file = open_file.get_variants_from_vcf(vcf_file)

#Name Collection & DB
collection_name = 'My_Variant_Info_Collection_Chunks'
db_name = 'My_Variant_Database'

#Run process, export to MongoDB in-built
my_variants = annotate_batch.AnnotationMethods()
myvariant_data = my_variants.myvariant_chunks(list_file, chunksize, step, collection_name, db_name)

########DEBUG#########


"""
import os
import sys
#sys.path.append('/Users/carlomazzaferro/Documents/Code/variantannotation-master')

from variantannotation import annotate_batch
from variantannotation import myvariant_parsing_utils
from variantannotation import mongo_DB_export
from variantannotation import utilities


from variantannotation import csv_to_df
import pandas
from variantannotation import utilities
from variantannotation import genotype_calling


LOL = csv_to_df.open_and_parse(csv_file)
df = csv_to_df.parse_to_df(LOL)


df = df.rename(columns={'1000g2015aug_all': 'ThousandGenomeAll'})
df.Chr = df.Chr.replace(to_replace='chrM', value='chrMT')
df['Start'] = pandas.to_numeric(df['Start'])
df['End'] = pandas.to_numeric(df['End'])

print 'Converting columns to float ...'
df["nci60"] = utilities.to_float(df, "nci60")
df["ThousandGenomeAll"] = utilities.to_float(df, "ThousandGenomeAll")
df["ESP6500si_ALL"] = utilities.to_float(df, "ESP6500si_ALL")

print 'Processing knownGene info ...'
utilities.split_string(df, "Func.knownGene")
utilities.split_string(df, "ExonicFunc.knownGene")

print 'Processing tfbsConsSites info ...'
df["tfbsConsSites"] = df["tfbsConsSites"].dropna().apply(utilities.cell_to_dict)

# print 'Processing targetScanS info ...'
# df["targetScanS"] = df["targetScanS"].dropna().apply(utilities.cell_to_dict)


print 'Processing genomicSuperDups info ...'
df["genomicSuperDups"] = df["genomicSuperDups"].dropna().apply(utilities.cell_to_dict)

print 'Processing cytoBand info ...'
df["cytoBand"] = df["cytoBand"].dropna().apply(utilities.split_cytoband)
df["cytoBand"] = df["cytoBand"].dropna().apply(utilities.lists_to_dict)

print 'Creating hgvs key ...'
df['hgvs_key'] = pandas.Series(list_file)

print 'Processing genotype call info ...'
my_sample_id = df["Otherinfo"].dropna().apply(genotype_calling.split_sample_ID)
genotype_call = my_sample_id.apply(lambda x: x[-2::])
dict_split = genotype_call.apply(genotype_calling.return_dict)
df['Otherinfo'] = dict_split
df = df.rename(columns={'Otherinfo': 'Genotype_Call'})

df = utilities.modify_df(df)

print 'Transforming to JSON from dataFrame'
# Clean up dataframe
df_final = df.where((pandas.notnull(df)), None)
list_dict = df_final.T.to_dict().values()

# Attempt to transform dataframe to dictionary
# Set the ID to be the HGVS_ID

print 'cleaning up...'
for i in range(0, len(list_dict)):
    list_dict[i] = utilities.scrub_dict(list_dict[i])

"""




