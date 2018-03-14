from Adafruit_AMG88xx import Adafruit_AMG88xx
import pygame
import os
import math
import time
import datetime
import csv
from datetime import datetime

import numpy as np
from scipy.interpolate import griddata





#how many color values we can have
COLORDEPTH = 1024

os.putenv('SDL_FBDEV', '/dev/fb1')

#initialize the sensor
sensor = Adafruit_AMG88xx()

#let the sensor initialize
time.sleep(.1)

with open(os.getcwd()+'/data/'+datetime.fromtimestamp(time.time()).strftime('%Y-%m-%dT %H-%M-%SZ')+".csv", "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=' ')
	
	while(1):
		output = []
		#read the pixels
		pixels = sensor.readPixels()
		output.append(time.time())
		output.append(pixels)
		print time.time()
		print os.getcwd()
		writer.writerow(output)
