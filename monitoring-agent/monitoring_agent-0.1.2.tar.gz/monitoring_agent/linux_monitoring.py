import psutil
import json
import subprocess

class CPU:
	def check(self):
		check = {'cpu_times_percent': self.cpu_times_percent(), 'cpu_count': self.cpu_count()}
		return check

	def cpu_times_percent(self):
		data = []
		all_cpus = psutil.cpu_times_percent(interval = 3, percpu = True)
		for cpu in all_cpus:
			data_per_cpu = {}
			for key in cpu._fields:
				data_per_cpu[key] = getattr(cpu, key)
			data.append(data_per_cpu)
		return data

	def cpu_count(self):
		return {"cpu_logical":psutil.cpu_count(), "cpu_physical":psutil.cpu_count(logical=False)}	

class Memory:
	def check(self):
		check = {'virtual_memory': self.virtual_memory()}
		return check

	def virtual_memory(self):
		data = {}
		vmem = psutil.virtual_memory()
		for attribute in vmem._fields:
			data[attribute] = getattr(vmem, attribute)
		return data

class IO:
	pass

class Load:
	def check(self):
		check = {'load': self.load()}
		return check

	def load(self):
		try:
			with open('/proc/loadavg') as f:
				load = f.readline().split()[:3]	
		except:
			uptime = subprocess.check_output(['uptime'])
			load = uptime.split()[-3:]
		return load
		
class Network:
	def check(self):
		check = {'net_io_counters': self.net_io_counters()}
		return check

	def net_io_counters(self):
		nets=psutil.net_io_counters(pernic=True)
		data = {}
		
		for iface, d in nets.iteritems():
		  per_iface = {}
		  for attribute in d._fields:
		    per_iface[attribute] = getattr(d, attribute)
		  data[iface]=per_iface
		return data

def get_metrics():
	data = {'cpu':CPU().check(), 'network':Network().check(), 'load':Load().check(), 'memory':Memory().check()}
	print json.dumps(data)

if __name__ == '__main__':
    get_metrics()	