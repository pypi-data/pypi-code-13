#!usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import tnseq_rawdata_treatng as tntr
import os,sys
import re
#import multiprocessing

##列出所有函数
all_function = {'r':'cutreads(filename,length)','c':'cutadapt(filename,transposon,pe)','b':'bowtie()',\
'u':'unique(transposon)','s':'site_annot(filename)','w':'weblogo(filename)','i':'gene_insert(filename)',\
'm':'mapES(filename)'}

filename_cr = ''
tag = ''
tag_cutadapt = ''
tag_bowtie = ''

def cutreads(filename,length):
    global filename_cr
    if filename[-3:] == '.gz':
        os.system('gunzip 2.Tndata_raw/%s'%filename)
        filename=filename[:-3]
    tntr.cutreads(filename,length)
    filename_cr = filename + '_cr'

def cutadapt(filename,transposon,pe):
    global tag,tag_cutadapt
    if filename_cr:
        filename = filename_cr
    tag=re.split('\.',filename)[0]
    tag_cutadapt=tag+'_t_l'
    if filename[-3:] == '.gz':
        os.system('gunzip 2.Tndata_raw/%s'%filename)
        filename=filename[:-3]
    if tag_cutadapt not in os.listdir('3.Cutadapt_trimmed'):
        tntr.cutadapt(filename,transposon,tag,pe)

def bowtie():
    global tag_bowtie
    tag_bowtie=tag+'_bowtie.txt'
    if tag_bowtie not in os.listdir('4.Bowtie_data_dir'):
        tntr.bowtie(tag_cutadapt,tag_bowtie)

def unique(transposon):
    if not os.path.exists(tag):
        os.system('mkdir %s'%tag)
    if tag+'_chr4_alldp.xls' not in os.listdir(tag):
        tntr.unique('4.Bowtie_data_dir/'+tag_bowtie,tag,transposon)

def site_annot(filename):
    global tag
    tag = re.split('\.',filename)[0]
    num_all,num_CDS = 0,0
    num_dict = {}
    for j in range(1,5):
        j='chr'+str(j)
        num_dict = tntr.site_annot(tag,j)
        num_all = num_all + num_dict['All_count']
        num_CDS = num_CDS + num_dict['CDS_count']
    print('-----The number of All insertion reads is %d-----'%num_all)
    print('-----The number of CDS insertion reads is %d-----\n'%num_CDS)
    os.system('cat %s/*chr*_CDS.xls > %s/%s_CDS.xls'%(tag,tag,tag))
    os.system('cat %s/*chr*_IGS.xls > %s/%s_IGS.xls'%(tag,tag,tag))

def gene_insert(filename):
    dirname = re.split('\.',filename)[0]
    for i in range(1,5):
        chro = 'chr' + str(i)
        tntr.gene_insert(dirname,chro)
    os.system('cat %s/*chr*_CDS_insert.xls > %s/%s_CDS_insert.xls'%(dirname,dirname,dirname))

def mapES(filename):
    dirname = re.split('\.',filename)[0]
    tntr.mapes('ESpredictbySL',dirname)
"""
def tnseqmaptr_all(transposon): 
    def tsmt(filename,transposon):  
        Tnseqmaptr(filename,transposon).cutadapt()
        Tnseqmaptr(filename,transposon).bowtie()
        Tnseqmaptr(filename,transposon).unique()
        Tnseqmaptr(filename,transposon).site_annot()
        weblogo(filename)
    #pool=multiprocessing.Pool(4)
    for i in os.listdir('2.Tndata_raw'):
        multiprocessing.Process(target=tsmt,args=(i,transposon,)).start()
        #p.join()
"""

if __name__=='__main__':
    transposon=sys.argv[1]
    """for i in range(1,5):
        tn.Weblogo('Thm2','chr'+str(i))
    except Exception,ex: 
        os.system("echo '%s:%s' | mail -s 'Infor' \
        347909696@qq.com,biojxz@163.com"%(Exception,ex))  """       
    
    
    


            
