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
        return self.items[self.values.keys()[index]]

    def __getitem__(self,index):
        return self.items[index]

    __repr__ = __str__

class Table():
    def __init__(self,db_ref,table_name):
        self.db_ref = db_ref
        self.table_name = table_name
        self.database = db_ref.database
        self.table_ref = self.database[table_name]

    def __str__(self):
        return "Table([{}])".format(", ".join([str(row) for row in self.table_ref]))

    def __getitem__(self,index):
        return self.table_ref[index]

    def index(self,index):
        return self.table_ref[index]

    def sort(self,column,order="ASC"):
        order = order.lower()
        sort_values = []

        for row in self.table_ref:
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
        self.table_ref.append(Row(int(len(self.table_ref)),**values))
        for key,val in values.items():
            self.db_ref.var(self.table_name,self.table_ref)

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
        setattr(self,key,value)

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
            return Table(self,index)

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


if __name__ == "__main__":
    import json

    data = PyDatabase()

    test = data["testing"]

    test.insert(name="HL3",release="NAN")
    test.insert(uid="ds8af83",payload=[1,2,3,4,5,6])

    db = convert_to_plain(data)
    print(json.dumps(db,indent=4))

    db = convert_to_database(db)
    print(db)