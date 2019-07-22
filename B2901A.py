import visa
from time import sleep
"""
adicionar measure speed
"""
class B2901A(object):
	"""docstring for B901A"""
	def __init__(self,port):
		rm = visa.ResourceManager()
		self.scm = rm.open_resource(port +'::INSTR')
		self.curr_source_value = 0;
		self.sourcetype = ''
		self.metertype = ''
		#self.scm = rm.open_resource('GPIB0::23::INSTR')

	def reset(self):
		self.write("*RST")

	def write(self, command):
		self.scm.write(command)

	def query(self, command):
		return self.scm.query(command)

	def read(self, command):
		pass
		
	def enableSourceOutput(self):
		self.write(":OUTP ON")

	def disableSourceOutput(self):
		self.write(":OUTP OFF")

	def setVoltageOutput(self):
		self.write(":SOUR:FUNC:MODE VOLT")

	def incrementSource(self, increment):
		self.curr_source_value += increment
		if(self.sourcetype == 'v'):
			self.applyVoltage(self.curr_source_value)
		elif(self.sourcetype=='a'):
			self.applyCurrent(self.curr_source_value)

	def setSource(self, value):
		self.curr_source_value = value
		if(self.sourcetype == 'v'):
			self.applyVoltage(value)
		elif(self.sourcetype=='a'):
			self.applyCurrent(value)
	def setCurrentOutput(self):
		self.write(":SOUR:FUNC:MODE CURR")

	def applyCurrent(self, value):
		self.write(":SOUR:CURR " + str(value))

	def applyVoltage(self, value):
		self.write(":SOUR:VOLT " + str(value))

	def setMaxVoltage(self, value=10):
		self.write(":SENS:VOLT:PROT " + str(value))

	def setMaxCurrent(self, value=0.1):
		self.write(":SENS:CURR:PROT " + str(value))

	def setVoltageRange(self, range):
		self.write(":SOUR:VOLT:RANG:AUTO OFF")
		self.write(":SOUR:VOLT:RANG 2")

	def setMeasureVoltage(self):
		self.write(":SOUR:FUNC VOLT")

	def setMeasureCurrent(self):
		self.write(":SENS:FUNC CURR")

	def readVoltage(self):
		return self.query(":MEAS:VOLT?")
	
	def readCurrent(self):
		return self.query(":MEAS:CURR?")

def main():
	a = B2901A("GPIB0::23")
	a.enableSourceOutput()
	a.setCurrentOutput()
	a.applyCurrent(0)
	sleep(0.1)
	a.setMeasureVoltage()
	a.setMaxVoltage(10)
	for x in range(0,101):
		curr_value = 0.005*(0.01*x)
		a.applyCurrent(curr_value)
		print('current: ', "{:.9f}".format(curr_value), '  voltage: ', "{:.9f}".format(float(a.readVoltage())))
		sleep(0.1)
	a.disableSourceOutput()


if __name__ == '__main__':
	main()

		