from distutils.core import setup
import os

setup (
	name = "gituser",
	version = "0.01",
	author = "chenminhua",
	author_email = "chenmh@shanghaitech.edu.cn",
	license = "MIT",
	description = "GET github-user's info and their repos' infos",
	url = "http://github.com/chenminhua/gituser",
	packages = [
		'gituser'
	],
	scripts = ['bin/gituser'],
	install_requires = [
		'prettytable >= 0.7.2'
	]
)
