
import os
import data_loader
import identifier
import rule_generator

def run(root_dir):
    df_paths = data_loader.load_domain_file_paths(root_dir)
    for (domain_name, filepath_list) in df_paths.items():
        for filepath in filepath_list:
            mapping = identifier.identify(filepath)
            cluster_dir = '/'.join(filepath.split('/')[:-1])
            rule_generator.generate(mapping, cluster_dir, show_extractions=True)

        # break

if __name__ == '__main__':
    run('../../dig-data/sample-datasets/escorts/')