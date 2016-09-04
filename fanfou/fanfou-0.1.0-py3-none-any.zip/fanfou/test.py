# -*- coding: utf-8 -*-
import fanfou

# print fanfou.APIs_all and browse https://github.com/FanfouAPI/FanFouAPIDoc/wiki/Apicategory

consumer = {'key': 'bfb0a8d5d9fa9d305bdfe059ddc74def',
            'secret': 'e768dbd94ab93c990cf45a00712e7044'}
client = fanfou.XAuth(consumer, 'apps.test', 'Lisp125036')  # enter your username and password, print fanfou.usage to learn more
fanfou.bound(client)  # if you like such client.statuses.update(...) than client.request('/statuses/update', ...)

client.request('/statuses/update', 'POST', {'status': 'test 1'})
client.statuses.update({'status': 'test 2'})
client.request('/photos/upload', 'POST', *fanfou.pack_image('test.jpg', 'test photo 1'))
client.photos.upload(*fanfou.pack_image('test.jpg', 'test photo 2'))
