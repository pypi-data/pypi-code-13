from sqlent import Query

class _BaseModel(object):
    pk = 'id'

    def __init__(self, d=None):
        if d is not None:
            self.set_from_dict(d)

    def set_from_dict(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
               setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
            else:
               setattr(self, a, obj(b) if isinstance(b, dict) else b)

    def outboundHasOne(self, ForeignModelClass, foreign_col_name, this_fk_col_name):
        """
        This function is designed to get one instance of a related object such
        that this object contains a column linking it to the forign object.
        Example:- This could be used to get the Artist for an Album from the Album
        object in the Chinook database.
        FoereignModelClass: The class instances should be returned (eg: Artist)
        foreign_col_name: The column name in the foreign table to match this against
        this_fk_col_name: The column name in this table whose value links this
        object with the object in the foreign table
        """
        sql_statement = "SELECT * FROM {foreign_table_name} where {foreign_col_name} = {this_fk_val};".format(
            foreign_table_name = ForeignModelClass.table_name,
            foreign_col_name = foreign_col_name,
            this_fk_val = getattr(self, this_fk_col_name))
        results = self.__class__.get_sql_results(sql_statement)
        return ForeignModelClass(results[0])

    def inboundHasMany(self, ForeignModelClass, foreign_col_name_to_search, this_col_name_that_contains_search_value):
        query = Query().select().table(ForeignModelClass.table_name).where(foreign_col_name_to_search, getattr(self, this_col_name_that_contains_search_value)).to_string()
        results = self.__class__.get_sql_results(query)
        return [ForeignModelClass(r) for r in results]

    @classmethod
    def all(cls):
        results = cls.get_sql_results(Query().select().table(cls.table_name).to_string())
        return [cls(r) for r in results]

    @classmethod
    def sqlent_query(cls):
        class ReturnableQuery(Query):
            def execute(self):
                return cls.raw_sql(self.to_string())
        return ReturnableQuery().table(cls.table_name)

    @classmethod
    def raw_sql(cls, sql):
        results = cls.get_sql_results(sql)
        return [cls(r) for r in results]
