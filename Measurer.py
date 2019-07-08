import time
from pymeasure.instruments.keithley import Keithley2400
import numpy as np
from B2901A import *
import matplotlib.pyplot as plt
current_time_ms = lambda:int(round(time.time()*1000))
"""
TODO: ADD PARAMETRIZED MEASUREMENT
	CHANGE READFILE PARAMETERS
	CHANGE HOW EXECUTE WORKS

"""
class Measurer(object):
	"""docstring for Measurer"""
	def __init__(self, filename):
		if(filename):
			self.filename = filename
			self.scm = Keithley2400("GPIB1::24")
			self.scm2 = B2901A("GPIB0::23")
			self.config = {}
			self.readFile()
			self.keithley_reading = []
			self.b2901a_reading = []

	def readFile(self):
		f = open(self.filename)
		string = f.readline()
		self.config['Experiment'] = string.split('=')[1].strip()
		print(self.config['Experiment'])
		string = f.readline()
		if(string.strip() != 'Keithley2400'):
			print('Wrong config, must be keithley2400')
			exit()
		string = f.readline()
		string = string.split(',')
		aux_dict = {}
		for x in string:
			b = x.split('=')
			aux_dict[b[0].strip()] = b[1].strip()
		self.config['Keithley2400'] = aux_dict

		string = f.readline()
		if(string.strip() != 'B2901A'):
			print('Wrong config, must be B2901A')
			exit()
		string = f.readline()
		string = string.split(',')
		aux_dict = {}
		for x in string:
			b = x.split('=')
			aux_dict[b[0].strip()] = b[1].strip()
		self.config['B2901A'] = aux_dict
		if(self.config['Keithley2400']['type'] == 'custom'):
			print('not implemented yet')
			exit()

	"""
	put here the configs
	"""
	def applyConfigs(self):
		try:
			self.sourcetype = self.config['Keithley2400']['sourcetype']
			self.interval = float(self.config['Keithley2400']['interval'])
			self.metertype = self.config['Keithley2400']['metertype']
			self.endTime = float(self.config['Keithley2400']['endTime'])
			self.source_i = float(self.config['Keithley2400']['source_i'])
			self.source_f = float(self.config['Keithley2400']['source_f'])
			if(self.config['Keithley2400']['rear']=='true'):
				self.scm.use_rear_terminals()
			elif(self.config['Keithley2400']['rear']=='false'):
				self.scm.use_front_terminals()
			else :
				print('rear must be true/false')
		except Exception as e:
			raise e
			exit('Config error!')
		if(self.config['Keithley2400']['metertype']=='v'):
			self.scm.measure_voltage()
			print('measure voltage!')
		elif(self.config['Keithley2400']['metertype']=='a'):
			self.scm.measure_current()
		else :
			print('invalid config')
			exit()

		try:
			self.scm2.sourcetype = self.config['B2901A']['sourcetype']
			self.b_metertype = self.config['B2901A']['metertype']
			self.b_source_i = float(self.config['B2901A']['source_i'])
			self.b_source_f = float(self.config['B2901A']['source_f'])
		except Exception as e:
			raise e
			exit('Config error!')
		if(self.config['B2901A']['sourcetype'] == 'v'):
			self.scm2.setVoltageOutput()
		elif(self.config['B2901A']['sourcetype']=='a'):
			self.scm2.setCurrentOutput()
		else :
			print ('invalid config')
			exit()
		self.scm2.setMaxVoltage(float(self.config['B2901A']['max_voltage']))
		if(self.config['B2901A']['metertype'] == 'v'):
			self.scm2.setMeasureVoltage()
		elif(self.config['B2901A']['metertype']=='a'):
			self.scm2.setMeasureCurrent()
		else :
			print ('invalid config')
			exit()



	def setToVoltage(self):
		self.scm.apply_voltage()
		self.scm.source_voltage_range = float(self.config['Keithley2400']['max_voltage'])
		#self.scm.compliance_voltage = float(self.config['Keithley2400']['compliance_voltage'])
		self.scm.source_voltage = float(self.source_i)
		self.scm.enable_source()  

	def setToCurrent(self):
		self.scm.apply_current()
		self.scm.source_current_range = float(self.config['Keithley2400']['max_current'])
		#self.scm.source_voltage_range = float(self.config['Keithley2400']['max_voltage'])
		self.scm.compliance_voltage = float(self.config['Keithley2400']['compliance_voltage'])
		self.scm.source_current = float(self.source_i)
		self.scm.enable_source()

	def rampFunction(self):
		number_samples = self.endTime/self.interval
		increment = (self.source_f - self.source_i)/float(number_samples)
		b_increment = (self.b_source_f - self.b_source_i)/float(number_samples)
		if(self.sourcetype == 'v'):
			print('here!')
			self.setToVoltage()
			i = 0
			while(i < number_samples):
				time.sleep(self.interval)
				self.scm.source_voltage += increment
				self.scm2.incrementSource(b_increment)
				self.registerReading()
				i+=1
		else :
			self.setToCurrent()
			i = 0
			while(i < number_samples):
				self.scm.source_current += increment
				self.scm2.incrementSource(b_increment)
				time.sleep(self.interval)
				self.registerReading()
				i+=1
	def incrementSourceKeithley(self, increment):
		if(self.sourcetype=='v'):
			self.scm.source_voltage += increment
		elif(self.sourcetype=='a'):
			self.scm.source_current += increment

	def subplot(self,x,y, mylabel):
		plt.plot(x,y, label=mylabel)

	def parametrizedB2901(self):
		number_samples = self.endTime/self.interval
		parametrized_samples = 10
		increment = (self.source_f - self.source_i)/float(parametrized_samples)
		b_increment = (self.b_source_f - self.b_source_i)/float(number_samples)
		if(self.sourcetype == 'v'):
			self.setToVoltage()
			i = 0
			while(i < parametrized_samples):
				j = 0
				self.scm2.setSource(self.b_source_i)
				while(j < number_samples):
					time.sleep(self.interval)
					self.scm2.incrementSource(b_increment)
					self.registerReading()
					j+=1
				axis_x = self.keithley_reading[i*j:i*j + j]
				axis_y = self.b2901a_reading[i*j:i*j+j]
				self.subplot(axis_x, axis_y, self.scm.source_voltage)
				self.scm.source_voltage += increment
				i+=1
		else :
			self.setToCurrent()
			i = 0
			while(i < parametrized_samples):
				j = 0
				self.scm2.setSource(0)
				while(j < number_samples):
					self.scm2.incrementSource(b_increment)
					time.sleep(self.interval)
					self.registerReading()
					j += 1
				axis_x = self.keithley_reading[i*j:i*j + j]
				axis_y = self.b2901a_reading[i*j:i*j+j]
				self.subplot(axis_x, axis_y, self.scm.source_current)
				self.scm.source_current += increment
				i+=1
		plt.savefig(self.filename + '.png')


	def parametrizedKeithley(self):
		number_samples = self.endTime/self.interval
		parametrized_samples = 10
		inputs = np.linspace(self.source_i, self.source_f, number_samples)
		increment = (self.source_f - self.source_i)/float(number_samples)
		b_increment = (self.b_source_f - self.b_source_i)/float(number_samples)
		if(self.sourcetype == 'v'):
			self.setToVoltage()
			i = 0
			while(i < parametrized_samples):
				j = 0
				self.scm.source_voltage = self.source_i
				while(j < number_samples):
					time.sleep(self.interval)
					self.scm.source_voltage += increment
					self.registerReading()
					j+=1
				axis_y = self.keithley_reading[i*j:i*j + j]
				axis_x = self.b2901a_reading[i*j:i*j+j]
				self.subplot(axis_x, axis_y, self.scm.curr_source_value)
				self.scm2.incrementSource(b_increment)
				i+=1
		else :
			self.setToCurrent()
			i = 0
			while(i < parametrized_samples):
				j = 0
				self.scm.source_current = self.source_i
				while(j < number_samples):
					self.scm.source_current += increment
					time.sleep(self.interval)
					self.registerReading()
					j += 1
				axis_y = self.keithley_reading[i*j:i*j + j]
				axis_x = self.b2901a_reading[i*j:i*j+j]
				self.subplot(axis_x, axis_y, self.scm2.curr_source_value)
				self.scm2.incrementSource(b_increment)
				i+=1

	def parametrizedMeasure(self):
		if(self.config['Experiment']=='param_b2901a'):
			self.parametrizedB2901()
		elif(self.config['Experiment']=='param_keithley'):
			self.parametrizedKeithley()


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
			self.keithley_reading.append(self.scm.voltage)
			print('v', self.scm.voltage)
		elif(self.metertype == 'a') :
			self.keithley_reading.append(self.scm.current)

		if(self.b_metertype=='v'):
			self.b2901a_reading.append(self.scm2.readVoltage())
		elif(self.b_metertype=='a'):
			self.b2901a_reading.append(self.scm2.readCurrent())



	def saveLog(self):
		number_samples = self.endTime/self.interval
		fn = 'log_' + self.filename
		save = open(fn, 'w+')
		inputs = np.linspace(self.source_i, self.source_f, number_samples)
		outputs = np.array(self.keithley_reading)
		binputs = np.linspace(self.source_i, self.source_f, number_samples)
		boutputs = np.array(self.b2901a_reading)
		save.write(self.sourcetype + ', ' + self.metertype + '\t' + self.scm2.sourcetype + ' ' + self.b_metertype)
		save.write('\n')
		for (inp,outp, binp, boutp) in zip(inputs, outputs, binputs, boutputs):
			mystring = "{:.9f}".format(float(inp)) + ', ' + "{:.9f}".format(float(outp)) + '\t'
			mystring += "{:.9f}".format(float(binp)) + ', ' + "{:.9f}".format(float(boutp))
			save.write(mystring)
			save.write('\n')
		save.close()
		if(not self.isParametrizedExperiment()):
			self.plot(inputs, outputs)
		
	def customFunction(self):
		pass

	def isParametrizedExperiment(self):
		if(self.config['Experiment']=='param_keithley' or self.config['Experiment']=='param_b2901a'):
			return True
		else:
			return False

	def plot(self, a, b):
		plt.plot(a,b)
		plt.ylabel(self.metertype)
		plt.xlabel(self.sourcetype)
		plt.savefig(self.filename + '.png')
	def execute(self):
		self.applyConfigs()
		if(self.isParametrizedExperiment()):
			print('Parametrized experiment')
			self.parametrizedMeasure()
		else :
			func = self.config['Keithley2400']['type']
			if(func == 'ramp'):
				self.rampFunction()
			elif(func == 'step'):
				self.unitStepFunction()
			elif(func == 'custom'):
				print('not yet implemented')
				exit('exiting...')
		self.saveLog()
		self.scm.shutdown()
		self.scm2.disableSourceOutput()

def testScript():
	keithley = Keithley2400("GPIB1::24")
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