import time
from pymeasure.instruments.keithley import Keithley2400
import numpy as np
current_time_ms = lambda:int(round(time.time()*1000))
class Measurer(object):
	"""docstring for Measurer"""
	def __init__(self, filename):
		if(filename):
			self.filename = filename
			self.scm = Keithley2400("GPIB::24")
			self.config = {}
			self.readFile()
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
			self.interval = float(self.config['interval'])
			self.metertype = self.config['metertype']
			self.endTime = float(self.config['endTime'])
			self.source_i = float(self.config['source_i'])
			self.source_f = float(self.config['source_f'])
			if(self.config['rear']=='true'):
				self.scm.use_rear_terminals()
			elif(self.config['rear']=='false'):
				self.scm.use_front_terminals()
			else :
				print('rear must be true/false')

		except Exception as e:
			raise e
			exit('Config error!')

	def setToVoltage(self):
		self.scm.apply_voltage()
		self.scm.source_voltage_range = self.config['max_voltage']
		self.scm.compliance_voltage = self.config['compliance_voltage']
		self.scm.source_voltage = self.source_i
		self.scm.enable_source()  

	def setToCurrent(self):
		self.scm.apply_current()
		self.scm.source_current_range = self.config['max_current']
		self.scm.source_voltage_range = self.config['max_voltage']
		self.scm.compliance_voltage = self.config['compliance_voltage']
		self.scm.source_current = self.source_i
		self.scm.enable_source()

	def rampFunction(self):
		number_samples = self.endTime/self.interval
		increment = (self.source_f - self.source_i)/float(number_samples)
		if(self.sourcetype == 'v'):
			self.setToVoltage()
			i = 0
			while(i < number_samples):
				time.sleep(self.interval)
				self.scm.source_voltage += increment
				self.registerReading()
				i+=1
		else :
			self.setToCurrent()
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
			self.setToVoltage()
		elif(self.sourcetype == 'a'):
			self.setToCurrent()
		j = 0
		while(j < number_samples):
			curr_time = time.time()
			j+=1
			time.sleep(self.interval)
			self.registerReading()

	def registerReading(self):
		if(self.metertype == 'v'):
			self.reading.append(self.scm.voltage)
		elif(self.metertype == 'a') :
			self.reading.append(self.scm.current)


	def saveLog(self):
		fn = 'log_' + self.filename
		save = open(fn, 'w+')
		inputs = np.linspace(self.source_i, self.source_f, number_samples)
		outputs = np.array(self.reading)
		save.write(self.sourcetype + ', ' + self.metertype)
		for (inp,outp) in zip(inputs, outputs):
			mystring = inp + ', ' + outp
			save.write(mystring)
		save.close()
		
	def customFunction(self):
		pass

	def execute(self):
		func = self.config['type']
		if(func == 'ramp'):
			self.rampFunction()
		elif(func == 'step'):
			self.unitStepFunction
		elif(func == 'custom'):
			print('not yet implemented')
			exit('exiting...')

def main():
	a = Measurer('testfile')
	print(a.config)
	for x in a.config:
		print(x)
if __name__ == '__main__':
	main()