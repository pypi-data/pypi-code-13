#!/home/user/eib202epgs/bin/bin/python
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------------#
# USAGE: ./jx                                                                        #
# AUTHOR: ZJX (Jim Chu), biojxz@gmail.com                                            #
# ORGANIZATION: ECUST                                                                #
# VERSION: 1.0                                                                       #
# CREATED: 2016年04月27日 15时20分01秒                                                 #
#------------------------------------------------------------------------------------#
import log
import yaml
import os,sys


#====================== <1:基于click技术的shell命令程序初始化> ======================#
import click 
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='1.0.0')
def binf():
    pass

#============================= <2:模块内部函数调用程序> =============================#
def procedure(module,procedure):
    global logger
    pwd1=os.getcwd()
    sys.path.append(pwd1)
    sys.path.append('/home/user/eib202epgs/zjx/python/jx-module')
    #logger = log.createCustomLogger('root')
    exec('import %s'%module)
    logger.info('Procedure is begining to run ...')    
    for i in procedure:
        fun = eval("%s.all_function['%s']"%(module,i))  #提取要执行的函数
        logger.info('Start ' + fun.split('(')[0] + ' ...')
        Return = eval(module+'.'+fun) 
        OI = fun.split('(')[0] + ' is over!'
        infor = OI if Return == None else "%s: %s \n%s"%(fun.split('(')[0],Return,OI)
        logger.info(infor)
    logger.info('Procedure is over!!')


#============================== <3: 子程序脚本分割线> ===============================#

#*********************** <3.1:Tnseq原始数据mapping和处理tntr> ***********************#
@binf.command(help='Tnseq site mapping and data treating.')
@click.option('--filename','-f',default='2.Tndata_raw/*',\
help='Please input Tnseq raw data filename.')
@click.option('--length','-l',default=80,\
help="Please input the length of reserved reads,default is 80")
@click.option('--transposon','-t',prompt='Transposon',\
help="Please input transposon abbreviated name,such as 'TcB'.")
@click.option('--pairedend','-pe',is_flag=True,\
help="If you want to analyze single end, please add '-npe'.")
@click.option('--procedure','-p',default='cbus',help='The selection of procedure:\
c:cutadapt;b:bowtie; u:unique;s:site_annot;r:cutreads. Default is cbus.')
def tntr(**kwargs):
    global filename,length,transposon,pe,manifest_data
    ##变量定义
    module = 'tnseqdt'
    filename = kwargs['filename']
    length = kwargs['length']
    transposon = manifest_data['transposon'][kwargs['transposon']]
    pe = kwargs['pairedend']
    dirname = filename.split('/')[0]
    filename = filename.split('/')[-1]
    ##调用全部或部分tnseqdt模块内部的类或函数## 
    if dirname == '2.Tndata_raw':
        procedure(module,kwargs['procedure'])
    else:
        print("Please choose '2.Tndata_raw' folder with '-f' option")
        sys.exit()

#*************************** <3.2:数据可视化命令visualization> **************************#
@binf.command(help='Visualization of Tnseq data.')
@click.option('--dirname','-d',prompt='Dirname',help='Please input objective dirname.')
@click.option('--procedure','-p', default='ws',help='The selection of procedure. \
w:weblogo, s:site_distribution, d:DNAplotter. Default is all.')
def visualization(**kwargs):
    global dirname
    module = 'visualization'
    dirname = kwargs['dirname']
    procedure(module,kwargs['procedure'])

#*************************** <3.3:多个测序库比较命令libvs> **************************#
@binf.command(help='Multi-seq-libraries compare.')
@click.option('--filename1','-f1',help='Please input filename of library1.')
@click.option('--filename2','-f2',help='Please input filename of library2.')
@click.option('--filenames','-fs',help='Please input filenames of librarys.')
@click.option('--procedure','-p', default='l',help='The selection of procedure. \
l:libreadcounts1_vs_libreadcounts2. Default is blastn.')
def libvs(**kwargs):
    global filename1,filename2,filenames
    module = 'libreadcounts1_vs_libreadcounts2'
    filename1 = kwargs['filename1']
    filename2 = kwargs['filename2']
    filenames = kwargs['filenames']
    procedure(module,kwargs['procedure'])

#**************** <3.4:测序序列、引物序列、长序列等序列比对命令blast> ***************#
@binf.command(help='Blast of sequnce and primer seq.')
@click.option('--database','-db',default='',help="Database_name.")
@click.option('--subject','-sj',default='',help='Seq file or folder contain seq.')
@click.option('--query','-q',prompt='query seq',help='Query sequences such as primer.')
@click.option('--task','-t',default='blastn-short',help="Permissible values: 'blastn',\
'blastn-short','dc-megablast','megablast','rmblastn';Default = 'blastn-short'.")
@click.option('--outfmt','-fmt',default=6,help="Formatting options, default is 6")
@click.option('--word_size','-w',default=14,help="Word size for wordfinder algorithm \
(length of best perfect match), default is 16.")
@click.option('--procedure','-p', default='b',help='The selection of procedure. \
b:blastn,i:internal_seq_extract_and_blastn. Default is all.')
def blast(**kwargs):
    import re
    global tag,result_folder,seq_folder,subtype,dbseq,seq,task,outfmt,word_size
    module = 'seqblast'
    proc = kwargs['procedure']
    if kwargs['database']:
        subtype,dbseq = 'db',kwargs['database']
        tag1 = re.split('_|\.',kwargs['database'])[0]
    elif kwargs['subject']:
        subtype,dbseq = 'subject',kwargs['subject']
        tag1 = re.split('_|\.',kwargs['subject'])[0]
        if os.path.isdir(kwargs['subject']):
            proc,seq_folder = 'e' + proc,kwargs['subject']
    else:
        print "Usage: please input subject or database name."
    tag2 = kwargs['query'].split('/')[-1].split('.')[0]
    result_folder = tag2 + '-' + tag1 + '_result'
    tag = tag2 + '-' + tag1
    if kwargs['subject']:
        dbseq = '%s/%s.seq'%(result_folder,tag)
    seq,task = kwargs['query'],kwargs['task']
    outfmt,word_size = kwargs['outfmt'],kwargs['word_size']
    procedure(module,proc)

#*************************** <3.5:必须基因分析esanalysis> **************************#
@binf.command(help='Essential analysis of Ppgene.')
@click.option('--filename','-f',prompt='filename',help='Please input objective filename.')
@click.option('--method','-m',default=1,help='Please input analysis method.Method 1 means \
retain repeated insertion reads, and 2 meads drop repeats. Default is 1.')
@click.option('--all_insert','-a',default=0,help='Total insertion number. Default is CDS \
total insertion number.')
@click.option('--estypefile','-ef',default='Sc.txt',help='Please input estypefile.')
@click.option('--procedure','-p', default='ge',help='The selection of procedure. \
g:gene_insert_density, e:es_mapes. Default is all.')
def esanalysis(**kwargs):
    global filename,method,all_insert,estypefile
    module = 'essential_assay'
    filename = kwargs['filename']
    method = kwargs['method']
    all_insert = kwargs['all_insert']
    estypefile = kwargs['estypefile']
    procedure(module,kwargs['procedure'])
#================================== <4:主程序运行> ==================================#                    
if __name__ == '__main__':
    logger = log.createCustomLogger('root')
    #logger.info('Loading manifest...')
    manifest_file = open('manifest.yaml')
    manifest_data = yaml.load(manifest_file)
    binf()







