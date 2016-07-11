#!/usr/bin/env python3
def split_read(file):
    ''' read file with split mark ':' '''
    data=open(file)
    for each_line in data:
        try:
            [role,line_speak]=each_line.split(':',1)
            print(role,end='')
            print(' said - ',end='')
            print(line_speak,end='')
        except ValueError:
            print(each_line)
    data.close()
#direc=r'D:\Documents\aPython\read_file\file.txt'
#split_read(direc)
