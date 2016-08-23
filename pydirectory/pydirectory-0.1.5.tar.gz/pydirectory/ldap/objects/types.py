from pydirectory.directory.objects import types
from ldap3 import MODIFY_DELETE,MODIFY_REPLACE

class object(types.object):
	def _delete(self):
		if self.dn.value == None:
			return None
		try:
			return self._objects._engine._worker.delete(self.dn.value)
		except self._exceptions.LDAPNoSuchObjectResult:
			return False

	def _save(self):
		self.container._is_modified = False
		if self.dn.value != None:
			modlist = {}
			for key,attr in self._attrs.items():
				if attr._is_modified and (not attr._is_rdn):
					operator = MODIFY_REPLACE
					modlist[key]= [(operator,attr.raw)]
					attr._is_modified = False
			for key in self._drops:
				operator = MODIFY_DELETE
				modlist[key] = [(operator,[])]
			self._drops = []
			if len(modlist) > 0:
				self._objects._engine._worker.modify(self.dn.value,modlist)

			if self.cn._is_modified:
				self._objects._engine._worker.modify_dn(self.dn.value,'CN='+self.cn.value)
				self.dn.update('CN='+self.cn.value+','+','.join(self.dn.value.split(',')[1:]))
				self.cn._is_modified = False

			if self.container._is_modified: #falta por terminar
				self._objects._engine._worker.modify_dn(self.dn.value,'CN='+self.cn.value,new_superior=self.container.value)
				self.dn.update('CN='+self.cn.value+','+self.container.value)
				self.container._is_modified = False
		else:
			attributes = {}
			self.dn.update('CN='+self.cn.value+','+self.container.value)
			for key,attr in self._attrs.items():
				if (key != "dn") and (key != "container"):
					attributes[key]= attr.value
					attr._is_modified = False
			if len(attributes) > 0:
				try:
					self._objects._engine._worker.add(self.dn.value,attributes=attributes)
				except self._exceptions.PyAsn1Error:
					raise self._exceptions.CheckValueAttributes


	def _reset(self):
		if self.dn.value != None:
			obj = self._objects.get(dn=self.dn.value,scope='BASE')
			self._attrs = obj._attrs
		else:
			raise self._exceptions.DNisNone
