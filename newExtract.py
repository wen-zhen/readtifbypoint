#!/usr/bin/python
# -*- coding:utf8 -*-

#read tif from point shp

import arcpy
import numpy as np

raster = 'ziyuan_beidao.tif'

point = 'point_erase.shp'

image = arcpy.Raster(r"**.tif")
arrImg = arcpy.RasterToNumPyArray(image)

cellSizeX=image.meanCellHeight
cellSizeY=image.meanCellWidth

Xmin = image.extent.XMin
Xmax = image.extent.XMax
Ymin = image.extent.YMin
Ymax = image.extent.YMax

radius = 3.5
XData = np.empty((428, 4, 2 * radius, 2 * radius))
YData = np.empty(428)

fields = ['Elevation', 'SHAPE@XY']
fc = '**' + point
index = 0
with arcpy.da.SearchCursor(fc, fields) as cursor:
   for row in cursor:
       elev = row[0]

       pointX = row[1][0]

       col = int((pointX - Xmin) / cellSizeX)
       row = int((pointY - Ymax) / -cellSizeY)

       XData[index] = arrImg[:, (row - radius):(row + radius), (col - radius):(col + radius)]
       YData[index] = elev
       index = index + 1

X = './output/wv/{0}/X'.format(str(int(radius*2)))
Y = './output/wv/{0}/Y'.format(str(int(radius*2)))

np.save(X, XData)
np.save(Y, YData)
