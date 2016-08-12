# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 14:40:36 2016

@author: Alexis Eidelman


List of transformation to aggregate a column
There is four parts in that file.
    1 - deals with numeral values
    2 - deals with string values
    3 - deals with date values
    4 - deals with special function, not always aggregating
"""

import pandas as pd
import itertools


### 1 - numbers
def num_drop(x):
    return x.mean()

### 2 - string
def str_drop(x):
    return 'dropped'

def first_letters(x, k=1):
    return x.str[:k]

def last_letters(x, k=1):
    return x.str[k:]

### 3 - date
def date_drop(x):
    return x.min()

def period_by_hours(x, separation):
    ''' aggrege le x par intervale d'heure.
        Le calcul pourrait être simple si on interdisait
        le chevauchement de jour.
    '''
    print(separation)
    assert isinstance(separation, list)
    assert all([sep < 24 for sep in separation])
    separation.sort()

    if 0 in separation:
        separation.append(24)
        hour_categ = pd.cut(x.dt.hour, separation, right=False)
        date_categ = x.dt.date
        return date_categ.astype(str) + ' ' + hour_categ.astype(str)
    else:
        hour = x.dt.hour
        hour_categ = pd.cut(hour, separation, right=False).astype(str)
        night_categ = '[' + str(separation[-1]) + ', ' + str(separation[0]) + ')'
        hour_categ[(hour < separation[0]) | (hour >= separation[-1])] = night_categ
        assert hour_categ.nunique(dropna=False) == len(separation)
        date_categ = x.dt.date.astype(str)
        # décalage d'un jour pour les premières heures
        decale = x.dt.date[x.dt.hour < separation[1]] + pd.DateOffset(days=-1)
        date_categ[x.dt.hour < separation[1]] = decale.astype(str)
        assert all(date_categ.str.len() == 10)
        return date_categ + ' ' + hour_categ


### 4 - special

def combinaison(dataframe, variable) : 

    # D'abord, on cherche toutes les combinaisons de variables

    dico_combinaisons = {}
    for ligne in dataframe[variable] :
        l = []
        modalite_splitée = list(str.split(ligne, " "))
        for subset in itertools.permutations(modalite_splitée, len(modalite_splitée)) : 
            l.append(subset)
        if l not in dico_combinaisons.values() :
            dico_combinaisons[ligne] = l
    return dico_combinaisons

def uniformisation(pandas, pandas_original, variable, dico_combinaisons) :
    for modalite in pandas[variable][pandas_original[variable] != pandas[variable]]:
        combinaisons = []
        modalite_splitée = str.split(modalite, " ou ")
        nombre_mots = len(modalite_splitée)
        if nombre_mots > 1 : 
            for subset in itertools.permutations(modalite_splitée, len(modalite_splitée)) : 
                combinaisons.append(subset)

            for liste_valeurs in dico_combinaisons.values():
                if combinaisons[0] not in liste_valeurs:
                    for modalité_normalisé, combinaison in dico_combinaisons.items():
                        if combinaisons[0] in combinaison :
                            pandas.loc[(pandas[variable]==modalite), variable] = modalité_normalisé  
    return(pandas)