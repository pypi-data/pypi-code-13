id_ok       = 0 #
id_require  = 1 # {0} is required
id_intRange = 2 # {0}={1} should be integer in range {2}-{3}
id_intMin   = 3 # {0}={1} should be integer >= {2}
id_intMax   = 4 # {0}={1} should be integer <= {2}
id_int      = 5 # {0}={1} should be integer
id_valFail  = 6 # {0}={1} should be one of {2}


import string
texts = {}

def format(code,*args,**kwargs):
    return string.Formatter().vformat( texts.get(code,'') , args , kwargs )

def getFormat(code):
    return texts.get(code,'')

def add(code,text):
    if code in texts:
        raise Exception("Already added : {0} | {1}".format(code,text))
    texts[code] = text

def addCodes():
    #Messages_Begin - This block is auto generated
    add(id_ok               ,"")
    add(id_require          ,"{0} is required")
    add(id_intRange         ,"{0}={1} should be integer in range {2}-{3}")
    add(id_intMin           ,"{0}={1} should be integer >= {2}")
    add(id_intMax           ,"{0}={1} should be integer <= {2}")
    add(id_int              ,"{0}={1} should be integer")
    add(id_valFail          ,"{0}={1} should be one of {2}")
    #Messages_End
    pass

addCodes()
if __name__ == '__main__':
    def update():
        import re
        import codecs
        def read():
            with codecs.open(__file__,'r') as ff:
                return ff.read()
        def write(ss):
            with codecs.open(__file__,'w') as ff:
                ff.write( ss)
        sep1   = 'Messages_'+'Begin'
        sep2   = 'Messages_'+'End'
        indent = '    '
        text   = ''
        source = read()
        for code in re.findall('\s*(id_\w+)\s*=\s*(\d+)\s*#(.*)', source):
            text += '{0}add({1:<20},"{2}")\n'.format(indent,code[0],code[2].replace('"','\"').strip())
        text = '{0}#{1} - This block is auto generated\n'.format(indent,sep1) + text + '{0}#{1}'.format(indent,sep2)
        write( re.sub('[ ]*#{0}((.|\n)*?){1}'.format(sep1,sep2), text,source,flags=re.MULTILINE) )
    update()
