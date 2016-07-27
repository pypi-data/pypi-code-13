from cantools import db

class Product(db.ModelBase):
	name = db.String()
	description = db.Text()
	image = db.Binary()
	price = db.Float()