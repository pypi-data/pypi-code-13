
import unittest, sys, json, collections, base64
sys.path.append('../')

from msm_transcoder import Transcoder

class TestStringMethods(unittest.TestCase):

  def setUp(self):
      self.data = dict(
          authType = 0,
          lastBackupTime = 1461125781055,
          isNew = True,
          isValid = True,
          maxInactive = 7200,
          principalData = dict(
              logined = True,
              verified = True,
              user = '55c064cbe4b002ab055d7fd3',
              agreedTerms = True
          ),
          creationTime = 1461125781055,
          principalDataLength = 0,
          version = 2,
          savedPrincipalDataLength = 0,
          savedRequestDataLength = 0,
          idLength = 32,
          thisAccessedTime = 1461125781055,
          sessionFieldsDataLength = 84,
          id = 'a3065b6606ae11e682397831c1c31f4a',
          lastAccessedTime = 1461125781055
      )
      self.transcoder = Transcoder()

  def __assertItemsEqual(self, v1, v2, msg):
      if self.__isNewVersion():
          self.assertCountEqual(v1, v2, msg)
      else:
          self.assertItemsEqual(v1, v2, msg)


  def __assertDictEqual(self, d1, d2, msg=None):
      if self.__isNewVersion():
          items = d1.items()
      else:
          items = d1.iteritems()

      for k,v1 in items:
          self.assertIn(k, d2, msg)
          v2 = d2[k]
          if(isinstance(v1, collections.Iterable)):
              self.__assertItemsEqual(v1, v2, msg)
          else:
              self.assertEqual(v1, v2, msg)
      return True

  def __isNewVersion(self): return sys.version_info[0] > 2

  def __getEncodingBData(self, encoding_data):
      text = ''.join( map( chr, encoding_data ) )
      if self.__isNewVersion():
          return text.encode('iso-8859-1')
      else:
          return text

  def __getDecodingBuffer(self, decoding_data):
      if self.__isNewVersion():
          text = decoding_data.decode('iso-8859-1')
      else:
          text = decoding_data
      return map( ord, text )

  def test_transcoder(self):
      data = self.data
      binary = self.transcoder.serialize(data)
      decode_data = self.transcoder.deserialize(binary)
      self.__assertDictEqual(data, decode_data)

  def test_base64(self):
      data = self.data
      encoding_data = self.transcoder.serialize( data )
      encoding_base64_data = base64.b64encode( self.__getEncodingBData(encoding_data) )
      decoding_base64_data = self.__getDecodingBuffer( base64.b64decode(encoding_base64_data) )
      result = self.transcoder.deserialize( list(decoding_base64_data) )
      self.__assertDictEqual( data, result )


if __name__ == '__main__':
    unittest.main()

