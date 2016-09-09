# -*- coding: utf-8 -*-

#======================================================================
# USAGE: ./tvector_blast.py
# AUTHOR: ZJX (Jim Chu), biojxz@gmail.com
# ORGANIZATION: ECUST
# VERSION: 1.0
# CREATED: 2016年05月29日 16时18分01秒
#======================================================================

"""
开发背景：
Miseq or Hiseq XTen建库中的关键一步——1st(or maybe include 2st)PCR中产物杂质
(fasle-positive)过多，为查明原因，我们目前将PCR产物连接pMD19-T载体后用M13F引物
测序片段的碱基序列。由于测序样品过多及Indx'R' && TcBR-out/SBR-out primer过段的
原因，我们很难用在线ncbi-blast去查明测序片段的成分来源(Indx'R',TcBR-out/SBR-out
 or genome of pichia pastoris).因此，撰写一个可以自动化分析测序结果的脚本很有必
 要。本脚本将成为后续本地化序列比对的基础。
使用说明：
1.将包含测序结果文件(.seq后缀名）的文件夹(download from GWZ email)导入pMD19-T_
exp文件夹(或者含tvector_blast.py & primer.fasta & pichia(db)的其他文件夹；
2.shell中输入python tvector_blast.py <dirname> <word_size = 12> <outfmt = 6>;
"""
import os,re
import pandas as pd
from pyfaidx import Fasta


all_function = {'e':'seq_extraction_merge(tag,result_folder,seq_folder)',
'b':'blastn(tag,result_folder,subtype,dbseq,seq,task,outfmt,word_size)',
'i':'internal_seq_extract_and_blastn(tag,result_folder,subtype,dbseq,seq,task,outfmt,word_size)'}

#tag表示为本次测序文件的标签，由测序文件夹名决定，所以必要时可修改文件夹名
def seq_extraction_merge(tag,result_folder,seq_folder):
    if '.zip' in seq_folder:
        os.system('unzip -q '+seq_folder)
        seq_folder = seq_folder[:-4]
    if not os.path.exists(result_folder):
        os.mkdir(result_folder)
    if not os.path.exists('%s/%s.seq'%(result_folder,tag)):
        os.system("cat %s/*.seq > %s/%s.seq"%(seq_folder,result_folder,tag))

#seq contains short sequences, primer sequences and so on
def blastn(tag,result_folder,subtype,dbseq,seq,task,outfmt,word_size): 
    if not os.path.exists(result_folder):
        os.mkdir(result_folder)
    CMD = "blastn -%s %s -query %s -task %s -word_size %d -outfmt %d -out %s/%s.\
blast%d.xls"%(subtype,dbseq,seq,task,word_size,outfmt,result_folder,tag,outfmt)
    os.system(CMD)
    return CMD
    
def internal_seq_extract_and_blastn(tag,result_folder,subtype,dbseq,seq,task,outfmt,word_size):
    df = pd.read_table("%s/%s.blast6.xls"%(result_folder,tag),header=None)
    #count align_reads of same sample
    gb1 = pd.DataFrame(df.groupby(1).size())
    #gb1 = gb1.drop(1,axis=0)
    #extract min site of internal seq
    gb2 = pd.DataFrame(df.groupby(1)[9].min())
    #extract max site of internal seq
    gb3 = pd.DataFrame(df.groupby(1)[9].max())
    #merge gb1,gb2 and gb3
    df_9merge = gb1.join(gb2)
    df_9merge = pd.merge(df_9merge,gb3,left_index=True,right_index=True,how="left")
    df_9merge.to_csv('%s/%s_Pp.site.xls'%(result_folder,tag),sep='\t',header=False)
    internal_seqf = '%s/%s_Pp.seq'%(result_folder,tag)
    fout = open(internal_seqf,'w')
    Tvector_seq_name = result_folder + '/' + tag + '.seq'
    Tvector_seq = Fasta(Tvector_seq_name)
    with open('%s/%s_Pp.site.xls'%(result_folder,tag)) as f:
        for i in f:
            i = i.split('\t')
            start,end = int(i[2]),int(i[3])
            if start != end:
                # start and end seq of internal(Pp)
                internal_seq = str(Tvector_seq[i[0]][start:end-1])  
                print >>fout,'>'+i[0]+'_internal\n'+internal_seq
        fout.close()   
    CMD = blastn(tag+'_Pp',result_folder,'db','pichia',internal_seqf,'blastn',outfmt,word_size+6)
    #info = "Internal seq blastn Pp is over! The blastn command is '%s'"%CMD
    return CMD
    

if __name__ == "__main__":
    import log,sys
    logger = log.createCustomLogger('root')
    dirname = sys.argv[1]
    tag = re.split("_|/.",dirname)[0]
    
    logger.info("Note: All data results will be in %s_result folder"%tag)
    logger.info("primer.seq blastn %s.seq is begining..."%tag)
    blastn(dirname,tag,'4')
    CMD1 = blastn(dirname,tag,'6')
    logger.info("pr blastn is over!\nThe blastn command is '%s'"%CMD1)
    
    logger.info("%s_Pp.seq is being extracted and blastn pichia.db..."%tag)
    internal_seq_extract_and_blastn(tag,'4')
    CMD2 = internal_seq_extract_and_blastn(tag,'6')
    logger.info("Pp blastn is over!\nThe blastn command is '%s'"%CMD2)
    
    