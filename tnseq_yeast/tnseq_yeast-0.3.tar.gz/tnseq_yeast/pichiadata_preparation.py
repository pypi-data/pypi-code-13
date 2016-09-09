# -*- coding: UTF-8 -*-

"""
1，更新毕赤酵母注释信息
2，分析"TA","TTAA"等bases分布
3，目前bases两位点(用于bedtools intersect分析的start && end)暂时为bases第一个碱基分别以染色体起始位点为0和1的对于位点
"""
from __future__ import print_function
import os,re
from pyfaidx import Fasta

def bases_distribution(strain_name,bases):
    ref_path="/home/user/eib202epgs/zjx/ref"
    strain_ref_path="%s/%s"%(ref_path,strain_name)
    bases_distribution_file="%s_%s_distribution"%(strain_name,bases)
    FIN=open('%s.bed'%bases_distribution_file,'w')
    genome_path="%s/genome.fa"%strain_ref_path
    genome=Fasta(genome_path)
    for i in genome.keys():
        seq=str(genome[i][:]).upper()
        for j in re.finditer(bases,seq):
            print(i,j.span()[0],j.span()[0]+1,j.group(),sep='\t',file=FIN)
    FIN.close()
    CMD_intersect="bedtools intersect -a %s/genome.gff -b %s.bed -wa -wb > %s.intersect.xls"\
    %(strain_ref_path,bases_distribution_file,bases_distribution_file)
    os.system(CMD_intersect)
    return CMD_intersect	
    
if __name__ == '__main__':
    import log
    import sys
    logger = log.createCustomLogger('root')
    strain_name=sys.argv[1]
    bases=sys.argv[2]
    logger.info("bases_distribution is begining...")
    CMD_intersect=bases_distribution(strain_name,bases)
    logger.info("The intersect command is '%s'"%CMD_intersect)
    logger.info("bases_distribution is over!")
