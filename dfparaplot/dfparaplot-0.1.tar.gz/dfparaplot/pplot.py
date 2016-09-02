# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 13:43:56 2016

@author: ferdinandleinbach
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools
import matplotlib.lines as mlines
import matplotlib.patches as mpatches


plt.close('all')

def splot(df, x=None, y=None, color=None, 
          linestyle=None, marker=None,ls=None, **kwdargs):
    df_data = df.copy()
    c_split = [""]
    l_split = [""]
    m_split = [""]
    markers = itertools.cycle(["v","o","<",3,4,"+"])
    linestyles = itertools.cycle(['-','--','-.',':'])
    colors = itertools.cycle(["r","y","g","b","p"])
    if not ls==None:
        linestyle = ls
    if x == None:
        x_data = df.index()
    else:
        x_data = df[x]
        df_data = df_data.drop(x,axis=1)
        
    if not color == None:
        c_split = df[color].unique()
        
        df_data = df_data.drop(color,axis=1)   
    if not linestyle == None:
        
        l_split = df[linestyle].unique()
        
        df_data = df_data.drop(linestyle,axis=1)
        
    if not marker == None:
        m_split = df[marker].unique()
        
        df_data = df_data.drop(marker,axis=1)
    c_dict = dict(zip(c_split,colors))
    l_dict = dict(zip(l_split,linestyles))
    m_dict = dict(zip(m_split,markers))
    if y == None:
        y=df_data.columns
    elif isinstance(y,str):
        y = [y]
       
    for c_cond, col in c_dict.items(): 
        if c_cond == "":
            sub1=df
        else:
            sub1 = df[df[color]==c_cond]
        for m_cond, mark in m_dict.items():
            if m_cond == "":
                sub2 = sub1
            else:
                sub2 = sub1[sub1[marker]==m_cond]
            for l_cond, ls in l_dict.items():
                if l_cond == "":
                    sub3 = sub2
                else:
                    sub3 = sub2[sub2[linestyle]==l_cond]
                if x == None:
                    x_data = sub3.index()
                else:
                    x_data = sub3[x]
                for y_col in y:
                    y_data= sub3[y]
                    plt.plot(x_data.values, y_data.values, color = col, 
                             marker=mark, ls=ls, **kwdargs)
                    plt.ylabel(y_col)
    color_handles = [ mlines.Line2D([],[],ls="",label=color)] 
    marker_handles = [ mlines.Line2D([],[],ls="",label=marker) ]
    ls_handles = [ mlines.Line2D([],[],ls="",label=linestyle) ]                
    for c_cond, col in sorted(c_dict.items()):
        color_handles.append( mpatches.Patch(color=col, label=c_cond) )
    for m_cond, mark in sorted(m_dict.items()):
        marker_handles.append( mlines.Line2D([], [], color='black', marker=mark,
                          markersize=10, label=m_cond, ls="") )
    for l_cond, ls in sorted(l_dict.items()):
        ls_handles.append( mlines.Line2D([], [], color='black', ls=ls,
                          label=l_cond) )
    
    l1 = plt.legend(handles=color_handles, loc=2)
    l2 = plt.legend(handles=marker_handles, loc=4)
    l3 = plt.legend(handles=ls_handles, loc=1)
    ax = plt.gca().add_artist(l1)
    ax = plt.gca().add_artist(l2)
    ax = plt.gca().add_artist(l3)
    plt.xlabel(x)

def get_data():  
    dfs2 = []
    for name in ['alcatel_newpipe','alcatel_oldpipe','becker_newpipe','becker_oldpipe']:
        indata=pd.read_csv(name + ".csv", sep=";",skiprows=1, decimal=',')
        dfs= []
        for i in [70,80,90,100]:
            try:
                df1=indata[[x for x in indata.columns if str(i) in x ]+['Flowrate mg/s']].copy()
                df1.columns = ["P1", "P2", "P3"]+['Flowrate']
                df1['MTP']=i
                dfs.append(df1)
            except:
                pass
        df=pd.concat(dfs, ignore_index=True)
        if "catel" in name:
            df["Pump"]="Alcatel"
        else:
            df["Pump"]="Becker"
        if "new" in name:
            df["Pipe"]="new"
        else:
            df["Pipe"]="old" 
        dfs2.append(df)
    df=pd.concat(dfs2, ignore_index=True)
    return df
   
plt.figure()   
df=get_data()              
#splot(df,x="Flowrate",y="P3",color="MTP",marker="Pump",linestyle="Pipe")
splot(df[(df['Pipe']=='new')],x="Flowrate",y="P3",color="MTP",ls="Pipe",marker="Pump")
plt.grid()
        