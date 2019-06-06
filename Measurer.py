import time
current_time_ms = lambda:int(round(time.time()*1000))
class Measurer(object):
	"""docstring for Measurer"""
	def __init__(self, filename):
		if(filename):
			self.filename = filename
			self.config = {}
			self.readFile()
			self.scm = None		#change later
			self.reading = []

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
		try:
			self.sourcetype = self.config['sourcetype']
			self.interval = self.config['interval']
			self.metertype = self.config['metertype']
			self.endTime = self.config['endTime']
			self.source_i = self.config['source_i']
			self.source_f = self.config['source_f']

			#sourcemeter configs
			self.scm.max = self.config['sourcetype']
		except Exception as e:
			raise e
			exit()

	def rampFunction(self):
		number_samples = self.endTime/self.interval
		increment = (self.source_f - self.source_i)/float(number_samples)
		if(self.sourcetype == 'v'):
			self.scm.source_voltage = source_i
			i = 0
			while(i < number_samples):
				time.sleep(self.interval)
				self.scm.source_voltage += increment
				self.registerReading()
				i+=1
		else :
			self.scm.source_current = source_i
			i = 0
			while(i < number_samples):
				self.scm.source_current += increment
				time.sleep(self.interval)
				self.registerReading()
				i+=1

	def unitStepFunction(self):
		number_samples = self.endTime/self.interval
		self.scm.source_current = source.i
		time.sleep(0.1)
		if(self.sourcetype == 'v'):
			self.scm.source_voltage = source.f
		else:
			self.scm.source_current = source.f
		j = 0
		while(j < number_samples):
			curr_time = time.time()
			j+=1
			time.sleep(self.interval)
			self.registerReading()

	def registerReading(self):
		if(self.metertype == 'v'):
			self.reading.append(self.scm.voltage)
		else :
			self.reading.append(self.scm.current)


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