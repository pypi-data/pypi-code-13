# from pypershelf import get_base_model
# import sqlite3, unittest
# from test import db_path
# from test.helpers import get_sql_results, dict_factory
#
#
#
# conn = sqlite3.connect(db_path)
# conn.row_factory = dict_factory
# BaseModel = get_base_model(conn)
# class Artist(BaseModel):
#     table_name = "Artist"
#     pk = "ArtistId"
#
# print(Artist.all())
# # self.assertEqual(len(Artist.all()), 275)


from sqlent import Query
def f():
    return Query().table('water').select().to_string()
