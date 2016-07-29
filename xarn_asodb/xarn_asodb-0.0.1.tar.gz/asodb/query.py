import asodb
from options import Options
import os

changelog = open('changelog', 'a')

def executePlain(query, data_str):
	
	tokens = query.split('\t')
	cmd = tokens[0].lower()
	path = tokens[1]
	args = {}
	for t in tokens[2:]:
		(key, value) = t.split('=', 1)
		args[key] = value
	return execute(cmd, path, args, data_str)

def executeHttp(method, path, args, data_str):
	cmd = None
	if method == 'GET':
		if 'count' in args and bool(args['count']):
			cmd = 'count'
		elif '*' in path:
			cmd = 'find'
		else:
			cmd = 'get'
	elif method == 'PUT':
		cmd = 'set'
	elif method == 'PATCH':
		if 'inc'in args:
			cmd = 'inc'
		else:
			cmd = 'update'
	elif method == 'POST':
		cmd = 'add'
	elif method == 'DELETE':
		cmd = 'delete'
		
	if cmd:
		return execute(cmd, path, args, data_str)
	

def execute(cmd, path, args, data_str):
	
	#print(cmd + ' ' + path)
	opt = Options(args)
	
	if cmd in ['set','add','update','delete','inc']:
		if cmd == 'delete':
			changelog.write(path + '\n\n')
		else:
			changelog.write(path + '\n' + data_str + '\n\n')
		changelog.flush()
	
	#changelog_size = os.path.getsize('changelog')
	
	#if changelog_size > dump_size:
	#	print('Dumping...')
	#	mysodb.dump('dump.temp')
	#	changelog.truncate(0)
	#	os.rename('dump.temp', 'dump')
	#	dump_size = os.path.getsize('dump')
	
	if cmd in ['get','find','count','delete']:
		return asodb.__dict__[cmd](path, opt)
	else:
		return asodb.__dict__[cmd](path, opt, data_str)