import os
import sys
sys.path.append('/Users/carlomazzaferro/Documents/Code/variantannotation-master')

from variantannotation import annotate_batch
from variantannotation import myvariant_parsing_utils
from variantannotation import mongo_DB_export
from variantannotation import create_output_files
from variantannotation import utilities
from variantannotation import MongoDB_querying


#set paths
collection_name = 'Test_Normal_Targeted'
db_name = 'My_Variant_Database'

#set paths
filepath = "/Volumes/Seagate Backup Plus Drive 1/vcf_files/"
csv_file = "normal_targeted_seq.hg19_multianno.csv"
vcf_file = "normal_targeted_seq.vcf"
os.chdir(filepath)


ANNOVAR_PATH = '/database/annovar/'
IN_PATH = '/data/Nof1/file.vcf'
OUT_PATH = '/data/ccbb_internal/interns/Carlo/annovar_results'

#1. Get csv file: run annovar
utilities.run_annovar(ANNOVAR_PATH, IN_PATH, OUT_PATH)

#--------#-------#--------#-------#--------#-------#--------#-------#--------#-------#--------#-------#

#METHOD 1: by chunks, iteratively.
collection_name = 'TEST_ANNOVAR_MyVariant_chunks'
db_name = 'My_Variant_Database'


#Run process, export to MongoDB in-built. Might take some time.
as_batch = annotate_batch.AnnotationMethods()
as_batch.by_chunks(collection_name=collection_name, db_name=db_name, vcf_file=vcf_file, csv_file=csv_file)


#Apply filter(s).
filter_collection = MongoDB_querying.Filters(db_name, collection_name)  #Filter Object

#Three different filters. Let's use the first one.
rare_cancer_variants = filter_collection.rare_cancer_variant()

#Create 4 output files: annotated vcf, annotated csv, filtered vcf, filtered csv
#All files will contain information from myvariant and ANNOVAR; the filtered ones will be much smaller in size.
out_unfiltered_vcf_file = filepath + "/_unfilterd_vcf_annotated.vcf"
out_unfiltered_csv_file = filepath + "/_unfiltered_csv_annotated.csv"

rare_cancer_variants_csv = filepath + "/_rare_cancer_vars.csv"
rare_cancer_variants_vcf = filepath + "/_rare_cancer_vars.vcf"

#The input gzipped vcf file is required to create a filtered one.
in_vcf_file = filepath + "/normal_targeted_seq.vcf.gz"

#Create writer object that pulls data from MongoDB
my_writer = create_output_files.FileWriter(db_name, collection_name)

#Write collection to csv and vcf
my_writer.generate_unfiltered_annotated_csv(out_unfiltered_csv_file)
my_writer.generate_unfiltered_annotated_vcf(in_vcf_file, out_unfiltered_vcf_file)

#cancer variants filtered files
my_writer.generate_annotated_csv(rare_cancer_variants, rare_cancer_variants_csv)
my_writer.generate_annotated_vcf(rare_cancer_variants, in_vcf_file, rare_cancer_variants_vcf)

#---------------#--------------#---------------#--------------#---------------#--------------#---------------#

#METHOD 2: usign full file, and holding it in memory (OK for smaller files)   ##TEST THIS##
#Run process, data saved to joint_list
as_one_file = annotate_batch.AnnotationMethods()
joint_list = as_one_file.full_file(vcf_file, csv_file)

#Name Collection & DB
collection_name = 'ANNOVAR_MyVariant_full'
db_name = 'My_Variant_Database'

#Export
exporting_function = mongo_DB_export.export
exporting_function(joint_list, collection_name, db_name)

#Generate output files
out_vcf_file = filepath + "/Tumor_RNAseq_rare_variants_ANNOTATED_FULL.vcf"
out_csv_file = filepath + "/Tumor_RNAseq_rare_variants_ANNOTATED_FULL.csv"
in_vcf_file = filepath + "/Tumor_RNAseq_rare_variants_VCF.vcf"
create_output_files.generate_annotated_vcf(joint_list, in_vcf_file, out_vcf_file)
create_output_files.generate_annotated_csv(joint_list, out_csv_file)


#Apply filters (as done in method 1)

#---------------#--------------#---------------#--------------#---------------#--------------#---------------#
#METHOD 3: ignore annovar, get data solely from myvariant (much faster, requires nothing but a VCF file.
#will however be incomplete (some variants will have no information).

#Run process
my_variants = annotate_batch.AnnotationMethods()
myvariant_data = my_variants.my_variant_at_once(vcf_file)

#Name Collection & DB
collection_name = 'My_Variant_Info_Collection_Full'
db_name = 'My_Variant_Database'

#Export
exporting_function = mongo_DB_export.export
exporting_function(myvariant_data, collection_name, db_name)

#Apply filters (as done in method 1)

#---------------#--------------#---------------#--------------#---------------#--------------#---------------#
#METHOD 4: ignore annovar, Get data solely from myvariant (much faster, requires nothing but a VCF file.
#will however be incomplete (some variants will have no information).
#Do so BY CHUNKS. Export function is built in the methods myvariant_chunks

#Name Collection & DB
collection_name = 'My_Variant_Info_Collection_Chunks'
db_name = 'My_Variant_Database'

#Run process, export to MongoDB in-built
my_variants = annotate_batch.AnnotationMethods()
myvariant_data = my_variants.myvariant_chunks(chunksize=10000, vcf_file=vcf_file,
                                              collection_name=collection_name, db_name=db_name)

out_vcf_file = filepath + "/Tumor_RNAseq_rare_variants_ANNOTATED_MYV_FULL.vcf"
out_csv_file = filepath + "/Tumor_RNAseq_rare_variants_ANNOTATED_MyV_FULL.csv"
in_vcf_file = filepath + "/Tumor_RNAseq_rare_variants_VCF.vcf"
create_output_files.generate_annotated_vcf(myvariant_data, in_vcf_file, out_vcf_file)
create_output_files.generate_annotated_csv(myvariant_data, out_csv_file)

#Apply filters (as done in method 1)

#---------------#--------------#---------------#--------------#---------------#--------------#---------------#

#Other methods

#Obtain list of variant ID's from a vcf file
open_file = myvariant_parsing_utils.VariantParsing()
variant_list = open_file.get_variants_from_vcf(vcf_file)
#0r, if file is too large to be held in memory:
variant_list = open_file.get_variants_from_vcf_chunk(vcf_file, 10000, 0)

