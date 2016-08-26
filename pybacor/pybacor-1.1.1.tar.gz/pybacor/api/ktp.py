import requests as req
from . import config 


class IbacorKTP(object):

	status = False
	message = 'Data Tidak Tersedia'

	nik = None
	nama = None
	kelamin = None
	kelurahan = None
	kecamatan = None
	kota = None
	provinsi = None

	def __init__(self, nik):
		self.nik = nik
		self.__r = None
		self.__url = config.BASE_URL+config.ENDPOINT_PARAM_KTP

		self.__init_request()
		self.__set_all()

	def set_nik(self, nik):
		self.nik = nik

	def get_nik(self):
		return self.nik

	def get_data(self):
		return self.__r.json()

	def __init_request(self):
		self.__r = req.get(self.__url.format(self.nik))

	def __set_all(self):
		try:
			dictionary = self.__r.json()
			if dictionary['pesan'].upper() == 'DATA ADA':
				self.message = 'Data Tersedia'
				self.status = True

				self.nik = dictionary['data']['nik']
				self.nama = dictionary['data']['nama']
				self.kelamin = dictionary['data']['kelamin']
				self.kelurahan = dictionary['data']['kelurahan']
				self.kecamatan = dictionary['data']['kecamatan']
				self.kota = dictionary['data']['kabupaten_kota']
				self.provinsi = dictionary['data']['provinsi']
		except:
			self.status = False
			self.message = 'Data Tidak Tersedia'

			self.nik = None
			self.nama = None
			self.kelamin = None
			self.kelurahan = None
			self.kecamatan = None
			self.kota = None
			self.provinsi = None

	def get_object(self):
		return self.__r