import matplotlib.pyplot as plt
from math import pow

def get_10s_power(num) : 
	"""
		get ceil(log num to base 10)
	"""
	duply = num
	power = 0
	while duply>1:
		power += 1
		duply /= 10

	return pow(10,power-1)

def plot_letters(letters,frequency):
	"""
		Takes 2 lists as input and prints graph
		x axis : letters
		y axis : frequency
	"""
	plt.plot(letters,frequency,'r')
	plt.title('Alphabet wise arrangement')
	plt.xlabel('Alphabets')
	plt.ylabel('Frequency')

	x_max = max(letters) + get_10s_power(max(letters))
	y_max = max(frequency) + get_10s_power(max(frequency))
	plt.axis([0, x_max, 0, y_max])#xmin , xmax , ymin , ymax
	#y max at e - 76168
	plt.show()
