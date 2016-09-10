# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------------#
# USAGE: ./jx                                                                        #
# AUTHOR: ZJX (Jim Chu), biojxz@gmail.com                                            #
# ORGANIZATION: ECUST                                                                #
# VERSION: 1.0                                                                       #
# CREATED: 2016年08月23日 15时20分01秒                                               #
#------------------------------------------------------------------------------------#

from __future__ import print_function
import os
import sys
import numpy
import pandas as pd

all_function = {'g':'gene_insert_density(filename,method,all_insert)','e':'es_map(filename,estypefile)'}

#分析指定文件夹内'*_CDS.xls'类文件的基因内部插入个数及位置
#参考Henry L. Levin的方法，必须基因非必须基因的分界线：20 inserts/kb/million
def gene_insert_density(filename,method,all_insert):
#'gene_length'可能含intron,eg:df = pd.read_table('1a2l8Tb21l22ab/T16728-1a_combined_R1_CDS.xls',usecols=[0,1,6,7,12],names=['chr','insert_site','gene_id','gene_start','gene_length'])
    df = pd.read_table(filename,usecols=[0,1,6,7,12],names=['chr','insert_site','gene_id','gene_start','gene_length'])
    df_annot = pd.read_table('/home/user/eib202epgs/zjx/tnseq/chr_annot/All_CDS.xls',names=['chr','gene_id','gene_length','gene_direct','gene_annot']) #暂时去除基因的方向
    #统计每个基因的插入个数
    if method == 2:
        df = df.groupby(['chr','insert_site'],as_index=False).first()
    gb_size = df.groupby(['chr','gene_id']).size()
    #gb为series格式，需数据框化
    dgb_size = pd.DataFrame(gb_size)
    #计算插入位点在基因ORF的位置，比如在中间则表示为0.5（称之为位点率）
    df['insert_ratio'] = (df['insert_site']-df['gene_start'])/df['gene_length']
    #计算某基因所以插入位点率的综合
    #dgb = df.groupby(['chr','gene_id','gene_length','annot']).count()['insert_site']
    dgb_sum = df.loc[:,['gene_id','insert_ratio']].groupby('gene_id').sum()
    #计算某基因所以插入位点率的最小值
    dgb_min = df.loc[:,['gene_id','insert_ratio']].groupby('gene_id').min()
    #outer表示并集
    dgb_sum_min = pd.merge(dgb_sum,dgb_min,left_index=True,right_index=True,how='outer')
    dgb_merge = pd.merge(dgb_sum_min,dgb_size,left_index=True,right_index=True,how='outer')
    dgb_merge['insert_ratio_x_ave'] = dgb_merge['insert_ratio_x']/dgb_merge[0]
    #基因长度，注释等信息重注释（回归）
    df_merge = pd.merge(df,dgb_merge,left_on=['chr','gene_id'],right_index=True,how='left')
    df_edition1 = df_merge.iloc[:,[0,1,2,4,8,5,7,9]]
    df_edition1.to_csv('%s_edition1.xls'%filename.split('.')[0],sep='\t',index=False,header=['chr','insert_site','gene_id','gene_length','insert_num','insert_ratio','insert_ratio_min','insert_ratio_ave'])
    df_edition1_mod1 = df_edition1.groupby(['chr','gene_id'],as_index=False).first()
    #删除某一列，用drop
    df_edition1_mod2 = df_edition1_mod1.drop(['insert_site','gene_length','insert_ratio'],1)
    df_merge2 = pd.merge(df_annot,df_edition1_mod2,left_on=['chr','gene_id'],right_on=['chr','gene_id'],how='left')
    df_final = df_merge2.fillna(0)
    ##计算所有独立插入
    all_insert_actually = all_insert if all_insert else df_final[0].sum()
    df_final['insert_freq'] = numpy.where(df_final['insert_ratio_y'] < 0.9,(1000000*1000*df_final[0])/(all_insert_actually*df_final['gene_length']),0)
    df_final.iloc[:,[0,1,2,3,5,6,7,8,4]].to_csv('%s_edition2.xls'%filename.split('.')[0],sep='\t',index=False,header=['chr','gene_id','gene_length','gene_direct','insert_num','insert_ratio_min','insert_ratio_ave','insert_freq','gene_annot'])

def esmap_fig(tag1,tag2):
    f=open('%s_%s_esfig_fig.R'%(tag1,tag2),'w')
    Rscript="""library("ggplot2")
    fa<-read.table("%s_%s_esfig.xls")
    colnames(fa) <-c("estype","insert_freq")
    fb<-fa[fa[,2]<600,]
    pdf("%s_%s_esfig.pdf")
    qplot(insert_freq,data=fb,geom = "density",colour=estype)
    dev.off()
    """%(tag1,tag2,tag1,tag2)
    print(Rscript,file=f)
    f.close()
    os.system('R2 CMD BATCH %s_%s_esfig_fig.R'%(tag1,tag2))

def es_map(filename,estypefile):  #df1 = pd.read_table('essential_gene/ESpredictbySL.txt',)
    tag1 = filename.split('.')[0]
    tag2 = estypefile.split('.')[0]
    df1 = pd.read_table('/home/user/eib202epgs/zjx/tnseq/7.essential_analysis/Material/%s'%estypefile)
    df2 = pd.read_table('%s_edition2.xls'%tag1)
    df = pd.merge(df1,df2,left_on='gene_id',right_on='gene_id',how='right')
    df_mod = df.iloc[:,[2,0,1,8,3,4,5,6,7,9]]
    ##去掉未匹配的数据
    df_mod2 = df_mod.dropna()
    df_mod2['estype'] = numpy.where(df_mod2['mapES'].str[-2:]=='ES','Essential','Nonessential')
    df.to_csv('%s_%s_esdata.xls'%(tag1,tag2),sep='\t',index=False)
    df_mod2.to_csv('%s_%s_esfig.xls'%(tag1,tag2),sep='\t',index=False,columns=['estype','insert_freq'],header=False)
    esmap_fig(tag1,tag2)




