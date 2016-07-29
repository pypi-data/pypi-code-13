# MIT License
# 
# Copyright (c) 2016 Shane Barbetta
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import dns.resolver, re

class Client:
	def __init__(self, endpoint, resolver):
		self.endpoint = endpoint
		self.resolver = resolver

	def get(self):
		# Set the resolver
		my_resolver = dns.resolver.Resolver()
		my_resolver.nameservers = [self.resolver]

		answer = my_resolver.query(self.endpoint, 'TXT')

		for rdata in answer:
			for txt_string in rdata.strings:
				txt_record = txt_string

		# Extract hostnames into array
		hostnames = [x.split(":")[1] for x in txt_record.split() if ":" in x]
		total_subnets = []

		for host in hostnames:
			answer = my_resolver.query(host, 'TXT')

			for rdata in answer:
				for txt_string in rdata.strings:
					txt_record = txt_string

			ip4_subnets = re.findall(r'ip4:(\S+)', txt_record)
			ip6_subnets = re.findall(r'ip6:(\S+)', txt_record)

			for subnet in ip4_subnets:
				total_subnets.append(subnet)

			for subnet in ip6_subnets:
				total_subnets.append(subnet)

		return total_subnets