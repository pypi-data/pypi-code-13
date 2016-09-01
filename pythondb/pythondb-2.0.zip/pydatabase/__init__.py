import pickle
from collections import OrderedDict
import operator
import os

class Row():
    def __init__(self,id,dictvalues=None,**values):
        self.id = id
        if dictvalues is None:
            self.items = values
        else:
            self.items = dictvalues

        self.keys = list(self.items.keys())
        self.values = list(self.items.values())

        for key,value in self.items.items():
            setattr(self,key,value)

    def __str__(self):
        return "Row(id={}, {})".format(self.id,", ".join([str(k)+"="+str(v) for k,v in self.items.items()]))

    def __contains__(self,key):
        return key in self.values

    def index(self,index):
        return self.values[index]

    def __getitem__(self,index):
        return self.values[index]

    def rmvar(self,value):
        delattr(self,value)
        del self.items[value]

        self.keys = list(self.items.keys())
        self.values = list(self.items.values())

    def var(self,key,value=None):
        setattr(self,key,value)
        self.items[key] = value

        self.keys = list(self.items.keys())
        self.values = list(self.items.values())

    __repr__ = __str__

class Table():
    def __init__(self,db_ref,table_name):
        self.db_ref = db_ref
        self.table_name = table_name
        self.database = db_ref.database
        self.table_ref = self.database[table_name]

    def kys(self):
        del self

    def __str__(self):
        return "Table([{}])".format(", ".join([str(row) for row in self.table_ref]))

    def __getitem__(self,index):
        return self.table_ref[index]

    def get(self,a,b):
        return self.table_ref[a:b]

    def index(self,index):
        return self.table_ref[index]

    def sort(self,column,order="ASC"):
        order = order.lower()
        sort_values = []

        for row in self.table_ref:
            try:
                sort_values.append((row,row.items[column]))
            except KeyError:
                raise ValueError("Trying to sort by non-existant column.")

        if order == "asc":
            sort_values = sorted(sort_values,key=operator.itemgetter(1))

        elif order == "desc":
            sort_values = sorted(sort_values,key=operator.itemgetter(1),reverse=True)

        return [x[0] for x in sort_values]

    def insert(self,**values):
        self.table_ref.append(Row(int(len(self.table_ref)),**values))
        for key,val in values.items():
            self.db_ref.var(self.table_name,self.table_ref)

    def remove(self,row):
        if isinstance(row,int):
            del self.table_ref[row]
        else:
            self.table_ref.remove(row)

    def remove_column(self,*columns):
        for column in columns:
            for row in self.table_ref:
                row.rmvar(column)

    def new_column(self,*columns,value=None):
        for column in columns:
            for row in self.table_ref:
                row.var(column,value)

    def list_column(self,*columns):
        column_values = []

        for column in columns:
            column_inner_values = []
            for row in self.table_ref:
                column_inner_values.append(row.items[column])
            column_values.append(column_inner_values)

        if len(column_values) == 1:
            return column_values[0]
        return column_values

    def new_row(self,rowobj):
        self.table_ref.append(rowobj)

    def find_one(self,**values):
        for query in values:
            for num,row in enumerate(self.table_ref):
                if query in row.items:
                    if row[query] == values[query]:
                        return self.table_ref[num]

    def find(self,**values):
        results = []
        for query in values:
            for num,row in enumerate(self.table_ref):
                if query in row.items:
                    if row[query] == values[query]:
                        results.append(self.table_ref[num])
        if len(results) == 1:
            return results[0]
        elif len(results) > 1:
            return results

    __repr__ = __str__

class Database():
    def __init__(self,dbname=None):
        self.dbname = dbname

        self.database = OrderedDict()

    def save(self,fname=None):
        if fname is None and self.dbname is not None:
            with open(self.dbname + ".pydb","wb") as f:
                pickle.dump(self,f,pickle.HIGHEST_PROTOCOL)
        elif fname is not None:
            with open(fname + ".pydb","wb") as f:
                pickle.dump(self,f,pickle.HIGHEST_PROTOCOL)
        else:
            raise ValueError("No specified name for DB file.")

    def export(self,fname):
        with open(fname,"w") as f:
            f.write(convert_to_plain(self))

    def var(self,key,value):
        setattr(self,key,value)

    def rmvar(self,value):
        delattr(self,value)

    def __str__(self):
        return "PyDatabase([{}])".format(", ".join([str(Table(self,v)) for v in self.database]))

    def __getitem__(self,index):
        if isinstance(index,int):
            return self.database[list(self.database.keys())[index]]
        else:
            if not index in self.database:
                self.database[index] = []
                setattr(self,index,self.database[index])
            return Table(self,index)

    def table(self,name):
        if not name in self.database:
            self.database[name] = []
            setattr(self,name,self.database[name])
        return Table(self,name)

    def index(self,index):
        if isinstance(index,int):
            return self.database[list(self.database.keys())[index]]
        else:
            if not index in self.database:
                self.database[index] = []
                setattr(self,index,self.database[index])
            return Table(self,name)

    __repr__ = __str__

def convert_to_plain(database):
    database = database.__dict__["database"]
    plain_dict = OrderedDict()
    for table_name in database:
        table_obj = database[table_name]
        plain_dict[table_name] = {}
        for row_obj in table_obj:
            plain_dict[table_name][row_obj.id] = row_obj.__dict__["items"]
    return plain_dict

def convert_to_database(dictionary):
    newdb = PyDatabase()
    for table_name in dictionary:
        table_obj = dictionary[table_name]
        newdb.table(table_name)
        for row in table_obj:
            row_obj = Row(int(row),dictvalues=table_obj[row])
            newdb[table_name].new_row(row_obj)
    return newdb

def PyDatabase(dbname=None):
    if dbname is not None:
        if os.path.isfile(dbname + ".pydb"):
            with open(dbname + ".pydb","rb") as f:
                return pickle.load(f)
        else:
            return Database(dbname)
    else:
        return Database()

if __name__ == "__main__":
    import json

    data = PyDatabase("testing")
    test = data["testing"]

    print(test)

    #test.insert(name="jack",age=12)
    #test.insert(name="jake",age=34)
    #test.insert(name="declan",age=23)
    #test.insert(name="eamonn",age=52)
    #test.insert(name="sean",age=17)

    print(data)

    #data.save()
