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

#%% Clear terminal
os.system('clear')

#%% chance workdirectory
home = expanduser("~")
home += "/Documents/Research/leafSurface"
os.chdir(home)

#%% Functions
def checkStatus(vL, vA, vB):
    status = False
    if (vL >= 40.0 and vL <= 80.0):
        if (vA >= 50.0 and vA <= 80.0):
            if (vB >= -40.0 and vB <= 10.0):
                status = True
    else:
        status = False
    return status

def checkStatusArea(vL, vA, vB):
    status = False
    # validate grayscale
    if (vL >= 0 and vL <= 100.0 and vA > -5.0 and vA < 5.0 and vB > -5.0 and vB < 5.0):
        status = False
    # validate mark color
    elif (vL >= 40.0 and vL <= 80.0 and vA >= 50.0 and vA <= 80.0 and vB >= -40.0 and vB <= 10.0):
        status = False
    else:
        status = True
    return status

# Function RGB to HLS
def convertColors(vr, vg, vb):
	r = vr/255.0
	g = vg/255.0
	b = vb/255.0
	colorPixel = 0
	h, l, s = colorsys.rgb_to_hls(r, g, b)
	if(l >= 0.5):
		#lighter color
		colorPixel = 1
		return colorPixel
	elif (l < 0.5):
		#darker color
		colorPixel = 0
		return colorPixel

# Function RGB to Lab
def rgbToLab(vr, vg, vb):
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
fileList = [x for x in os.listdir('images') if x.endswith('.JPG')]

print(fileList)

for file in fileList:
    tempTitleImage = "images/{}".format(file)
    tempTitle = file.split('.')
    im = Image.open(tempTitleImage) # Can be many different formats.
    pix = im.load()
                
    #%% size of the image
    x, y = im.size  # size of the image
    print("***** Size of file {}:".format(file))
    print("***** X: %d Y: %d" % (x, y))

    #%% Total of pixels 
    totalPixeles = x * y      # Print Y
    print("***** Total Pixels: {}".format(totalPixeles))

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
    checkPoints = "x,y,l,a,b\n"
    noCheckPoints = "x,y,v\n"

    #%% status Bar
    #def displayStatusBar(xV, yV, c):
    #    sys.stdout.write('\r')
    #    totalOfPoints = xV * yV
    #    valueToDisplay = c * 100 / totalOfPoints
    #    sys.stdout.write("[{}] {}".format('='*int(valueToDisplay/10), round(valueToDisplay,2)))
    #    sys.stdout.flush()
        
    #%% Start processing time
    startProcessing = strftime("%Y-%m-%d %H:%M:%S")

    #%% Find marks
    print("***** Searching for marks...")
    for u in range(1, x):
        for v in range(1, y):
            vR, vG, vB = pix[u, v]
            valueL, valueA, valueB = rgbToLab(vR, vG, vB)
            statusColor = checkStatus(valueL, valueA, valueB)
            if statusColor:
                checkPoints += "{},{},{},{},{}\n".format(u,v,valueL, valueA, valueB)
                totalOfPoints += "{},{},1\n".format(u,v)
            else:
                noCheckPoints += "{},{},0\n".format(u,v)
                totalOfPoints += "{},{},0\n".format(u,v)
            counter += 1
    print("***** Marks done...")

    #%% check points
    print("***** Generating check points file...")
    tempTitleFile = 'data/{}_checkPoints.csv'.format(tempTitle[0])
    textFileCheckPoints = open(tempTitleFile, "w")
    textFileCheckPoints.write(checkPoints)
    textFileCheckPoints.close()

    #%% no Check Points
    #textFileNoCheckPoints = open('data/noCheckPoints.csv', "w")
    #textFileNoCheckPoints.write(noCheckPoints)
    #textFileNoCheckPoints.close()

    #%% total of points
    #textFileTotalOfPoints = open('data/totalOfPoints.csv', "w")
    #textFileTotalOfPoints.write(totalOfPoints)
    #textFileTotalOfPoints.close()

    #%% Read check points
    tempTitleFile = 'data/{}_checkPoints.csv'.format(tempTitle[0])
    dataCheckPoints = pd.read_csv(tempTitleFile)

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

    #%% x2 value
    x2 = x4

    #%% x3 value
    x3 = x1

    #%% x values
    y_values = np.array(dataCheckPoints["y"])

    #%% sort x values
    y_values.sort()

    #%% x1 value
    y1 = y_values[0]

    #%% x4 value
    y4 = y_values[-1]

    #%% x2 value
    y2 = y1

    #%% x3 value
    y3 = y4

    #%% Print X y Y values
    print("***** Points")
    print("***** x1 = {}, y1 = {}".format(x1,y1))
    print("***** x2 = {}, y2 = {}".format(x2,y2))
    print("***** x3 = {}, y3 = {}".format(x3,y3))
    print("***** x4 = {}, y4 = {}".format(x4,y4))

    #%% Generate the area
    areaPoints = "x,y,l,a,b\n"
    print("***** Generating surface...")
    for u in range(1, x):
        for v in range(1, y):
            if (u >= x1 and u <= x4 and v >= y1 and v <= y4):
                vR, vG, vB = pix[u, v]
                valueL, valueA, valueB = rgbToLab(vR, vG, vB)
                statusColor = checkStatusArea(valueL, valueA, valueB)
                if statusColor:
                    pixelValue = convertColors(vR, vG, vB)
                    if (pixelValue == 0):
                        tempText = str(u) + "-" + str(v)
                        arrayColors.append(tempText)
                        areaPoints += "{},{},{},{},{}\n".format(u,v,valueL, valueA, valueB)
                        counterColors += 1
                    elif (pixelValue == 1):
                        counterBackground += 1
    
    #%% print finish
    print("***** Finish surface...")
    
    #%% size of the side
    sideX = 24.0 / abs(x1-x4)
    sideY = 17.7 / abs(y1-y4)

    #%% Generate area
    print("***** Color pixels: {}".format(counterColors))
    areaFoliar = (sideX * sideY) * counterColors
    print("***** Leaf Surface: {} cm2".format(areaFoliar))

    #%% area points
    tempTitleFile = 'data/{}_areaPoints.csv'.format(tempTitle[0])
    textFileTotalOfPoints = open(tempTitleFile, "w")
    textFileTotalOfPoints.write(areaPoints)
    textFileTotalOfPoints.close()

    #%% generate scatter plot

    #%%	Scatter Plot
    tempTitleFile = 'data/{}_areaPoints.csv'.format(tempTitle[0])
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
    tempTitleFile = 'results/{}_area.png'.format(tempTitle[0])
    plt.savefig(tempTitleFile)
