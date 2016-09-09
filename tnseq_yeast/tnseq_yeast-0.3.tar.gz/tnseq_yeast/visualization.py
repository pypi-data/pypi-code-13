
from __future__ import print_function
import tnseqdata_visualization as tv

all_function = {'w':'weblogo(dirname)','s':'site_distribution(dirname)','d':'dnaplotter_artemis(dirname)'}
def weblogo(dirname):
    if '/' in dirname:
        dirname = dirname[:-1]
    tv.Weblogo(dirname)

def site_distribution(dirname):
    if dirname[-1] == '/':
        dirname = dirname[:-1]
    for i in range(1,5):
        chro = 'chr%d'%i
        tv.Site_distribution(dirname,chro)
    tv.R_sd(dirname)

def dnaplotter_artemis(dirname):
    if dirname[-1] == '/':
        dirname = dirname[:-1]
    tv.dnaplotter_artemis(dirname)
