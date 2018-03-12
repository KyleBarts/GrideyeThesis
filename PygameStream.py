#from Adafruit_AMG88xx import Adafruit_AMG88xx
import pygame
import os
import math
import time
import csv
import cv2
from datetime import datetime

import numpy as np
from scipy.interpolate import griddata
from collections import OrderedDict

from time import sleep

from colour import Color


img = np.zeros((480,480,3), np.uint8)
cv2.rectangle(img, (0, 0), (30,30), 200)
cv2.imshow('image', img)
os.environ

#how many color values we can have
COLORDEPTH = 1024

os.putenv('SDL_FBDEV', '/dev/fb1')
# pygame.init()



#initialize the sensor
#sensor = Adafruit_AMG88xx()

points = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
avepoints = [(math.floor(ix / 8), (ix % 8)) for ix in range(0, 64)]
grid_x, grid_y = np.mgrid[0:7:32j, 0:7:32j]

print avepoints

#sensor is an 8x8 grid so lets do a square
height = 480
width = 480

#the list of colors we can choose from
blue = Color("indigo")
colors = list(blue.range_to(Color("red"), COLORDEPTH))

#create the array of colors
colors = [(int(c.blue * 255), int(c.green * 255), int(c.red * 255)) for c in colors]

displayPixelWidth = width / 30
displayPixelHeight = height / 30

# lcd = pygame.display.set_mode((width, height))

# lcd.fill((255,0,0))

# pygame.display.update()
# pygame.mouse.set_visible(False)

# lcd.fill((0,0,0))
# pygame.display.update()

#some utility functions
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def map(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
  reader = csv.DictReader(open("data.csv"))

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

averagepixels = []
iterator = 0
storage = []
timekeeper = []
reader = csv.DictReader(open("ConcatFirst.csv"))

for row in reader:
    storagerow = []
    
    rowkeeper = 0
    sorted_row = OrderedDict(sorted(row.items(),
        key=lambda item: reader.fieldnames.index(item[0])))
    
    
    for col, pixel in sorted_row.items():
        #print pixel
        if(col=="Column1"):
            timekeeper.append(float(pixel))

        if(col!="Column1") and (col!="Column2.65"): 
            rowkeeper = rowkeeper + 1

            if(isfloat(pixel)):
                storagerow.append(float(pixel))
            else:
                storagerow.append(23)

    #print "HELLO ITS ME"
    storage.append(storagerow)
    iterator = iterator + 1
    
    if(iterator==100):
        print "TADAAAAA"
        averagepixels=storage
        averagepixels = np.average(storage, axis=0)
        print averagepixels
    #print storage

print "done"

numRows = np.asarray(storage)
maxima = np.amax(numRows)
minima = np.amin(numRows)

#low range of the sensor (this will be blue on the screen)
MINTEMP = 0

#high range of the sensor (this will be red on the screen)
MAXTEMP = 2.2

print maxima
print minima
#let the sensor initialize
time.sleep(.1)
count = 0

for row in storage:
    count = count +1
    print count
   # pygame.event.get()
    nonsubtracted = np.asarray(row)
    print nonsubtracted
    pixels = np.subtract(nonsubtracted,averagepixels)
    #read the pixels
#   pixels = sensor.readPixels()
    
    currTime= datetime.fromtimestamp(timekeeper[count]).strftime('%Y-%m-%dT%H:%M:%SZ')
    
    
    #print pixels
    pixels = [map(p, MINTEMP, MAXTEMP, 0, COLORDEPTH - 1) for p in pixels]
    #print pixels
    #perdorm interpolation
    bicubic = griddata(points, pixels, (grid_x, grid_y), method='cubic')
    print pixels
    #draw everything
    # for ix, row in enumerate(bicubic):
    #     for jx, pixel in enumerate(row):
    #         pygame.draw.rect(lcd, colors[constrain(int(pixel), 0, COLORDEPTH- 1)], (displayPixelHeight * ix, displayPixelWidth * jx, displayPixelHeight, displayPixelWidth))

    for ix, row in enumerate(bicubic):
        for jx, pixel in enumerate(row):
            cv2.rectangle(img, (displayPixelHeight * ix, displayPixelWidth * jx), ((displayPixelHeight * ix)+displayPixelHeight, (displayPixelWidth * jx)+displayPixelWidth), colors[constrain(int(pixel), 0, COLORDEPTH- 1)], thickness=-1)

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img,currTime,(0,30), font, .5,(0,255,255),1,cv2.LINE_AA)
    cv2.imshow("Window", img)

    cv2.waitKey(5)
    

    # pygame.display.update()
    