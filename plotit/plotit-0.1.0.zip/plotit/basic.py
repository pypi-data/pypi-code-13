'''
Created on 10 sept. 2016

@author: Sergio
'''
'''
Created on 10 sept. 2016

@author: Sergio
'''
from matplotlib.dates import  MONDAY, DayLocator, date2num, \
        DateFormatter, WeekdayLocator, MonthLocator, YearLocator
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from math import exp

def calc_x_scale(date_list, ax):
        if np.any(date_list):
            if date_list.size < 30: 
                axis_locator = DayLocator()
                axis_formatter = DateFormatter('%b %d %Y')
            elif date_list.size < 210:
                    axis_locator = WeekdayLocator(MONDAY)
                    axis_formatter = DateFormatter('%b %d %Y') 
            elif date_list.size < 900:
                axis_locator =  MonthLocator(bymonth = range(1, 13),
                                             bymonthday = 1, interval = 1)
                axis_formatter = DateFormatter('%b %y') 
            else:
                axis_locator = YearLocator()
                axis_formatter = DateFormatter('%Y')
            ax.xaxis.set_major_locator(axis_locator)
            ax.xaxis.set_major_formatter(axis_formatter)

def basic_plot(ndays, date1, mu ,sigma):
    
    Date1 = (datetime.strptime(date1, "%d/%m/%Y"))
    date_list= date2num([Date1-timedelta(days = -x) 
                         for x in range(0, ndays) ])
    print(date_list)
    data1 = mu + sigma * np.random.randn(ndays)
    data2 = mu + sigma * np.random.randn(ndays)
    diff = (data2 - data1)
    data3 = np.asarray([5 * exp(0.1 * x) for x in diff])
    
    data_name = 'random values'
    x_name = 'days'
    trace_type = 'ro-'
    title_plot = 'Evolution'
    log_y = True
     
    fig, ax = plt.subplots(1, 1, figsize=(8, 6), dpi = 80 )  # @UnusedVariable
    ax.plot_date(date_list, data3, trace_type, label = data_name)
    plt.subplots_adjust(bottom = 0.1, hspace = 0.4)
    ax.set_ylabel(data_name)
    ax.set_xlabel(x_name)
    ax.legend(loc = 'best', frameon = False)
    ax.set_title(title_plot)
    ax.grid(True, which = "both", ls = "-", color = '0.65')
    if log_y:
        ax.set_yscale('log')
    calc_x_scale(date_list, ax)
    ax.autoscale_view()
    plt.setp(ax.get_xticklabels(), rotation = 45, horizontalalignment = 'right')
    ax.tick_params(axis = 'x', labelsize = 8)
    
    plt.show()

