"""
utilities to edit pyConTextNLP itemData and other stuff in the
Jupyter notebook
"""
from IPython.display import display, HTML, clear_output
import pandas as pd

def get_multi_attribute(i):

    cat = input("Enter %s:\n"%i)
    if isinstance(cat,str):
        return cat
    else:
        return ",".join(cat)
def get_attribute(att):
    attribute = input("Enter value for %s:\n"%att)
    return attribute
def should_edit_attribute(i, attr):
    """
    i: a pandas series containing an individual item
    attr: the attribute to consider editing

    prompt user whether the named attribute should be edited
    """
    clear_output()
    print(i)
    yn = input("Edit %s?\n"%attr)
    try:
        return bool(yn.lower()[0] == 'y')
    except IndexError:
        return edit_attribute(attr)

def create_item():
    """
    create an itemData tuple as a pandas series
    """
    lex = get_attribute("Lex")
    t = get_multi_attribute("Type")
    regex = get_attribute("Regex")
    direction = get_attribute("Direction")
    codes = get_multi_attribute("Codes")
    newitem=pd.Series(data=[lex, t, regex, direction, codes],
                      index=["Lex","Type","Regex","Direction","Codes"])
    return newitem


def edit_item(items, literal):
    """
    items: a pandas DataFrame containing itemData
    literal: a string to match lexical type
    """
    for index, _ in items[items["Lex"] == literal].iterrows():
        if should_edit_attribute(items.loc[index], "Lex"):
            print("editing lex")
            items.loc[index, "Lex"] = get_attribute("Lex")
        if should_edit_attribute(items.loc[index], "Type"):
            items.loc[index, "Type"] = get_multi_attribute("Type")
        if should_edit_attribute(items.loc[index], "Regex"):
            items.loc[index, "Regex"] = get_attribute("Regex")
        if should_edit_attribute(items.loc[index], "Direction"):
            items.loc[index, "Direction"] = get_attribute("Direction")
        if should_edit_attribute(items.loc[index], "Codes"):
            items.loc[index, "Codes"] = get_multi_attribute("Direction")
