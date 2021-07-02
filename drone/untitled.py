import numpy as np


botMap = np.array(34*[59*['?']])


botMap[20,30] = '.'

for i in range(34):
	for j in range(59):
		print(botMap[i][j],end = " ")
	print() 