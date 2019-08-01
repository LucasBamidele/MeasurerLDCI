import time
import sys
from pymeasure.instruments.keithley import Keithley2400
import numpy as np
from B2901A import *
import matplotlib.pyplot as plt
current_time_ms = lambda:int(round(time.time()*1000))
"""
TODO: ADD PARAMETRIZED MEASUREMENT
	CHANGE READFILE PARAMETERS
	CHANGE HOW EXECUTE WORKS

	LONG = 200 ms
	MEDIO = 2 ms
	normal = 20 ms
	short = 0.2 ms



	TODO: adjust log + plotting
		Clean up code
		Make readfile easier to make/read



"""
class Measurer(object):
	"""docstring for Measurer"""
	def __init__(self, filename):
		if(filename):
			self.filename = filename
			self.config = {}
			self.readFile()
			self.keithley_input = []
			self.b2901a_input = []
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

	"""
	put here the configs
	"""
	def applyConfigs(self):
		if(self.config['Keithley2400']['active'] == 'true'):
			self.scm = Keithley2400("GPIB1::24")
			try:
				self.sourcetype = self.config['Keithley2400']['sourcetype']
				self.interval = float(self.config['Keithley2400']['interval'])
				self.metertype = self.config['Keithley2400']['metertype']
				self.source_i = float(self.config['Keithley2400']['source_i'])
				self.source_f = float(self.config['Keithley2400']['source_f'])
				self.number_samples = int(self.config['Keithley2400']['number_samples']) +1
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
				print('invalid config: keithley meter type must be `a` or `v` ')
				exit()
		else :
			self.scm = False

		if(self.config['B2901A']['active'] == 'true'):
			self.scm2 = B2901A("GPIB0::23")
			try:
				self.scm2.sourcetype = self.config['B2901A']['sourcetype']
				self.b_metertype = self.config['B2901A']['metertype']
				self.b_source_i = float(self.config['B2901A']['source_i'])
				self.b_source_f = float(self.config['B2901A']['source_f'])
				self.b_interval = float(self.config['B2901A']['interval'])
				self.b_number_samples = int(self.config['B2901A']['number_samples'])+1
			
			except Exception as e:
				raise e
				exit('Config error!')
			if(self.config['B2901A']['sourcetype'] == 'v'):
				self.scm2.setVoltageOutput()
			elif(self.config['B2901A']['sourcetype']=='a'):
				self.scm2.setCurrentOutput()
			else :
				print ('invalid config: b2901a sourcetype type must be `a` or `v`')
				exit()
			self.scm2.setMaxVoltage(float(self.config['B2901A']['max_voltage']))
			if(self.config['B2901A']['metertype'] == 'v'):
				self.scm2.setMeasureVoltage()
			elif(self.config['B2901A']['metertype']=='a'):
				self.scm2.setMeasureCurrent()
			else :
				print ('invalid config')
				exit()
		else :
				self.scm2 = False
		if((not (self.scm and self.scm2)) and self.isParametrizedExperiment()):
			print('invalid config: for parametrized experiments both instruments must be active')
			exit()




	def setToVoltage(self):
		self.scm.apply_voltage()
		self.scm.source_voltage_range = float(self.config['Keithley2400']['max_voltage'])
		self.scm.compliance_voltage = float(self.config['Keithley2400']['compliance_voltage'])
		self.scm.source_voltage = float(self.source_i)
		self.scm.enable_source()  

	def setToCurrent(self):
		self.scm.apply_current()
		self.scm.source_current_range = float(self.config['Keithley2400']['max_current'])
		#self.scm.source_voltage_range = float(self.config['Keithley2400']['max_voltage'])
		self.scm.compliance_voltage = float(self.config['Keithley2400']['compliance_voltage'])
		self.scm.source_current = float(self.source_i)
		self.scm.enable_source()

	def rampB2901a(self):
		number_samples = self.b_number_samples
		b_increment = (self.b_source_f - self.b_source_i)/float(number_samples)
		i = 0
		while(i < number_samples):
			time.sleep(self.b_interval)
			self.scm2.incrementSource(b_increment)
			self.registerReading()
			i+=1

	def rampKeithley(self):
		number_samples = self.number_samples
		increment = (self.source_f - self.source_i)/float(number_samples)
		if(self.sourcetype == 'v'):
			self.setToVoltage()
			i = 0
			while(i < number_samples):
				self.scm.source_voltage += increment
				self.registerReading()
				time.sleep(self.interval)
				i+=1
		else :
			self.setToCurrent()
			i = 0
			while(i < number_samples):
				self.scm.source_current += increment
				self.registerReading()
				time.sleep(self.interval)
				i+=1

	def rampFunction(self):
		number_samples = number_samples
		increment = (self.source_f - self.source_i)/float(number_samples)
		b_increment = (self.b_source_f - self.b_source_i)/float(number_samples)
		if(self.sourcetype == 'v'):
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

	def parametrizedB2901(self, parametrized_samples):
		number_samples = self.b_number_samples
		parametrized_samples = self.number_samples

		increment = (self.source_f - self.source_i)/float(parametrized_samples)
		b_increment = (self.b_source_f - self.b_source_i)/float(number_samples)
		if(self.sourcetype == 'v'):
			self.setToVoltage()
			i = 0
			while(i < parametrized_samples):
				j = 0
				self.scm2.setSource(self.b_source_i)
				while(j < number_samples):
					time.sleep(self.b_interval)
					self.scm2.incrementSource(b_increment)
					self.registerReading()
					j+=1
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
					time.sleep(self.b_interval)
					self.registerReading()
					j += 1
				self.scm.source_current += increment
				i+=1
		self.saveplot(self.source_i, self.source_f, self.b_source_i, self.b_source_f)

	def saveplot(self,xi, xo, yi,yo):
		pass
		# ybot, ytop = plt.ylim()
		# plt.ylim(ybot, ytop)
		#plt.savefig(self.filename + ".png")

	def parametrizedKeithley(self,parametrized_samples):
		number_samples = self.number_samples
		parametrized_samples = self.b_number_samples
		inputs = np.linspace(self.source_i, self.source_f, number_samples)
		increment = (self.source_f - self.source_i)/float(number_samples)
		b_increment = (self.b_source_f - self.b_source_i)/float(parametrized_samples)
		self.scm2.setSource(self.b_source_i)
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
				self.scm2.incrementSource(b_increment)
				i+=1
		self.saveplot(self.source_i, self.source_f, self.b_source_i, self.b_source_f)

	def parametrizedMeasure(self):
		if(self.config['Experiment']=='parametrized_b2901a'):
			self.parametrizedB2901(5)
		elif(self.config['Experiment']=='parametrized_keithley'):
			self.parametrizedKeithley(5)


	def registerReading(self):
		if(self.scm):
			if(self.metertype == 'v'):
				self.keithley_reading.append(float(self.scm.voltage))
			elif(self.metertype == 'a') :
				self.keithley_reading.append(float(self.scm.current))
			if(self.sourcetype == 'a'):
				self.keithley_input.append(float(self.scm.source_current))
			else :
				self.keithley_input.append(float(self.scm.source_voltage))
		if(self.scm2):
			if(self.b_metertype=='v'):
				self.b2901a_reading.append(float(self.scm2.readVoltage()))
			elif(self.b_metertype=='a'):
				self.b2901a_reading.append(float(self.scm2.readCurrent()))
			self.b2901a_input.append(float(self.scm2.curr_source_value))
		


	def saveLog(self):
		number_samples = self.endTime/self.interval
		fn = 'log_' + self.filename
		save = open(fn, 'w+')
		if(self.keithley_input):
			inputs = np.array(self.keithley_input)
			outputs = np.array(self.keithley_reading)
		else:
			size = len(self.b2901a_input)
			inputs = np.zeros(size)
			outputs = np.zeros(size)

		if(self.b2901a_input):
			binputs = np.array(self.b2901a_input)
			boutputs = np.array(self.b2901a_reading)
		else :
			size = len(self.keithley_input)
			binputs = np.zeros(size)
			boutputs = np.zeros(size)

		save.write('keithley: ' + self.sourcetype + ', ' + self.metertype + '\t' + 'b2901a: ' +self.scm2.sourcetype + ' ' + self.b_metertype)
		save.write('\n')
		for (inp,outp, binp, boutp) in zip(inputs, outputs, binputs, boutputs):
			mystring = "{:.9f}".format(float(inp)) + ', ' + "{:.9f}".format(float(outp)) + '\t'
			mystring += "{:.9f}".format(float(binp)) + ', ' + "{:.9f}".format(float(boutp))
			save.write(mystring)
			save.write('\n')
		save.close()
		self.plot(inputs, outputs)
		

	def isParametrizedExperiment(self):
		if(self.config['Experiment']=='parametrized_keithley' or self.config['Experiment']=='parametrized_b2901a'):
			return True
		else:
			return False

	def plot(self, a, b, number=0, afilename=''):
		if(self.isParametrizedExperiment()):
			self.plotParametrized()
		else: 
			self.plot_keithley()
			self.plot_b2901a()

	def plot_keithley(self):
		if(self.scm):
			inputs, outputs = [], []
			if(self.sourcetype == 'v'):
				inputs = np.array(self.keithley_input)
				outputs = np.array(self.keithley_reading)
			elif(self.sourcetype == 'a'):
				outputs = np.array(self.keithley_input)
				inputs = np.array(self.keithley_reading)
			plt.plot(inputs, outputs)
			plt.title('keithley  v x i')
			plt.savefig(self.filename + '_keithley' + '.png')
			plt.clf()

	def plot_b2901a(self):
		if(self.scm2):
			inputs, outputs = [], []
			if(self.scm2.sourcetype == 'v'):
				inputs = np.array(self.b2901a_input)
				outputs = np.array(self.b2901a_reading)
			elif(self.scm2.sourcetype == 'a'):
				outputs = np.array(self.b2901a_input)
				inputs = np.array(self.b2901a_reading)
			plt.plot(inputs, outputs)
			plt.title('b290a1a  v x i')
			plt.savefig(self.filename + '_b2901a' + '.png')
			plt.clf()

	def plotParametrized(self):
		legends = []
		if(self.config['Experiment'] == 'parametrized_keithley'):
			j = 0
			i = int(self.number_samples)
			for inp in self.keithley_input:
				if(inp not in legends):
					legends += [inp]
				plt.plot(self.keithley_input[i*j:i*j+i], b2901a_reading[i*j:i*j+i])
				j+=1
			plt.legend(legends)
			plt.savefig(self.filename + '' + '.png')
			plt.clf()
			j = 0
			for inp in self.keithley_input:
				plt.plot(self.keithley_input[i*j:i*j+i], self.keithley_reading[i*j:i*j+i])
				j+=1
			plt.legend(legends)
			plt.savefig(self.filename + '_2' + '.png')

		elif(self.config['Experiment'] == 'parametrized_b2901a'):
			j = 0
			i = int(self.b_number_samples)
			for inp in self.b2901a_input:
				if(inp not in legends):
					legends += [inp]
				plt.plot(self.b2901a_input[i*j:i*j+i], self.keithley_reading[i*j:i*j+i])
				j+=1
			plt.legend(legends)
			plt.savefig(self.filename + '' + '.png')
			plt.clf()
			j = 0
			for inp in self.b2901a_input:
				plt.plot(self.b2901a_input[i*j:i*j+i], self.b2901a_reading[i*j:i*j+i])
				j+=1
			plt.legend(legends)
			plt.savefig(self.filename + '_2' + '.png')
		else:
			print('something is wrong')

	def execute(self):
		self.applyConfigs()
		if(self.isParametrizedExperiment()):
			print('Parametrized experiment')
			self.parametrizedMeasure()
		else :
			if(not (self.scm and self.scm2)):
				if(self.scm):
					self.rampKeithley()
				else :
					self.rampB2901a()
			else:
				self.rampFunction()
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
	filename = sys.argv[1]
	measurer = Measurer(filename)
	for a in measurer.config:
		print(a)
		print(measurer.config[a])
		print()
	print('executing...\n\n')
	measurer.execute()

if __name__ == '__main__':
	#testScript()
	main()