import unittest
from serializers import Jsonipy
class MockClass():
    name=''
    age=''
    def __init__(self,**kwargs):
        self.name=kwargs.get('name','')
        self.age=kwargs.get('age',0)

class MockSerializer(Jsonipy):
    class Meta:
        model=MockClass
        fields='__all__'

class MockSerializerExtra(Jsonipy):
    class Meta:
        model=MockClass
        fields=['name']


class JsonipyTest(unittest.TestCase):
    """ Tests Jsonipy class  """
    def test_gives_json(self):
        mock_obj=MockClass(name='tester',age='34')              #create a mock object
        serializer=MockSerializer(mock_obj)                     #mock serializer with fields set to all
        serializer2=MockSerializerExtra(mock_obj)               #mock serializer with fields set to 'name' only

        self.assertEqual(serializer.data,'{"age": "34", "name": "tester"}')
        self.assertEqual(serializer2.data,'{"name": "tester"}')


        mock_obj=MockClass(age='34')
        serializer=MockSerializer(mock_obj)

        self.assertEqual(serializer.data,'{"age": "34", "name": ""}')


if __name__=='__main__':
    unittest.main()