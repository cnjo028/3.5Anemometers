import numpy as np
import pandas as pd
import csv
import sys
import os
import time
from datetime import datetime
import re

class parselog(object):

	def __init__(self):
		#self.f = file;
		self.windspeeds = ['Windspeeds'];
		os.chdir(os.getcwd() + '/tcc/processed')
		self.dir = os.getcwd();
		self.files = np.array(os.listdir(self.dir));

	def sep(self):
		for f in self.files:
			if f[0] != '.':
				fil = open(f)
				line = fil.readline()
				if 'WindSpeed' in line:
					print line
					self.windspeeds = np.append(self.windspeeds,line)
				while line:
					if 'WindSpeed' in line:
						print line
						self.windspeeds = np.append(self.windspeeds,line)
					line = fil.readline()
				fil.close()
		self.windspeeds = np.vstack(self.windspeeds)
		np.savetxt('windspeeds.csv', self.windspeeds,fmt="%s")

		


if __name__ == '__main__':
	g = parselog();
	g.sep();
	print g.windspeeds;
