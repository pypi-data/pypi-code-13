#!/usr/bin/env python

""" MultiQC module to parse output from FastQ Screen """

from __future__ import print_function
from collections import OrderedDict
import json
import logging
import re

from multiqc import config, BaseMultiqcModule, plots

# Initialise the logger
log = logging.getLogger(__name__)

class MultiqcModule(BaseMultiqcModule):

    def __init__(self):

        # Initialise the parent object
        super(MultiqcModule, self).__init__(name='FastQ Screen', anchor='fastq_screen', 
        href="http://www.bioinformatics.babraham.ac.uk/projects/fastq_screen/", 
        info="allows you to screen a library of sequences in FastQ format against"\
        " a set of sequence databases so you can see if the composition of the"\
        " library matches with what you expect.")

        # Find and load any FastQ Screen reports
        self.fq_screen_data = dict()
        self.num_orgs = 0
        for f in self.find_log_files(config.sp['fastq_screen'], filehandles=True):
            parsed_data = self.parse_fqscreen(f['f'])
            if parsed_data is not None:
                if f['s_name'] in self.fq_screen_data:
                    log.debug("Duplicate sample name found! Overwriting: {}".format(f['s_name']))
                self.add_data_source(f)
                self.fq_screen_data[f['s_name']] = parsed_data

        if len(self.fq_screen_data) == 0:
            log.debug("Could not find any reports in {}".format(config.analysis_dir))
            raise UserWarning

        log.info("Found {} reports".format(len(self.fq_screen_data)))

        # Section 1 - Alignment Profiles
        # Posh plot only works for around 20 samples, 8 organisms.
        if len(self.fq_screen_data) * self.num_orgs <= 160 and not config.plots_force_flat:
            self.intro += self.fqscreen_plot()
        # Use simpler plot that works with many samples
        else:
            self.intro += self.fqscreen_simple_plot()
        
        # Write the total counts and percentages to files
        self.write_data_file(self.parse_csv(), 'multiqc_fastq_screen')


    def parse_fqscreen(self, fh):
        """ Parse the FastQ Screen output into a 3D dict """
        parsed_data = OrderedDict()
        for l in fh:
            if l.startswith('%Hit_no_libraries:'):
                empty = { 'unmapped': 0, 'multiple_hits_one_library': 0, 'one_hit_multiple_libraries': 0, 'multiple_hits_multiple_libraries': 0 }
                parsed_data['No hits'] = {'percentages': empty, 'counts': empty}
                parsed_data['No hits']['percentages']['one_hit_one_library'] = float(l[19:])
            else:
                fqs = re.search(r"^(\S+)\s+(\d+)\s+(\d+)\s+([\d\.]+)\s+(\d+)\s+([\d\.]+)\s+(\d+)\s+([\d\.]+)\s+(\d+)\s+([\d\.]+)\s+(\d+)\s+([\d\.]+)$", l)
                if fqs:
                    org = fqs.group(1)
                    parsed_data[org] = {'percentages':{}, 'counts':{}}
                    parsed_data[org]['counts']['reads_processed'] = int(fqs.group(2))
                    parsed_data[org]['counts']['unmapped'] = int(fqs.group(3))
                    parsed_data[org]['percentages']['unmapped'] = float(fqs.group(4))
                    parsed_data[org]['counts']['one_hit_one_library'] = int(fqs.group(5))
                    parsed_data[org]['percentages']['one_hit_one_library'] = float(fqs.group(6))
                    parsed_data[org]['counts']['multiple_hits_one_library'] = int(fqs.group(7))
                    parsed_data[org]['percentages']['multiple_hits_one_library'] = float(fqs.group(8))
                    parsed_data[org]['counts']['one_hit_multiple_libraries'] = int(fqs.group(9))
                    parsed_data[org]['percentages']['one_hit_multiple_libraries'] = float(fqs.group(10))
                    parsed_data[org]['counts']['multiple_hits_multiple_libraries'] = int(fqs.group(11))
                    parsed_data[org]['percentages']['multiple_hits_multiple_libraries'] = float(fqs.group(12))
        if len(parsed_data) == 0:
            return None
        
        self.num_orgs = max(len(parsed_data), self.num_orgs)
        return parsed_data
    
    def parse_csv(self):
        totals = OrderedDict()
        for s in sorted(self.fq_screen_data.keys()):
            totals[s] = OrderedDict()
            for org in self.fq_screen_data[s]:
                try:
                    k = "{} counts".format(org)
                    totals[s][k] = self.fq_screen_data[s][org]['counts']['one_hit_one_library']
                    totals[s][k] += self.fq_screen_data[s][org]['counts']['multiple_hits_one_library']
                    totals[s][k] += self.fq_screen_data[s][org]['counts']['one_hit_multiple_libraries']
                    totals[s][k] += self.fq_screen_data[s][org]['counts']['multiple_hits_multiple_libraries']
                except KeyError: pass
                try:
                    k = "{} percentage".format(org)
                    totals[s][k] = self.fq_screen_data[s][org]['percentages']['one_hit_one_library']
                    totals[s][k] += self.fq_screen_data[s][org]['percentages']['multiple_hits_one_library']
                    totals[s][k] += self.fq_screen_data[s][org]['percentages']['one_hit_multiple_libraries']
                    totals[s][k] += self.fq_screen_data[s][org]['percentages']['multiple_hits_multiple_libraries']
                except KeyError: pass
        return totals

    def fqscreen_plot (self):
        """ Makes a fancy custom plot which replicates the plot seen in the main
        FastQ Screen program. Not useful if lots of samples as gets too wide. """
        
        categories = list()
        getCats = True
        data = list()
        p_types = OrderedDict()
        p_types['multiple_hits_multiple_libraries'] = {'col': '#7f0000', 'name': 'Multiple Hits, Multiple Genomes' }
        p_types['one_hit_multiple_libraries'] = {'col': '#ff0000', 'name': 'One Hit, Multiple Genomes' }
        p_types['multiple_hits_one_library'] = {'col': '#00007f', 'name': 'Multiple Hits, One Genome' }
        p_types['one_hit_one_library'] = {'col': '#0000ff', 'name': 'One Hit, One Genome' }
        for k, t in p_types.items():
            first = True
            for s in sorted(self.fq_screen_data.keys()):
                thisdata = list()
                if len(categories) > 0:
                    getCats = False
                for org in self.fq_screen_data[s]:
                    thisdata.append(self.fq_screen_data[s][org]['percentages'][k])
                    if getCats:
                        categories.append(org)
                td = {
                    'name': t['name'],
                    'stack': s,
                    'data': thisdata,
                    'color': t['col']
                }
                if first:
                    first = False
                else:
                    td['linkedTo'] = ':previous'
                data.append(td)

        html = '<div id="fq_screen_plot" class="hc-plot"></div> \n\
        <script type="text/javascript"> \n\
            fq_screen_data = {};\n\
            fq_screen_categories = {};\n\
            $(function () {{ \n\
                $("#fq_screen_plot").highcharts({{ \n\
                    chart: {{ type: "column", backgroundColor: null }}, \n\
                    title: {{ text: "FastQ Screen Results" }}, \n\
                    xAxis: {{ categories: fq_screen_categories }}, \n\
                    yAxis: {{ \n\
                        max: 100, \n\
                        min: 0, \n\
                        title: {{ text: "Percentage Aligned" }} \n\
                    }}, \n\
                    tooltip: {{ \n\
                        formatter: function () {{ \n\
                            return "<b>" + this.series.stackKey.replace("column","") + " - " + this.x + "</b><br/>" + \n\
                                this.series.name + ": " + this.y + "%<br/>" + \n\
                                "Total Alignment: " + this.point.stackTotal + "%"; \n\
                        }}, \n\
                    }}, \n\
                    plotOptions: {{ \n\
                        column: {{ \n\
                            pointPadding: 0, \n\
                            groupPadding: 0.02, \n\
                            stacking: "normal" }} \n\
                    }}, \n\
                    series: fq_screen_data \n\
                }}); \n\
            }}); \n\
        </script>'.format(json.dumps(data), json.dumps(categories))

        return html
    
    
    def fqscreen_simple_plot(self):
        """ Makes a simple bar plot with summed alignment counts for
        each species, stacked. """
        
        # First, sum the different types of alignment counts
        data = OrderedDict()
        cats = list()
        for s_name in self.fq_screen_data:
            data[s_name] = OrderedDict()
            for org in self.fq_screen_data[s_name]:
                if org == 'No hits':
                    continue
                data[s_name][org] = self.fq_screen_data[s_name][org]['percentages']['one_hit_one_library']
                data[s_name][org] += self.fq_screen_data[s_name][org]['percentages']['multiple_hits_one_library']
                data[s_name][org] += self.fq_screen_data[s_name][org]['percentages']['one_hit_multiple_libraries']
                data[s_name][org] += self.fq_screen_data[s_name][org]['percentages']['multiple_hits_multiple_libraries']
                if len(cats) < len(self.fq_screen_data[s_name]):
                    cats.append(org)
        
        pconfig = {
            'title': 'FastQ Screen',
            'cpswitch': False,
            'ylab_format': '{value}%',
            'tt_percentages': False
        }
        
        return ("<p>Summed alignment percentages are shown below. Note that percentages \
                can sum to greater than 100% if reads align to multiple organisms.</p>" +
                plots.bargraph.plot(data, cats, pconfig) )

        
        
