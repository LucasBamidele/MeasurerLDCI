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
		if(self.config['metertype']=='v'):
			self.scm.measure_voltage()
		elif(self.config['metertype']=='a'):
			self.scm.measure_current()
		else :
			print('invalid config')
			exit()

	def setToVoltage(self):
		self.scm.apply_voltage()
		self.scm.source_voltage_range = float(self.config['max_voltage'])
		#self.scm.compliance_voltage = float(self.config['compliance_voltage'])
		self.scm.source_voltage = float(self.source_i)
		self.scm.enable_source()  

	def setToCurrent(self):
		self.scm.apply_current()
		self.scm.source_current_range = float(self.config['max_current'])
		self.scm.source_voltage_range = float(self.config['max_voltage'])
		self.scm.compliance_voltage = float(self.config['compliance_voltage'])
		self.scm.source_current = float(self.source_i)
		self.scm.enable_source()

	def rampFunction(self):
		number_samples = self.endTime/self.interval
		increment = (self.source_f - self.source_i)/float(number_samples)
		if(self.sourcetype == 'v'):
			print('here!')
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
			print('v', self.scm.voltage)
		elif(self.metertype == 'a') :
			self.reading.append(self.scm.current)


	def saveLog(self):
		number_samples = self.endTime/self.interval
		fn = 'log_' + self.filename
		save = open(fn, 'w+')
		inputs = np.linspace(self.source_i, self.source_f, number_samples)
		outputs = np.array(self.reading)
		self.plot(inputs, outputs)
		save.write(self.sourcetype + ', ' + self.metertype)
		save.write('\n')
		for (inp,outp) in zip(inputs, outputs):
			mystring = "{:.9f}".format(float(inp)) + ', ' + "{:.9f}".format(float(outp))
			save.write(mystring)
			save.write('\n')
		save.close()
		
	def customFunction(self):
		pass

	def plot(self, a, b):
		import matplotlib.pyplot as plt
		plt.plot(a,b)
		plt.ylabel(self.metertype)
		plt.xlabel(self.sourcetype)
		plt.savefig(self.filename + '.png')
	def execute(self):
		self.applyConfigs()
		func = self.config['type']
		if(func == 'ramp'):
			self.rampFunction()
		elif(func == 'step'):
			self.unitStepFunction
		elif(func == 'custom'):
			print('not yet implemented')
			exit('exiting...')
		self.saveLog()

def testScript():
	keithley = Keithley2400("GPIB::24")
	keithley.apply_current()                # Sets up to source current
	keithley.source_current_range = 10e-3   # Sets the source current range to 10 mA
	keithley.compliance_voltage = 10        # Sets the compliance voltage to 10 V
	keithley.source_current = 0             # Sets the source current to 0 mA
	keithley.enable_source()                # Enables the source output

	keithley.measure_voltage()              # Sets up to measure voltage

	keithley.ramp_to_current(5e-3)          # Ramps the current to 5 mA
	print(keithley.voltage)                 # Prints the voltage in Volts

	keithley.shutdown()
def main():
	measurer = Measurer('testfile')
	for a in measurer.config:
		print(a)
		print(measurer.config[a])
		print()
	print('executing...\n\n')
	measurer.execute()

if __name__ == '__main__':
	#testScript()
	main()