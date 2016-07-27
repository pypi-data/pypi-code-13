
import os
import sys
import data_loader
import identifier
import rule_generator

FILIENAME_RULES_STEP01 = 'step01_rules.json'
FILIENAME_RULES_STEP02 = 'step02_rules.json'
FILIENAME_EXTRACTIONS_STEP01 = 'step01_extractions.jl'
FILIENAME_EXTRACTIONS_STEP02 = 'step02_extractions.jl'


def run_same_dirpath(root_dir):
    df_paths = data_loader.load_domain_file_paths(root_dir)
    for (domain_name, filepath_list) in df_paths.items():
        
        if domain_name[0] == '.':
            continue
        print 'process: ', domain_name

        for filepath in filepath_list:
            filename = filepath.split('/')[-1]
            if filename[0] == '.':
                continue
            cluster_dir = '/'.join(filepath.split('/')[:-1])
            # print cluster_dir
            
            if int(cluster_dir[-3:]) > 3:
                continue
            # print filepath
            # print 'cluster_dir', '#',int(cluster_dir[-3:])

            print '-', cluster_dir.encode('ascii', 'ignore')
            step01_rule_path = os.path.join(cluster_dir, FILIENAME_RULES_STEP01)
            step02_rule_path = os.path.join(cluster_dir, FILIENAME_RULES_STEP02)
            step01_extraction_path = os.path.join(cluster_dir, FILIENAME_EXTRACTIONS_STEP01)
            step02_extraction_path = os.path.join(cluster_dir, FILIENAME_EXTRACTIONS_STEP02)
            do_ani(step01_extraction_path=step01_extraction_path, step01_rule_path=step01_rule_path, step02_extraction_path=step02_extraction_path, step02_rule_path=step02_rule_path)

def run4memex(step01_extraction_dirpath, step01_rule_dirpath):
    step01_extraction_paths =  [_ for _ in os.listdir(step01_extraction_dirpath) if _[0] != '.']
    step01_extraction_mappings = {'.'.join(_.split('/')[-1].split('.')[:-1]):os.path.join(step01_extraction_dirpath, _) for _ in step01_extraction_paths}
    step01_rule_mappings = data_loader.load_domain_file_paths(step01_rule_dirpath)

    # print step01_extraction_mappings

    for key, step01_extraction_path in step01_extraction_mappings.iteritems():
        # print step01_extraction_mappings
        # print key
        # step01_extraction_path = step01_extraction_path
        if key not in step01_rule_mappings:
            continue
        step01_rule_paths = step01_rule_mappings[key]
        for step01_rule_path in step01_rule_paths:  # for clusters

            step02_rule_path = os.path.join('/'.join(step01_rule_path.split('/')[:-1]), FILIENAME_RULES_STEP02)

            do_ani(step01_extraction_path, step01_rule_path, step02_rule_path=step02_rule_path)





            
def do_ani(step01_extraction_path, step01_rule_path, step02_extraction_path=None, step02_rule_path=None):
    mapping = identifier.identify(step01_extraction_path)
    rule_generator.generate(mapping, step01_extraction_path=step01_extraction_path, step01_rule_path=step01_rule_path, step02_extraction_path=step02_extraction_path, step02_rule_path=step02_rule_path)



    
