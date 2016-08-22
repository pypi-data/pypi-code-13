import argparse
import requests
import sys
import csv
import os
import tempfile
import time
#Nonstandard
from bs4 import BeautifulSoup
import mhctools

def main(args_input = sys.argv[1:]):
    parser = argparse.ArgumentParser('pvacseq call_iedb')
    parser.add_argument('input_file', type=argparse.FileType('r'),
                        help="Input FASTA file")
#    parser.add_argument('output_file', type=argparse.FileType('w'),
#                        help="Output file from iedb")
    args = parser.parse_args(args_input)

    count = 1
    fasta_keys = {}
    for line in args.input_file:
        if line.startswith('>'):
            fasta_keys[count] = line.rstrip()
            count += 1

    args.input_file.seek(0, 0)

    method = 'NetMHC4.0'

    if method == 'NetMHC4.0':
        payload = {
            'allele':'HLA-A2902',
            'SEQPASTE':'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA',
            'len':'9',
            'configfile':'/usr/opt/www/pub/CBS/services/NetMHC-4.0/NetMHC.cf',
        }
        request = requests.post('http://www.cbs.dtu.dk/cgi-bin/webface2.fcgi', payload)
        tree = BeautifulSoup(request.content, 'html.parser')
        job_node = tree.find("input", {'name':'jobid'})
        while job_node is not None:
            time.sleep(20)
            jobid = job_node['value']
            request2 = requests.post('http://www.cbs.dtu.dk/cgi-bin/webface2.fcgi', data={'jobid':jobid})
            tree2 = BeautifulSoup(request2.content, 'html.parser')
            job_node = tree2.find("input", {'name':'jobid'})
            print(job_node)
        print(request2.text)
        #print(tree.find(name="jobid").get('value'))
    else:
        sequence_text = args.input_file.read()
        method        = 'ann'
#Need to insert the * in the allele name
        allele        = 'HLA-A*29:02'
        length        = '9'

        data = {
            'sequence_text':sequence_text,
            'method':method,
            'allele':allele,
            'length':length,
        }

        request = requests.post('http://tools-api.iedb.org/tools_api/mhci/', data=data)
        result_file = tempfile.NamedTemporaryFile(mode='w')
        result_file.write(request.text)
        reader = csv.DictReader(open(result_file.name, 'r'), delimiter='\t')

        for line in reader:
            print(line)
            break


        result_file.close()
    args.input_file.close()

if __name__ == "__main__":
    main()
