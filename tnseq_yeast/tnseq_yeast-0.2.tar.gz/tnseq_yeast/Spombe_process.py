from __future__ import print_function
from Bio import Entrez

#从DEG10必须基因数据库中提取S.pombe必须基因的gi
def essential_gi():
    f = open('Sp_es_gi.txt')
    gi_list = []
    for i in f:
        gi_list.append(i.split()[2])
    f.close()
    return gi_list

def extract_NP(id_list):
    f = open('Sp_es_NP.txt','w')
    #eg. id_list = ["429241493","19113749"]
    handle = Entrez.esummary(db="protein", id=",".join(id_list))
    record = Entrez.read(handle)
    NP_list = []
    for key in record:
        NP = record[key]['Extra'].split('|')[3]
        print(NP,file=f)
    f.close()
    return NP_list

if __name__=='__main__':
    id_list = essential_gi()
    extract_NP(id_list)