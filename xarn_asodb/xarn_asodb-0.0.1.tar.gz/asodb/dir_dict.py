import os
import os.path
import pysos


class DirDict(dict):
	def __init__(self, path):
		self.path = path
		os.makedirs(path, exist_ok=True)
		
		self._collections = {}
		for filename in os.listdir(path):
			print(filename)
			self._collections[filename] = pysos.load( self.fp(filename) )
			print(len( self._collections[filename] ))
			
	def fp(self, key):
		return os.path.join(self.path, key)
		
	def __getitem__(self, key):
		return self._collections[key]
	
	def __contains__(self, key):
		return (key in self._collections)
    
	def __setitem__(self, key, value):
		if not (isinstance(value, list) or isinstance(value, dict)):
			print(value)
			raise Exception('Only list or dict collections are allowed at the root level.')
		
		# delete it
		if key in self._collections:
			del self[key]
		
		# make a new one from scratch
		if isinstance(value, list):
			coll = pysos.List( self.fp(key) )
			for v in value:
				coll.append(v)
		else:
			coll = pysos.Dict( self.fp(key) )
			for k,v in value.items():
				coll[k] = v
		
		self._collections[key] = coll
			
	def __delitem__(self, key):
		coll = self._collections[key]
		coll.close()
		os.remove( self.fp(key) )
		del self._collections[key]
		
	def items(self):
		return self._collections.items()
		
	def keys(self):
		return self._collections.keys()
		
	def values(self):
		return self._collections.values()
		
	def clear(self):
		for k in self.keys():
			del self[k]
	
	def __iter__(self):
		return self.keys()
	