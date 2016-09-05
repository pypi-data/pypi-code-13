import json

class Jsonipy(object):
    """ Serializes a given object """
    
    def __init__(self, model_instance=None):
        self.data=''
        self.model_instance=model_instance
        self._validate(self.model_instance)
        
    def _validate(self,obj):
        ''' validates the metaclass and fields '''
        assert hasattr(self,'Meta'), "No meta class found,please refer to the documentation"
        assert hasattr(self.Meta,'model') , "have you specified 'model' in meta class"
        assert hasattr(self.Meta,'fields'), "have you specified 'fields' in meta class"
        
        if self.model_instance :
             assert isinstance(self.model_instance,self.Meta.model), "Invalid object"
             self._serialize()
        
    
    def _serialize(self):
        """ serializes the data into json format """
        
        data_dict={}
        if self.Meta.fields == '__all__':                       
            data_dict = self._get_all_fields()
        else:
            for field in self.Meta.fields:
                data_dict[field] = getattr(self.model_instance,field)
        
        serialized_data = json.dumps(data_dict)                 #serialize data into json file
        self.data=serialized_data                               
        
    
    def _get_all_fields(self):
        ''' gets all the fields of the passed object '''

        fields = vars(self.model_instance) 
        return fields

    def _validate_all_fields(self):
        raise NotImplementedError()
