
from __future__ import print_function
from pyfaidx import Fasta
import pandas as pd
import numpy as np
from Bio.Seq import Seq
import os

def dnaplotter_artemis(tag):
    #df = pd.read_table('T16728-12b_combined_R1/T16728-12b_combined_R1_alldp.xls',usecols=[0,1,2],names=['chro','site','direct'])
    df = pd.read_table('%s/%s_alldp.xls'%(tag,tag),usecols=[0,1,2],names=['chro','site','direct'])
    CL={'chr1':2798491,'chr2':2394163,"chr3":2245428,"chr4":1778296}
    def chro_proc(chro):
        df_chro = df[df['chro']==chro]
        df_chro = df_chro.groupby(['site','direct'],as_index=False).count()
        #df_chro['plotter'] = np.where(df_chro['direct']=='+',df_chro['chro'],-1*df_chro['chro'])
        df_chro['F'] = np.where(df_chro['direct']=='+',df_chro['chro'],0)
        df_chro['R'] = np.where(df_chro['direct']=='-',-1*df_chro['chro'],0)
        df_coordinate = np.arange(CL[chro])
        df_coordinate = pd.DataFrame(df_coordinate)
        df_map = pd.merge(df_coordinate,df_chro,left_on=0,right_on='site',how='left')
        df_map = df_map.fillna(0)
        df_map_mod = df_map[df_map['site']!=0]
        df_map.to_csv('%s/%s_%s_plus.txt'%(tag,tag,chro),sep='\t',index=False,columns=['F'],header=False)
        df_map.to_csv('%s/%s_%s_minus.txt'%(tag,tag,chro),sep='\t',index=False,columns=['R'],header=False)
        df_map_mod.to_csv('%s/%s_%s_artemis.txt'%(tag,tag,chro),sep='\t',index=False,columns=['site','F','R'])
    for i in range(1,5):
        chro = 'chr' + str(i)
        chro_proc(chro)

def DNAplotter_reads(tag,chromosome,ic='uniq'):
    f1=open('%s/%s_%s_alldp.xls'%(tag,tag,chromosome),"r")
    forward,reverse = {},{}
    CL={'chr1':2798491,'chr2':2394163,"chr3":2245428,"chr4":1778296}
    for i in f1:
        i=i.split()
        n=int(i[1])
        if ic=='uniq':
            if i[2]=='+':
                forward[n]=1
            else:
                reverse[n]=-1
        else:
            if i[2]=='+':
                forward[n]=i[5]
            else:
                reverse[n]=-int(i[5])            
    def Data_transform(d,o,tag,chromosome):
        f2=open('%s/%s_%s_%s.txt'%(tag,tag,chromosome,o),'w')
        chr_length=CL[chromosome]
        for i in range(1,chr_length+1):
            if i in d.keys():
                print(d[i],file=f2)
            else:
                f2.write('0\n')
        f2.close()
    Data_transform(forward,'plus',tag,chromosome)
    Data_transform(reverse,'minus',tag,chromosome)
    f1.close()

def Site_distribution(argv1,argv2):
    wm='w' if argv2=='chr1' else 'a'
    f=open('%s/%s_sd.xls'%(argv1,argv1),wm)
    f1=open('%s/%s_%s_IGS.xls'%(argv1,argv1,argv2))
    for i in f1:
        i=i.split()
        i[1],i[4],i[5]=float(i[1]),float(i[4]),float(i[5])
        if i[1] >= (i[4]+i[5])/2:
            sd=(i[1]-i[5])/1000
        else:
            sd = 1+(i[1]-i[4])/1000
        print(argv2,sd,sep='\t',file=f)
    f.close()
    f1.close()
    f=open('%s/%s_sd.xls'%(argv1,argv1),'a')
    f2=open('%s/%s_%s_CDS.xls'%(argv1,argv1,argv2))
    for i in f2:
        i=i.split()
        i[1],i[7],i[12]=float(i[1]),float(i[7]),float(i[12])
        sd=(i[1]-i[7])/i[12]
        print(argv2,sd,sep='\t',file=f)
    f.close()

def R_sd(tag):
    f=open('%s/%s_sd.R'%(tag,tag),'w')
    
    Rscript="""library("ggplot2")
    fa<-read.table("%s/%s_sd.xls")
    colnames(fa) <-c("Chromosome","Insertion.site")
    fb<-fa[fa[,2]>-3,]
    fb<-fb[fb[,2]<3,]
    pdf("%s/%s_sd.pdf")
    qplot(Insertion.site,data=fb,geom = "density",colour=Chromosome)
    dev.off()
    """%(tag,tag,tag,tag)
    
    print(Rscript,file=f)
    f.close()
    os.system('R2 CMD BATCH %s/%s_sd.R'%(tag,tag))

#def Pichia_TA_weblogo():


def Weblogo(tag):
    f1=open('%s/%s_alldp.xls'%(tag,tag),"r")
    f2=open('%s/%s_base.txt'%(tag,tag),'w')
    #f3=open('%s/%s_basecount.txt'%(tag,tag),"w")
    pichia_genome_path = '/home/user/eib202epgs/zjx/ref/pichia/genome.fa'
    pichia_genome = Fasta(pichia_genome_path)
    seq,count='',0
    D={}
    D2 = {'chr1':'NC_012963.1','chr2':'NC_012964.1','chr3':'NC_012965.1','chr4':'NC_012966.1'}
    """for i in range(1,19):
        D['s'+str(i)+'A']=0  #some site for A
        D['s'+str(i)+'C']=0
        D['s'+str(i)+'G']=0
        D['s'+str(i)+'T']=0"""
    for j in f1:
        count=count+1
        j=j.split()
        chromosome = D2[j[0]]
        site = int(j[1])
        Targetseq = pichia_genome[chromosome][site-9:site+9]
        Targetseq = str(Targetseq)
        if j[2] == '-':
            Targetseq = str(Seq(Targetseq).reverse_complement())
        print('>%s_%d\n%s'%(chromosome,count,Targetseq),file=f2)
        """for k in range(1,18):
            D['s'+str(k)+seq[k-1]]+=1
    for i in range(1,18):
        for j in ['A','C','G','T']:
            print('s'+str(i),j,D['s'+str(i)+j],sep='\t',file=f3)"""
    f1.close()
    f2.close()
    #f3.close()
    os.system("weblogo -c classic --format pdf < %s/%s_base.txt > \
    %s/%s_base.pdf"%(tag,tag,tag,tag))
    