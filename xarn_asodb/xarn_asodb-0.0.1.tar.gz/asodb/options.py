from collections import namedtuple

OptionsT = namedtuple('Options', 
                     'select ignore depth expand rooted where unless distinct path key sortby limit offset count inc to')


class Options:
    
    def __init__(self, args={}):
        self.select = ''
        self.ignore = ''
        self.depth = 0
        
        self.expand = False # can be true/false, a number or a string (path1,path2,...)
        self.rooted = False
        
        self.where = ''
        self.unless = ''
        self.distinct = False
        
        self.path = False
        self.key = False
        
        self.sortby = ''
        self.limit = 100
        self.offset = 0
        
        self.count = False
        self.inc = 0
        self.to = ''
        
        for (k,v) in args.items():
            if k in ['depth','limit','offset','inc']:
                v = int(v)
            elif k in ['expand','rooted','distinct','path','key','count']:
                v = bool(v)
            self.__dict__[k] = v
    
    def __str__(self):
        return str(self.__dict__)
        
    def validate(self):
        opt = self

        # select, ignore and depth are exclusive
        if opt.select and opt.ignore:
            raise Exception("The 'select', 'ignore' and 'depth' parameters are exclusive. Use either one, but not both at the same time.")

        if opt.count and opt.limit:
            raise Exception("What are you doing?! The 'limit' parameter doesn't make sense in a 'count=true' request.")
        if opt.count and opt.offset:
            raise Exception("What are you doing?! The 'offset' parameter doesn't make sense in a 'count=true' request.")
        if opt.count and opt.sortby:
            raise Exception("What are you doing?! The 'sortby' parameter doesn't make sense in a 'count=true' request.")
        if opt.count and opt.depth and not opt.distinct:
            raise Exception("What are you doing?! The 'select' parameter doesn't make sense in a 'count=true' request.")
        if opt.count and opt.select and not opt.distinct:
            raise Exception("What are you doing?! The 'select' parameter doesn't make sense in a 'count=true' request.")
        if opt.count and opt.ignore and not opt.distinct:
            raise Exception("What are you doing?! The 'ignore' parameter doesn't make sense in a 'count=true' request.")

