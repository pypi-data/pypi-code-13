
import anvil.server

class Table:
	def __init__(self, id):
		self.id = id

	def search(self, _chunk_size=None, **kwargs):
		return anvil.server.call("anvil.private.tables.search", self.id, _chunk_size, **kwargs)

	def add_row(self, **kwargs):
		return anvil.server.call("anvil.private.tables.add_row", self.id, **kwargs)

	def list_columns(self):
		return anvil.server.call("anvil.private.tables.list_columns", self.id)

class AppTables:
	def __getattr__(self, name):
		id = anvil.server.call("anvil.private.tables.get_table_id", name)
		if id is None:
			raise AttributeError("No such app table: '%s'" % name)
		return Table(id)

	def __setattr__(self, name, val):
		raise Exception("app_tables is read-only")

app_tables = AppTables()

def set_client_config(x):
    pass
