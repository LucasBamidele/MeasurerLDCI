import matplotlib.pyplot as plt
import numpy as np
def main():
	v1 = np.linspace(0,10, 10)
	i1 = np.linspace(0, 0.1, 10)
	j = 0
	reading = []
	for v,i in zip(v1,i1):
		v2 = np.linspace(0,10, 100)
		i2 = np.linspace(0, 0.1, 100)
		y = i*np.ones(100)
		x = v2
		plt.plot(x,y)
		j+=1
	plt.savefig('haha.png')
if __name__ == '__main__':
	main()