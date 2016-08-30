import pickle
from collections import OrderedDict
import operator

def save_dict(obj,fname):
    with open(fname + ".pydb","wb") as f:
        pickle.dump(obj,f,pickle.HIGHEST_PROTOCOL)

def load_dict(fname):
    with open(fname + ".pydb","rb") as f:
        return pickle.load(f)

class Row():
    def __init__(self,id,dictvalues=None,**values):
        self.id = id
        if dictvalues is None:
            self.values = values
        else:
            self.values = dictvalues

        self.keys = list(values.keys())
        self.vals = list(values.values())

        for key,value in values.items():
            if isinstance(value,str):
                exec("self.{} = \"{}\"".format(key,value))
            elif isinstance(value,int):
                exec("self.{} = int({})".format(key,value))
            elif isinstance(value,list):
                exec("self.{} = list({})".format(key,value))
            elif isinstance(value,dict):
                exec("self.{} = dict({})".format(key,value))
            else:
                exec("self.{} = {}".format(key,value))

    def __str__(self):
        return "Row(id={}, {})".format(self.id,", ".join([str(k)+"=\""+str(v)+"\"" for k,v in self.values.items()]))

    def __contains__(self,key):
        return key in self.vals

    def index(self,index):
        return self.values[self.values.keys()[index]]

    def __getitem__(self,index):
        return self.values[index]

    __repr__ = __str__

class Table():
    def __init__(self,dbobj,table):
        self.dbobj = dbobj
        self.tablename = table
        self.database = dbobj.database
        self.table = self.database[table]

    def __str__(self):
        return "Table([{}])".format(", ".join([str(row) for row in self.table]))

    def __getitem__(self,index):
        return self.table[index]

    def index(self,index):
        return self.table[index]

    def sort(self,column,order="ASC"):
        order = order.lower()
        sort_values = []

        for row in self.table:
            try:
                sort_values.append((row,row.values[column]))
            except KeyError:
                raise ValueError("Trying to sort by non-existant column.")

        if order == "asc":
            sort_values = sorted(sort_values,key=operator.itemgetter(1))

        elif order == "desc":
            sort_values = sorted(sort_values,key=operator.itemgetter(1),reverse=True)

        return [x[0] for x in sort_values]

    def insert(self,**values):
        self.table.append(Row(int(len(self.table)),**values))
        for key,val in values.items():
            self.dbobj.var(self.tablename,self.table)

    def new_row(self,rowobj):
        self.table.append(rowobj)
        #for key,val in values.items():
         #   self.dbobj.var(self.tablename,self.table)

    def find_one(self,**values):
        for query in values:
            for num,row in enumerate(self.table):
                if query in row.values:
                    if row[query] == values[query]:
                        return self.table[num]

    def find(self,**values):
        results = []
        for query in values:
            for num,row in enumerate(self.table):
                if query in row.values:
                    if row[query] == values[query]:
                        results.append(self.table[num])
        if len(results) == 1:
            return results[0]
        elif len(results) > 1:
            return results

class PyDatabase():
    def __init__(self,fname=None):
        if fname is not None:
            try:
                self.database = OrderedDict(load_dict(fname))
            except:
                self.database = OrderedDict()
        else:
            self.database = OrderedDict()

    def var(self,key,value):
        if isinstance(value,str):
            exec("self.{} = \"{}\"".format(key,value))
        elif isinstance(value,int):
            exec("self.{} = int({})".format(key,value))
        elif isinstance(value,list):
            exec("self.{} = list({})".format(key,value))
        elif isinstance(value,dict):
            exec("self.{} = dict({})".format(key,value))
        else:
            exec("self.{} = {}".format(key,value))

    def __str__(self):
        return "PyDatabase({})".format(", ".join(["["+str(num)+"]=\""+v+"\"" for num,v in enumerate(self.database.keys())]))

    def __getitem__(self,index):
        if isinstance(index,int):
            return self.database[list(self.database.keys())[index]]
        else:
            if not index in self.database:
                self.database[index] = []
                exec("self.{} = '{}'".format(index,self.database[index]))
            return Table(self,index)

    def table(self,name):
        if not index in self.database:
            self.database[index] = []
            exec("self.{} = '{}'".format(index,self.database[index]))
        return Table(self,index)

    def index(self,index):
        if isinstance(index,int):
            return self.database[list(self.database.keys())[index]]
        else:
            if not index in self.database:
                self.database[index] = []
                exec("self.{} = '{}'".format(index,self.database[index]))
            return Table(self,index)

    __repr__ = __str__

def convert_to_plain(database):
    database = database.__dict__["database"]
    plain_dict = OrderedDict()
    for table_name in database:
        table_obj = database[table_name]
        plain_dict[table_name] = {}
        for row_obj in table_obj:
            plain_dict[table_name][row_obj.id] = row_obj.__dict__["values"]
    return plain_dict

def convert_to_database(dictionary):
    newdb = PyDatabase()
    for table_name in database_plain:
        table_obj = database_plain[table_name]
        newdb.table(table_name)
        for row in table_obj:
            row_obj = Row(int(row),dictvalues=table_obj[row])
            newdb[table_name].new_row(row_obj)
    return newdb


if __name__ == "__main__":
    data = PyDatabase()

    people = data["people"]

    people.insert(name="Jack", age=18, sex="Male")
    people.insert(name="Declan", age=34, sex="Male")
    people.insert(name="Hannah", age=21, sex="Female")
    people.insert(name="Derek", age=18, sex="Male")
    people.insert(name="Emma", age=12, sex="Female")

    print(people.find_one(age=18))