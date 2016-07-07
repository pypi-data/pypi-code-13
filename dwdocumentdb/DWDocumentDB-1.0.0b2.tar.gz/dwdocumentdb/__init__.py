from pydocumentdb import document_client

class DWDocumentDB:
	def __init__(self,host, masterkey, dbname=None,collname=None):
		self.client=document_client.DocumentClient(host,{'masterKey':masterkey})
		if dbname!=None and collname!=None:
			self.setDBCollection(dbname,collname)
		if dbname!=None:
			self.setDB(dbname)

	def _getDB(self,dbname):
		try:
			db=next((data for data in self.client.ReadDatabases() if data['id']==dbname))
		except:
			db=self.createDB(dbname)
		return db 

	def _getCollection(self,db, collname):
		try:
			coll=next((data for data in self.client.ReadCollections(db['_self']) if data['id']==collname))
		except:
			coll=self.createCollection(collname)
		return coll 

	def _getDocument(self,coll, docname):
		doc=next((data for data in self.client.ReadDocuments(coll['_self']) if data['id']==docname))
		return doc 

	def setDB(self,dbname):
		self.db=self._getDB(dbname)

	def setCollection(self,collname):
		self.coll=self._getCollection(self.db,collname)

	def setDBCollection(self,dbname,collname):
		self.db=self._getDB(dbname)
		self.coll=self._getCollection(self.db, collname)

	def createDB(self, dbname):
		# Attempt to delete the database.  This allows this to be used to recreate as well as create
		try:
			db = next((data for data in self.client.ReadDatabases() if data['id'] == dbname))
			self.client.DeleteDatabase(db['_self'])
		except:
			pass
		# Create database
		db = client.CreateDatabase({ 'id': dbname })
		return db

	def createCollection(self,collname,offerType='S1'):
		coll = self.client.CreateCollection(self.db['_self'],{ 'id': collname }, { 'offerType': offerType })
		return coll

	def deleteCollection(self,collname=None):
		if collname!=None:
			self.setCollection(collname)
		self.client.DeleteCollection(self.coll['_self'])

	def deleteDatabase(self,dbname=None):
		if dbname!=None:
			self.setDB(dbname)
		self.client.DeleteDatabase(db['_self'])

	def deleteDocument(self,docname):
		try:
			doc=self._getDocument(self.collname,docname)
			self.client.DeleteDocument(doc['_self'])
		except:
			print 'Error. Have you set database and collection? Check your document name.'
			
	def readDocument(self,docname, key=None):
		try:
			coll=self.coll
		except:
			print "No collection has been set. Please call setDBCollection."
			return
		doc=self._getDocument(coll, docname)
		if key==None:
			return doc
		if '/' in key:
			keys=key.split('/')
			data=doc
			for eachkey in keys:
				data=data[eachkey]
			return data
		return doc[key]

	def replaceDocument(self,docname, data, key=None):
		try:
			coll=self.coll
		except:
			print "No collection has been set. Please call setDBCollection."
			return
		olddoc=self._getDocument(coll, docname)
		uri=olddoc['_self']
		if key==None:
			newdoc=self.client.ReplaceDocument(uri,data)
			return newdoc
		if '/' in key:
			keys=key.split('/')
			ndict=olddoc
			for eachkey in keys[:-1]:
				ndict=ndict[eachkey]
			ndict[keys[-1]]=data 
			newdoc=self.client.ReplaceDocument(uri,olddoc)
			return newdoc
		olddoc[key]=data
		newdoc=self.client.ReplaceDocument(uri,olddoc)
		return newdoc