class Person():
    '''
    Example found Person()
    
    >>>from cuil import Person
    >>>c = Person(31449202, Cuil.MALE)
    >>>c.cuil()
    20-31449202-2
    >>>c.url_dateas()
    '''
    MALE = 20
    FAMALE = 27
    BUSSINES = 33
    VALID_OPTIONS = [MALE,FAMALE,BUSSINES]
    
    def __init__(self, dni, genre):
        self.dni = dni
        self.genre = genre
        
    def cuil(self):
        xy= self.genre        
        Z = 0
        n = 5
        adding = 0
        if self.genre in Person.VALID_OPTIONS:
            for d in (str(self.genre) + str(self.dni)):
                adding += (int(d) * n)
                n-=1
                if n<=1:
                    n = 7 
            resto = adding - (adding/11)*11
            if resto > 1:
                z = 11 - resto
            elif resto ==1 and self.genre == Person.MALE:
                xy = 23
                z = 9
            elif resto ==1 and self.genre == Person.FAMALE:
                xy = 23
                z = 4
            return xy,self.dni,z    
        return None

dni = input()
tipo = input()
    
print "{}".format(Person(dni,tipo).cuil())