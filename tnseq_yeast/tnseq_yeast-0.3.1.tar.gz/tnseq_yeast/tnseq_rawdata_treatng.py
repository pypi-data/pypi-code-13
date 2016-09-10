#! /usr/local/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import pickle
import shutil
import numpy
import pandas as pd
from Bio.Seq import Seq

#毕赤酵母基因组信息更新    
def chr_annot_update():
    from Bio import Entrez
    if not os.path.exists('chr_annot'):
        #shutil.rmtree('chr_annot')
        os.mkdir('chr_annot')
    Entrez.email="biojxz@163.com"
    Chr={'chr1_annot':'238029138','chr2_annot':'238030677',\
    'chr3_annot':'238032011','chr4_annot':'238033210'}
    for key in Chr:
        f=open('%s.xls'%key,'w')
        handle = Entrez.efetch(db="nucleotide", id=Chr[key],rettype="ft",retmode="text")
        f.write(handle.read())
        f.close()
        shutil.move('%s.xls'%key,'chr_annot')

#毕赤酵母染色体信息格式修改
class Chr_annot_mod():
    def __init__(self):
        """Chr_annot_mod:please input the directory of chromosome annotation \
        files in file_deal function,the default directory is 'chr_annot'
        """ 
    
    def file_deal(self,annot_dir='chr_annot'):
        for i,j,k in os.walk(annot_dir):
            print("\nModifying files as follow:")
            for n in k:
                if '_m' not in n:
                    print(n)
                    self.modify('%s/%s'%(i,n))               
    
    def modify(self,annot_file):    
        f1=open('%s'%annot_file)
        f2=open('%s_m.pkl'%annot_file.split(".")[0],'wb')            
        gene,CDS,annot,Lcds,n={},{},{},[],0       
        #List=[['IGR_s1','IGR_s2','gene_logo','gene_s1','gene_s2','Ori','CDS_s1',\
        #'CDS_s2','Intron_num','CDS_len','Intron_s1','Intron_s2','annot']]
        List=[]
        for i in f1:
            i=i.rstrip()
            i=i.split('\t')
            if i[0] != '':
                try:
                    if i[2]=='gene':
                        CDS[n]=Lcds
                        n=n+1
                        gene[n]=i[4],i[0],i[1]
                        Lcds=[]
                    else:
                        Lcds.append([i[0],i[1]])
                        try:
                            if i[3]=='product':
                                annot[n]=i[4]  #annotation
                        except:
                            pass                               
                except:
                    Lcds.append([i[0],i[1]])
        CDS[n]=Lcds
        End_b,CDS_e_b=0,0
        for i in range(1,n+1):
            count=0
            Start,End=int(gene[i][1]),int(gene[i][2])
            for j in CDS[i]:        
                CDS_s,CDS_e=int(j[0]),int(j[1])
                length=CDS_e-CDS_s    
                if End>Start:
                    length2=End-Start
                    if count>0:
                        List.append([End_b+1,Start-1,gene[i][0],Start,End,'+',\
                        CDS_s,CDS_e,length2+1,length+1,count,CDS_e_b+1,CDS_s-1,annot[i]]) 
                    else:      
                        List.append([End_b+1,Start-1,gene[i][0],Start,End,'+',\
                        CDS_s,CDS_e,length2+1,length+1,count,0,0,annot[i]]) 
                    End_b,CDS_e_b=End,CDS_e
                else:
                    length2=Start-End
                    if count>0:
                        List.append([End_b+1,End-1,gene[i][0],End,Start,'-',\
                        CDS_e,CDS_s,length2+1,-length+1,count,CDS_e_b+1,CDS_e-1,annot[i]])
                    else:
                        List.append([End_b+1,End-1,gene[i][0],End,Start,'-',\
                        CDS_e,CDS_s,length2+1,-length+1,count,0,0,annot[i]])   #,annot[i]
                    End_b,CDS_e_b=Start,CDS_s
                count=count+1
        pickle.dump(List,f2)
        f2.close()

#截短reads读长
def cutreads(Tndata,length):
    f1 = open('2.Tndata_raw/%s_cr'%Tndata,'w')
    f2 = open('2.Tndata_raw/'+Tndata)
    count = 0
    for i in f2:
        i = i.rstrip()
        count += 1
        line = i if count%2 else i[:length]
        print(line,file=f1)
    f1.close()
    f2.close()

#去除reads两端的接头
def cutadapt(Tndata,transposon,tag,pe):
    ADAPTER_FWD = transposon
    ADAPTER_REV = str(Seq(ADAPTER_FWD).reverse_complement())
    ADAPTER_LNK = 'ATACCACGAC'
    ADAPTER_LNK_R = 'GTCGTGGTAT'
    pm_t="-O 17 -e 0.2  --match-read-wildcards --discard-untrimmed -f fastq" 
    pm_l="-O 5 -e 0.1 -m 10 -f fastq"
    if pe:
        Tndata1 = Tndata
        Tndata2 = Tndata.replace("_R1","_R2")
        tag1 = tag
        tag2 = tag.replace("_R1","_R2")
        adapter_rev_p,adapter_link_p = ' -A' + ADAPTER_REV,' -G' + ADAPTER_LNK_R
        os.system('cutadapt -g %s -A %s %s -o 3.Cutadapt_trimmed/%s_t -p 3.Cutadapt_trimmed/%s_t 2.Tndata_raw/%s 2.Tndata_raw/%s'\
        %(ADAPTER_FWD,ADAPTER_REV,pm_t,tag1,tag2,Tndata1,Tndata2))
        os.system('cutadapt -a %s -G %s %s -o 3.Cutadapt_trimmed/%s_t_l -p 3.Cutadapt_trimmed/%s_t_l 3.Cutadapt_trimmed/%s_t 3.Cutadapt_trimmed/%s_t'\
        %(ADAPTER_LNK,ADAPTER_LNK_R,pm_l,tag1,tag2,tag1,tag2))
    else:
        adapter_rev_p,adapter_link_p = '',''
        if tag + '_t' not in os.listdir('3.Cutadapt_trimmed'):
            os.system('cutadapt -g %s %s -o 3.Cutadapt_trimmed/%s_t 2.Tndata_raw/%s'%(ADAPTER_FWD,pm_t,tag,Tndata))
        #cutadapt -a ATACCACGAC -O 5 -e 0.1 -m 10 -f fastq -o 3.Cutadapt_trimmed/tss4_t_l 3.Cutadapt_trimmed/tss4_t
        os.system('cutadapt -a %s %s -o 3.Cutadapt_trimmed/%s_t_l 3.Cutadapt_trimmed/%s_t'%(ADAPTER_LNK,pm_l,tag,tag))
    print("\n========== Cutadapt finished for: %s ==========\n\n"%Tndata) 

#比对毕赤酵母基因组
def bowtie(tag_cutadapt,tag_bowtie):   
    os.system("bowtie -p 16 -v 3 -a --best --strata -m 1 -q pichia/genome \
    3.Cutadapt_trimmed/%s 4.Bowtie_data_dir/%s"%(tag_cutadapt,tag_bowtie))
    #shutil.move(tag_bowtie,'4.Bowtie_data_dir/')
    print("\n========== Bowtie finished for: %s ==========\n\n"%tag_cutadapt)

#去除reads匹配到基因组上相同位点的重复
def unique(file_impt,tag,transposon):
    if not os.path.exists(tag):
        os.mkdir(tag)
    L=['NC_012963.1','NC_012964.1','NC_012965.1','NC_012966.1']

    df=pd.read_table("%s"%file_impt,header=None) 
    #drop the length of site base is less 20bp
    df=df[df[4].map(lambda x:len(x)>=20)].iloc[:,[2,3,1,4]] ##reads读长的限制，gonna to cancell in future
    #site amendment
    if 'TcB' in transposon:
         df['site_amdt'] = numpy.where(df[1]=='+',df[3]+4,df[3]+df[4].str.len()-4)
    if 'SB' in transposon:
        df['site_amdt'] = numpy.where(df[1]=='+',df[3]+1,df[3]+df[4].str.len()-1)
    gb1=df.groupby([2,'site_amdt',4]).count()
    gb2=df.groupby([2,'site_amdt']).count()
    df['sn']=df[4].str.len()
    df=pd.merge(df,gb1,left_on=[2,'site_amdt',4],right_index=True,how='left')

    def dereplicate1(df,n=1,columns1='3_y',columns2='sn'):
        #this sort will miss long length of site base
        return df.sort_values(by=[columns1,columns2])[-n:]
    df=df.groupby([2,'site_amdt'],group_keys=False).apply(dereplicate1)
    df=pd.merge(df,gb2,left_on=[2,'site_amdt'],right_index=True,how='left')\
    .iloc[:,[0,4,2,3,6,8]]

    def dereplicate2(s,n,transposon):  #mark similar reads
        Ls=df[df[2].isin([s])].values
        f1=open("%s/%s_chr%d_alldp.xls"%(tag,tag,n),'w')
        a0,e0,Ta0,D1=0,0,"SS",{}
        for i in Ls:
            [a,c,b,d,e]=i[1:]
            if transposon == 'SB':
                Ta=b[:2] if c=='+' else b[-2:]
            if transposon == 'TcBR' or transposon == 'TcBL':
                Ta=b[3:5] if c=='+' else b[-5:-3]
            if a>a0+3:
                D1[a]='Unique_read'
                a0,c0,e0,Ta0=a,c,e,Ta
            else:
                if c==c0:
                    if Ta=='TA' and Ta0=='TA':
                        if e>e0:
                            if a==a0+1:
                                D1[a],D1[a0]='SimTRemain','Similar'
                            else:
                                D1[a],D1[a0]='SimTRemain','SimT'
                            a0,c0,e0,Ta0=a,c,e,Ta
                        else:
                            if a==a0+1:
                                D1[a],D1[a0]='Similar','SimTRemain'
                            else:                            
                                D1[a],D1[a0]='SimT','SimTRemain'  
                    elif Ta=='TA' and Ta0!='TA':
                        D1[a],D1[a0]='Remain','Similar'
                        a0,c0,e0,Ta0=a,c,e,Ta
                    elif Ta!='TA' and Ta0=='TA':
                        D1[a0],D1[a]='Remain','Similar'
                    else:
                        if e>e0:
                            D1[a],D1[a0]='SimFRemian','Similar'
                            a0,c0,e0,Ta0=a,c,e,Ta
                        else:
                            D1[a0],D1[a]='SimFRemian','Similar'
                else:
                    D1[a]='Unique_read'
                    a0,c0,e0,Ta0=a,c,e,Ta
        before_unique=0
        for i in Ls:
            before_unique=before_unique+1
            if D1[i[1]] not in ['Similar','SimT']:
                f1.write("chr%d\t%d\t%s\t%s\t%d\t%d\t%s\n"\
                %(n,i[1],i[2],i[3],i[4],i[5],D1[i[1]]))
        f1.close()
        os.system("cat %s/*chr*_alldp.xls > %s/%s_alldp.xls"%(tag,tag,tag))
        return before_unique
    D2={}
    for i in range(4):
        d2=dereplicate2(L[i],i+1,transposon)
        D2['befuniq_chr'+str(i+1)]=d2
    return D2

#插入位点分类及修饰处理                                              
def site_annot(argv1,argv2):
    f=open('chr_annot/%s_annot_m.pkl'%argv2,'rb')
    List=pickle.load(f)
    f1=open('%s/%s_%s_alldp.xls'%(argv1,argv1,argv2))
    f2=open('%s/%s_%s_IGS.xls'%(argv1,argv1,argv2),'w')
    f3=open('%s/%s_%s_CDS.xls'%(argv1,argv1,argv2),'w')
    f4=open('%s/%s_%s_Intron.xls'%(argv1,argv1,argv2),'w')
    All_count=IGS_count=CDS_count=Intron_count=0
    List_tail={'chr1':2796884,'chr2':2388753,'chr3':2243457,'chr4':1774176}
    for i in f1:
        All_count=All_count+1
        i=i.split()
        i[1]=int(i[1])
        if i[1]<=List_tail[argv2]:
            for j in List:
                if j[3]>i[1]:
                    IGS_count=IGS_count+1
                    f2.write('%s\t%d\t%s\tIGS\t%d\t%d\t%s\t%d\t%d\t%s\t%d\t%d\
                    \t%d\t%d\t%d\t%d\t%d\t%s\n'%(i[0],i[1],i[2],j[0],j[1],j[2],j[3]\
                    ,j[4],j[5],j[6],j[7],j[8],j[9],j[10],j[11],j[12],j[13]))
                    break
                elif j[4]>=i[1]:
                    if i[1]>=j[6] and i[1]<=j[7]:
                        CDS_count=CDS_count+1
                        f3.write('%s\t%d\t%s\tCDS\t%d\t%d\t%s\t%d\t%d\t%s\t%d\t%d\
                        \t%d\t%d\t%d\t%d\t%d\t%s\n'%(i[0],i[1],i[2],j[0],j[1],j[2],j[3]\
                        ,j[4],j[5],j[6],j[7],j[8],j[9],j[10],j[11],j[12],j[13]))
                        break
                    elif i[1]>=j[10] and i[1]<=j[11]:
                        Intron_count=Intron_count+1
                        f4.write('%s\t%d\t%s\tIntron\t%d\t%d\t%s\t%d\t%d\t%s\t%d\t%d\
                        \t%d\t%d\t%d\t%d\t%d\t%s\n'%(i[0],i[1],i[2],j[0],j[1],j[2],j[3]\
                        ,j[4],j[5],j[6],j[7],j[8],j[9],j[10],j[11],j[12],j[13]))
                        break
        else:
            f2.write('%s\t%d\t%s\tIGS\t%d\t%d\t%s\t%d\t%d\t%s\t%d\t%d\
            \t%d\t%d\t%d\t%d\t%d\t%s\n'%(i[0],i[1],i[2],j[0],j[1],j[2],j[3]\
            ,j[4],j[5],j[6],j[7],j[8],j[9],j[10],j[11],j[12],j[13]))
            IGS_count=IGS_count+1
    print('-----The number of All insertion reads of %s is %d-----'%(argv2,All_count))
    print('-----The number of CDS insertion reads of %s is %d-----\n'%(argv2,CDS_count))
    f.close()
    f1.close()
    f2.close()
    f3.close()
    f4.close()
    return {'All_count':All_count,'IGS_count':IGS_count,'CDS_count':CDS_count,'Intron_count':Intron_count}

#基因内部插入个数及位置
def gene_insert(dirname,chro):
    #df1 = pd.read_table('../chr_annot/chr1_CDS.xls',header=None)
    df1 = pd.read_table('chr_annot/%s_CDS.xls'%chro,header=None)
    #df2 = pd.read_table('T16728-5aTb_combined_R1_chr1_CDS.xls',header=None)
    df2 = pd.read_table('%s/%s_%s_CDS.xls'%(dirname,dirname,chro),header=None)
    df2 = df2.iloc[:,[6,1,7,12]]
    #统计每个基因的插入个数
    gb = df2.groupby(6).size()
    #gb为series格式，需数据框化
    dgb1 = pd.DataFrame(gb)
    df2[13] = (df2[1]-df2[7])/df2[12]
    dgb2 = df2.iloc[:,[0,4]].groupby(6).sum()
    dgb3 = df2.iloc[:,[0,4]].groupby(6).min()
    #outer表示并集
    dgb4 = pd.merge(dgb2,dgb3,left_index=True,right_index=True,how='outer')
    df3 = pd.merge(dgb4,dgb1,left_index=True,right_index=True,how='outer')
    df3['site_ratio'] = df3['13_x']/df3[0]
    df4 = pd.merge(df1,df3,left_on=0,right_index=True,how='outer')
    df4 = df4.iloc[:,[0,7,8,6,2,3,4]].fillna(0)
    ##目前暂定义最小插入位点大于等于0.7的为必须基因
    df4['estag'] = numpy.where((df4['13_y'] > 0) & (df4['13_y'] < 0.7) & (df4['0_y'] > 0),'Non-essential','Essential')
    df4.iloc[:,[0,7,1,2,3,4,5,6]].to_csv('%s/%s_%s_CDS_insert.xls'%(dirname,dirname,chro),sep='\t',header=False,index=False)

def mapes(estype,dirname):  #df1 = pd.read_table('essential_gene/ESpredictbySL.txt',)
    df1 = pd.read_table('essential_gene/%s.txt'%estype,header=None)
    df2 = pd.read_table('%s/%s_CDS_insert.xls'%(dirname,dirname),header=None)
    df = pd.merge(df1,df2,left_on=0,right_on=0,how='right')
    df.to_csv('%s/%s_CDS_insert_es.xls'%(dirname,dirname),sep='\t',header=False,index=False)