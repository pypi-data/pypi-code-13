#! python3

import sys
from plotit.basic import basic_plot


def print_basic_plot(days, starting_date, avg, sdev):
    """Script to test basic plot
    
    This script will print out a basic chart to test the matplotlib
    functionality
    
    Arguments:
    ndays (integer) ---  Number of days to print
    date1 (str)     ---  Starting date, format is dd/mm/yyyy
    mu    (float)   ---  Distribution average
    sigma (float)   ---  Distribution sigma
    
    Output:
    Chart in the screen, no returned value
    
    Examples:
    > py -3 print_basic_plot.py 100 03/05/2054 0 5 
       
    > py -3 board_xml_list.py --help
    This help
    """
    basic_plot(ndays = days, date1 = starting_date, mu = avg, sigma = sdev)
            

if __name__=="__main__":
    if len(sys.argv)== 1:
        print('Error. No arguments')
        print('Use -H or --help to get help')
        sys.exit(2)
    if len(sys.argv)== 2:
        if sys.argv[1]=='-H' or sys.argv[1]=='--help':
            print(print_basic_plot.__doc__)
            sys.exit(0)
        else:
            print('Error. No valid argument ' + sys.argv[1]) 
            print('Use -H or --help to get help')
            sys.exit(2)
    if len(sys.argv)!= 5:
        print('Error. print_basic_plot.py script needs only 1 or 4 arguments')
        print(str(sys.argv) + ' arguments passed')
        print('Use -H or --help to get help')
        sys.exit(2)
    print('ndays=' + sys.argv[1])
    print('date=' + sys.argv[2])
    print('mu=' + sys.argv[3])
    print('sigma=' + sys.argv[4])      
    print_basic_plot(int(sys.argv[1]), sys.argv[2], 
                     float(sys.argv[3]), float(sys.argv[4]))
    sys.exit(0)
