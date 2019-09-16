import csv
class UnitTest(object):
	"""docstring for UnitTest
	tests to run to ensure stuff is working"""
	def __init__(self, arg):
		super(UnitTest, self).__init__()
		self.arg = arg
def read(file):
	f = open(file, 'r')
	csv_reader = csv.reader(f, delimiter=',')
	inputs, outputs, binputs, boutputs = [], [],[],[]
	next(csv_reader)
	for row in csv_reader:
		inputs.append(row[0])
		binputs.append(row[1])
		outputs.append(row[2])
		boutputs.append(row[3])
	return inputs, outputs, binputs, boutputs

def test(inputs, outputs, binputs, boutputs, config):

	import csv
	b_number_samples = 4
	number_samples = 50
	with open('matest.csv', 'w', newline='') as csvfile:
		csvwriter = csv.writer(csvfile, delimiter=',')
		row = []
		if(config['Experiment']=='parametrized_keithley'):
			for a in range(b_number_samples):
				row.append('keithley_v')
				row.append('b29_a')
				row.append('b29_v')
			csvwriter.writerow(row)
			row = []
			for b in range(number_samples):
				for a in range(b_number_samples):
					row.append(binputs[a*number_samples+b])
					row.append(outputs[a*number_samples+b])
					row.append(boutputs[a*number_samples+b])
				csvwriter.writerow(row)
				row = []

		if(config['Experiment']=='parametrized_b2901a'):
			row = []
			for a in range(b_number_samples):
				row.append('keithley_v')
				row.append('b29_a')
				row.append('b29_v')
			csvwriter.writerow(row)
			row = []
			for b in range(b_number_samples):
				for a in range(number_samples):
					row.append(binputs[a*b_number_samples+b])
					row.append(outputs[a*number_samples+b])
					row.append(boutputs[a*number_samples+b])
				csvwriter.writerow(row)

inp, out, binp, bout = read('curva_saida.txt.csv')
config = {}
config['Experiment'] = 'parametrized_keithley'
test(inp, out, binp, bout, config)


