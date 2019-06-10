import visa
class B901A(object):
	"""docstring for B901A"""
	def __init__(self, arg):
		self.arg = arg
		rm = visa.ResourceManager()
		self.scm = rm.open_resource('GPIB0::23::INSTR')

	def reset(self):
		self.write("*RST")

	def write(self, command):
		pass

	def query(self, command):
		pass

	def read(self, command):
		pass
	def enableSourceOutput(self):
		self.write(":OUTP ON")

	def disableSourceOutput(self):
		self.write(":OUTP OFF")

	def setVoltageOutput(self):
		self.write(":SOUR:FUNC:MODE VOLT")

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

	def setToMeasureCurrent(self):
		self.write(":SENS:FUNC CURR")

	def readVoltage(self):
		return  self.query(":MEAS:VOLT?")
	


		