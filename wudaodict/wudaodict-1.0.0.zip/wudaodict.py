def trans():
	print('欢迎使用无道词典')
	print('------------------------------------------------')
	import urllib.request
	import urllib.parse
	import json
	import time
	while True:
		cccc=input('请输入要翻译内容：\n')
		if cccc=='exit':
			break

		url=('http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=fanyi.logo')

		"""head={}
		head['User-Agent']='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'"""

		data={}
		data['type']='AUTO'
		data['i']=cccc
		data['doctype']='json'
		data['xmlVersion']=['1.8']
		data['keyfrom']='fanyi.web'
		data['ue']='UTF-8'
		data['action']='FY_BY_CLICKBUTTON'
		data['typoResult']='true'
		data=urllib.parse.urlencode(data).encode('UTF-8')



		req=urllib.request.Request(url,data)
		req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36')

		response=urllib.request.urlopen(req)

		abc=response.read().decode('UTF-8')
		yw=json.loads(abc)

		print('译文：\n%s' % (yw['translateResult'][0][0]['tgt']))
		print('------------------------------------------------')
		time.sleep(3)



