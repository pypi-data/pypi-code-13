# -*- coding: utf-8 -*-
#libreadcounts1_vs_libreadcounts2
#warning:输入的库文件名filename的开头必须是转座子名称的第一个字母且大写！！

"""
模块功能说明：
1. Readcounts_diff = (Readcounts1 – Readcounts2)/Max(Readcounts1,Readcounts2)
2. 我们定义，两个library的测序reads数差异程度用参数Readcounts_diff表示；
3. 本脚本的作用是比较两个library的测序reads数差异。如某位点仅在lib1中有reads，则Readcounts_diff = 1;
反之,如某位点仅在lib2中有reads,则Readcounts_diff = -1;两个lib都测出reads时-1< Readcounts_diff <1
4. 将两个lib测出的所有sites按染色体位点从小到大进行排序，以排序的序号为横坐标，Readcounts_diff为纵坐标，
绘制散点图(位点插入reads数测序差异图)
5. 位点插入reads数测序差异图可反映两个库的重叠性，进而可在一定程度上判断库的饱和性，转座子随机性和互补性
"""

from __future__ import print_function
import re
import os,sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

##列出所有函数
all_function={'l':'libreadcounts1_vs_libreadcounts2(filename1,filename2)','p':'libs_plus(filenames)'}

def libreadcounts1_vs_libreadcounts2(filename1,filename2):
    #判断lib-filename是否合法
    if (filename1[0] not in 'TS') and (filename2[0] not in 'TS'):
        print("Usage:filename's first letter must be 'S' or 'T'!")   
    pwd=os.getcwd() 

    #以符号'_'或'.'为分隔符，注意点号需要转义
    tag1=re.split("_|\.",filename1)[0]
    tag2=re.split("_|\.",filename2)[0] 
    
    #使用pandas.read_table打开两个要vs(pk)的两个文件
    df1=pd.read_table('%s/%s'%(pwd,filename1),names=['chr','site','orientation','seq','count1','count2','rep'])
    df2=pd.read_table('%s/%s'%(pwd,filename2),names=['chr','site','orientation','seq','count1','count2','rep'])

    #合并两个数据框，同时具有去重复的作用，'outer'表示为并集
    df_merge=pd.merge(df1,df2,on=['chr','site'],how='outer')
    df_merge=df_merge.sort_values(by=['chr','site'])                
    
    #指定在一些列中将缺失值填充０,生成四条染色体文件
    df_merge=df_merge.fillna({'count1_x':0,'count2_x':0,'count1_y':0,'count2_y':0})
    df_merge=df_merge.fillna('NULL')
    
    #计算readcounts差异，生成汇总文件
    df_merge['readcounts_diff']=np.where(df_merge['count2_x']-df_merge['count2_y']>=0,(df_merge['count2_x']-df_merge['count2_y'])/df_merge['count2_x'],\
    (df_merge['count2_x']-df_merge['count2_y'])/df_merge['count2_y'])
    df_merge=df_merge.iloc[:,[0,1,4,5,9,10,12,3,8,6,11,2,7]]
    df_merge.to_csv('%s/%s_%s_alldp.xls'%(pwd,tag1,tag2),sep='\t',header=True,index=False)
    
    #统计，筛选，报告文件生成
    #统计行数,也可以用df1.shape[0]和df1.shape[1]
    df1_rownum=len(df1.index) 
    df2_rownum=df2.shape[0]
    df_merge_rownum=df_merge.shape[0]
    #统计unique_reads
    tag1_muniq=df_merge[df_merge['seq_y']=='NULL']['seq_y'].value_counts()
    tag2_muniq=df_merge[df_merge[u'seq_x']=='NULL']['seq_x'].value_counts()
    
    #报告文件生成
    f=open("%s/%s_%s_report.xls"%(pwd,tag1,tag2),'w')
    print("%s_reads\t%d"%(tag1,df1_rownum),"%s_reads\t%d"%(tag2,df2_rownum),\
    "merge_reads\t%d"%df_merge_rownum,"%s_muniq\t%d"%(tag1,tag1_muniq),\
    "%s_muniq\t%d"%(tag2,tag2_muniq),sep='\n',file=f)
    f.close() 
    
    #绘制散点图
    plt.plot(df_merge['readcounts_diff'],'|',fillstyle='none',markersize=5,color='#00aa00') 
    plt.ylim(-1.03,1.03)
    plt.xlabel('unique_read')
    plt.ylabel('readcounts_diff')
    plt.title('%s_reads vs %s_reads'%(tag1,tag2))
    plt.savefig('%s/%s_reads vs %s_reads.pdf'%(pwd,tag1,tag2),dpi=1080*720)

def libs_plus(filenames):
    filenames_list = filenames.split('/')
    tag,names = '',''
    for i in filenames_list:
        names = names + ' ' + i
        t = i.split('_')[0]
        tag = tag + t
    file_combine = tag + '.xls'
    os.system('cat %s > %s'%(names,file_combine))
    df = pd.read_table(file_combine,header=None)
    df1 = df.iloc[:,[0,1,2]]
    df2 = df1.groupby([0,1]).count()
    print("Uniq reads: %d"%len(df2))
    df2.to_csv('%s_combcount.xls'%tag,sep='\t',header=False)
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:Please input filenames of library1 and library2")
    elif len(sys.argv) == 2:
        filename1=sys.argv[1]
        filename2=sys.argv[2]
        libreadcounts1_vs_libreadcounts2(filename1,filename2)
        