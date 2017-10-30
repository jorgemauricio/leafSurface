#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 11:11:18 2017

@author: jorgemauricio
"""

#%% Librerias
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import csv
import os
import sys
import colorsys
from time import gmtime, strftime
from scipy import misc
import pandas as pd
from os.path import expanduser
import datetime

#%% estilo de la grafica
plt.style.use('ggplot')

#%% Functions
def checkStatus(vL, vA, vB):
    """
    Validacion de las marcas, si el pixel coincide con algun color regresa True
    """
    if (vL >= 40 and vL <= 80) and (vA >= 50 and vA <= 80) and (vB >= -40 and vB <= 10):
        return True
    else:
        return False

def checkStatusArea(vL, vA, vB):
    """
    Validación de los pixeles para contabilizar si son parte de la hoja
    """
    # validate grayscale and mark points
    if (vL >= 0 and vL <= 100 and vA > -5 and vA < 5 and vB > -5 and vB < 5) or (vL >= 40 and vL <= 80 and vA >= 50 and vA <= 80 and vB >= -40 and vB <= 10):
        return False
    else:
        return True

# Function RGB to HLS
def convertColors(vr, vg, vb):
	r = vr/255.0
	g = vg/255.0
	b = vb/255.0
	h, l, s = colorsys.rgb_to_hls(r, g, b)
	if(l >= 0.5):
		#lighter color
		return False
	else:
		#darker color
		return True

# Function RGB to Lab
def rgbToLab(vr, vg, vb):
    """
    Convertir colores del espectro RGB a Lab
    """
    r = (vr + 0.0) / 255
    g = (vg + 0.0) / 255
    b = (vb + 0.0) / 255

    if (r > 0.04045):
        r = pow((r + 0.055) / 1.055, 2.4)
    else:
        r = r / 12.92
    if (g > 0.04045):
        g = pow((g + 0.055) / 1.055, 2.4)
    else:
        g = g / 12.92
    if (b > 0.04045):
        b = pow((b + 0.055) / 1.055, 2.4)
    else:
        b = b / 12.92

    r = r * 100.0
    g = g * 100.0
    b = b * 100.0

    var_x = r * 0.4124 + g * 0.3576 + b * 0.1805
    var_y = r * 0.2126 + g * 0.7152 + b * 0.0722
    var_z = r * 0.0193 + g * 0.1192 + b * 0.9505

    var_x = var_x / 95.047
    var_y = var_y / 100.00
    var_z = var_z / 108.883

    if (var_x > 0.008856):
        var_x = pow(var_x, (1.0 / 3.0))
    else:
        var_x = (7.787 * var_x) + (16.0 / 116.0)
    if (var_y > 0.008856):
        var_y = pow(var_y, (1.0 / 3.0))
    else:
        var_y = (7.787 * var_y) + (16.0 / 116.0)
    if (var_z > 0.008856):
        var_z = pow(var_z, (1.0 / 3.0))
    else:
        var_z = (7.787 * var_z) + (16.0 / 116.0)

    var_L = (116.0 * var_y) - 16.0
    var_a = 500.0 * (var_x - var_y)
    var_b = 200.0 * (var_y - var_z)
    if (var_L >= 0 and var_L <= 100 and var_a == 0 and var_b == 0):
    	return 0.0, 0.0, 0.0
    else:
    	return var_L, var_a, var_b 

#%% load image
tempTitleImage = "images/2.jpg"
im = Image.open(tempTitleImage) # Can be many different formats.
pix = im.load()
            
#%% size of the image
x, y = im.size  # size of the image
print("X: %d Y: %d" % (x, y))

#%% Total of pixels 
totalPixeles = x * y      # Print Y
print("Total de pixeles: %d" % totalPixeles)

#%% variables
counter = 0.0
counterBackground = 0
counterColors = 0 
arrayColors = []
#statusColor = False
statusCounting = False
xInicial = 0
yInicial = 0
xFinal = 0
yFinal = 0

totalOfPoints = "x,y,v\n"
checkPoints = "x,y,v\n"
noCheckPoints = "x,y,v\n"


#%% Start processing time
startProcessing = strftime("%Y-%m-%d %H:%M:%S")

#%% Find marks
print("Tiempo inicial: {}".format(startProcessing))
print("Searching for marks...")
for u in range(1, x):
    for v in range(1, y):
        vR, vG, vB = pix[u, v]
        valueL, valueA, valueB = rgbToLab(vR, vG, vB)
        statusColor = checkStatus(valueL, valueA, valueB)
        if statusColor:
            checkPoints += "{},{},1\n".format(u,v)
            totalOfPoints += "{},{},1\n".format(u,v)
        else:
            noCheckPoints += "{},{},0\n".format(u,v)
            totalOfPoints += "{},{},0\n".format(u,v)
        counter += 1
print("Marks done...")

#%% Start processing time
endProcessing = strftime("%Y-%m-%d %H:%M:%S")
print("Tiempo Final: {}".format(endProcessing))

#%% check points
textFileCheckPoints = open('data/checkPoints.csv', "w")
textFileCheckPoints.write(checkPoints)
textFileCheckPoints.close()

#%% Read check points
dataCheckPoints = pd.read_csv('data/checkPoints.csv')

#%% Check Info
dataCheckPoints.head()

#%% x values
x_values = np.array(dataCheckPoints["x"])

#%% sort x values
x_values.sort()

#%% x1 value
x1 = x_values[0]

#%% x4 value
x4 = x_values[-1]

#%% x1 value
x3 = x1

#%% x1 value
x2 = x4

#%% xyvalues
y_values = np.array(dataCheckPoints["y"])

#%% sort x values
y_values.sort()

#%% x1 value
y1 = y_values[0]

#%% x4 value
y4 = y_values[-1]

#%% x1 value
y2 = y1

#%% x1 value
y3 = y4

#%% Print X y Y values
print("Points")
print("x1 = {}, y1 = {}".format(x1,y1))
print("x2 = {}, y2 = {}".format(x2,y2))
print("x3 = {}, y3 = {}".format(x3,y3))
print("x4 = {}, y4 = {}".format(x4,y4))

#%% tiempo de inicio
startProcessing = strftime("%Y-%m-%d %H:%M:%S")
dt_started = datetime.datetime.utcnow()
print("Tiempo Inicial: {}".format(startProcessing))

#%% Generate the area
areaPoints = "x,y\n"
for u in range(x1, x4):
    for v in range(y1, y4):
        if (u >= x1 and u <= x4 and v >= y1 and v <= y4):
            vR, vG, vB = pix[u, v]
            valueL, valueA, valueB = rgbToLab(vR, vG, vB)
            statusColor = checkStatusArea(valueL, valueA, valueB)
            if statusColor:
                pixelValue = convertColors(vR, vG, vB)
                if (pixelValue):
                    tempText = str(u) + "-" + str(v)
                    arrayColors.append(tempText)
                    areaPoints += "{},{}\n".format(u,v)
                    counterColors += 1
                else:
                    counterBackground += 1

#%% tiempo inicial
endProcessing = strftime("%Y-%m-%d %H:%M:%S")
dt_ended = datetime.datetime.utcnow()
print("Tiempo Final: {}".format(endProcessing))

#%% tiempo de proceso
print("Tiempo de proceamiento")
print((dt_ended - dt_started).total_seconds())

#%% size of the side
sideX = 24.0 / abs(x1-x4)
sideY = 17.7 / abs(y1-y4)

#%% Generate area
print("***** Color pixels: {}".format(counterColors))
areaFoliar = (sideX * sideY) * counterColors
print("***** Leaf Surface: {} cm2".format(areaFoliar))

#%% area points
tempTitleFile = 'data/areaPoints.csv'
textFileTotalOfPoints = open(tempTitleFile, "w")
textFileTotalOfPoints.write(areaPoints)
textFileTotalOfPoints.close()

#%% generate scatter plot

#%% Scatter Plot
tempTitleFile = 'data/areaPoints.csv'
dataScatterPlot = pd.read_csv(tempTitleFile)
xValues = dataScatterPlot['x']
yValues = dataScatterPlot['y']

#%% plot the points
fig, ax = plt.subplots()
ax.set_title("Mapping")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.scatter(xValues, yValues, color="blue", marker="o")
ax.legend(['punto'])
ax.grid(False)
tempTitleFile = 'results/area.png'
plt.savefig(tempTitleFile)
