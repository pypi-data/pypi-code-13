from __future__ import unicode_literals
from builtins import *
from iBizProduct.Contracts.CaseSpec import CaseSpec

class iBizCase(CaseSpec):
    def __init__(self):
        self._spec = dict(auto_close = 'YES', priority = 'HIGH', status = 'NEW')

    def getSpec(self):
        return self._spec

    Spec = property(getSpec)

    def getAutoClose(self):
        return self._spec.get('auto_close')

    def setAutoClose(self,autoClose):
        self._spec['auto_close'] = autoClose

    AutoClose = property(getAutoClose, setAutoClose)

    def getDescription(self):
        return self._spec.get('description')

    def setDescription(self,description):
        self._spec['description'] = description

    Description = property(getDescription, setDescription)

    def getDetail(self):
        return self._spec.get('detail')   

    def setDetail(self,detail):
        self._spec['detail'] = detail

    Detail = property(getDetail, setDetail)

    def getInternalNotes(self):
        self._spec.get('internal_notes')
        
    def setInternalNotes(self,internal_notes):
        self._spec['internal_notes'] = internal_notes

    InternalNotes = property(getInternalNotes, setInternalNotes)

    def getIsResolved(self):
        self._spec.get('is_resolved')
        
    def setIsResolved(self,is_resolved):
        self._spec['is_resolved'] = is_resolved

    IsResolved = property(getIsResolved, setIsResolved)

    def getPriority(self):
        self._spec.get('priority')
        
    def setPriority(self,priority):
        self._spec['priority'] = priority

    Priority = property(getPriority, setPriority)

    def getReturnHours(self):
        self._spec.get('return_hours')
        
    def setReturnHours(self,return_hours):
        self._spec['return_hours'] = return_hours

    ReturnHours = property(getReturnHours, setReturnHours)

    def getStatus(self):
        self._spec.get('status')
        
    def setStatus(self, status):
        self._spec['status'] = status

    Status = property(getStatus, setStatus)

    def getType(self):
        self._spec.get('type')
        
    def setType(self,type):
        self._spec['type'] = type

    Type = property(getType, setType)
