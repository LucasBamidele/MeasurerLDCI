import time
class Measurer(object):
	"""docstring for Measurer"""
	def __init__(self, filename):
		if(filename):
			self.filename = filename
			self.config = {}
			self.readFile()

	def readFile(self):
		f = open(self.filename)
		string = f.readline()
		string = string.split(',')
		for x in string:
			b = x.split('=')
			self.config[b[0].strip()] = b[1].strip()
		if(self.config['type'] == 'custom'):
			print('not implemented yet')
			exit()
	"""
	put here the configs
	"""
	def applyConfigs(self):
		pass

	def rampFunction(self):
		pass

	def pulseFunction(self):
		pass

	def customFunction(self):
		pass

	def execute(self):
		pass

def main():
	a = Measurer('testfile')
	print(a.config)
	for x in a.config:
		print(x)
if __name__ == '__main__':
	main()