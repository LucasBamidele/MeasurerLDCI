import matplotlib.pyplot as plt
import numpy as np
def main():
	f = open('n_log_testfile3')
	f.readline()
	lines = f.readlines()
	v1 = []
	a1 = []
	a2 = []
	for line in lines:
		a = line.split('\t')
		split1 = a[0].split(',')
		split2 = a[1].split(',')
		v1.append(float(split2[0]))
		a1.append(1e6*float(split1[1]))
		a2.append(1e6*float(split2[1]))
	plt.plot(v1[:20], a2[:20])
	plt.plot(v1[20:40], a2[20:40])
	plt.plot(v1[40:60], a2[40:60])
	plt.plot(v1[60:80], a2[60:80])
	plt.plot(v1[80:100], a2[80:100])
	plt.legend(['0', '0.1','0.2', '0.3', '0.4'])
	plt.show()
	plt.plot(v1[:20], a1[:20], label='0 volts')
	plt.plot(v1[20:40], a1[20:40], label='0.1 volts')
	plt.plot(v1[40:60], a1[40:60], label='0.2 volts')
	plt.plot(v1[60:80], a1[60:80], label='0.3 volts')
	plt.plot(v1[80:100], a1[80:100], label='0.4 volts')
	plt.legend(['0', '0.1','0.2', '0.3', '0.4'])
	plt.savefig('/Users/lucasbamidele/Desktop/figure9.png')


if __name__ == '__main__':
	main()