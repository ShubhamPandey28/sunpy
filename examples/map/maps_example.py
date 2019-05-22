# -*- coding: utf-8 -*-
"""
=========================================
Interacting with Data Using SunPy Maps
=========================================

In this example you will be learning how to create and modify SunPy Map objects.
"""

##############################################################################
# Start by importing the necessary modules.
import numpy as np
import matplotlib.pyplot as plt

import astropy.units as u
from astropy.coordinates import SkyCoord

import sunpy.map
import sunpy.data.sample

##############################################################################
# SunPy Maps store 2D data in a numpy array and additional data in a metadata
# dictionary giving information relating to the data and instrument.
# You can create a Map in a number of ways, including loading a FITS file or URL:
# ``mymap = sunpy.map.Map('file1.fits')``
# ``mymap = sunpy.map.Map(url_str)``
# Or using creating manually by using tuple with the data/header within:

data = np.random.rand(20, 15)
header = {'cunit1': 'arcsec', 'cunit2': 'arcsec'}
manual_map = sunpy.map.Map((data, header))

##############################################################################
# The data numpy array and metadata dictionary can easily be accessed:

print(manual_map.data)
print(manual_map.meta)

# In this case notice that the metadata has been populated by default with the
# naxis details that correspond to the array used for the data.

##############################################################################
# You can quickly plot a map using the plot method:
fig = plt.figure()
manual_map.plot()

##############################################################################
# SunPy Maps have a number of attributes that can be accessed easily.
# Most return astropy Quantity objects.
# In general the attributes are populated using details in the metadata and in
# this case there is no centre pixel or pixel size information given so SunPy
# is defaulting to assuming each pixel is 1 arcsec.
# This is in Helioprojective tangent projection in both longitude and latitude:
print(manual_map.coordinate_system)

##############################################################################
# A real map example is given in the sample data, where the sunpy.data.sample.NAME
# returns the location of the given FITS file.

aia_map = sunpy.map.Map(sunpy.data.sample.AIA_171_IMAGE)
fig = plt.figure()
aia_map.plot()
aia_map.draw_limb()

##############################################################################
# This has comprehensive metadata:

print(aia_map.meta)

##############################################################################
# And find out information about the observation device and date:

print(aia_map.date)
print(aia_map.observatory)
print(aia_map.detector)
print(aia_map.exposure_time)
print(aia_map.coordinate_system)
print(aia_map.measurement)

##############################################################################
# Maps also hold coordinate objects for the coordinate system they are in.

print(aia_map.coordinate_frame)

##############################################################################
# To see only a part of the image you create a submap, by specifying the top
# left and bottom right corners of the rectangle as either `SkyCoord` or
# `Quantity` objects.

bottom_left = aia_map.bottom_left_coord
top_right = SkyCoord(0 * u.arcsec, 0 * u.arcsec, frame=aia_map.coordinate_frame)
aia_submap = aia_map.submap(bottom_left, top_right)

fig = plt.figure()
aia_submap.plot()
aia_submap.draw_limb()
##############################################################################
# Similarly, if you want to reduce the angular resolution of the map you can use
# the `~sunpy.map.GenericMap.resample` method, specifying the dimensions as an
# Astropy Quantity in pixels:

dimensions = u.Quantity([50, 50], u.pixel)
aia_resampled_map = aia_map.resample(dimensions)

fig = plt.figure()
aia_resampled_map.plot()
aia_resampled_map.draw_grid()
aia_resampled_map.draw_limb()

##############################################################################
# Similar to resampling you can use the `~sunpy.map.GenericMap.superpixel`
# method, this will reduce the resolution of the image by combining the number
# of pixels (in each dimension) in the dimensions argument into one single
# pixel. This can be used to increase the signal to noise ratio. For this the
# new dimensions must divide original image size exactly.

dimensions = u.Quantity(aia_map.dimensions) / 16
aia_superpixel_map = aia_map.superpixel(dimensions)

fig = plt.figure()
aia_superpixel_map.plot()
aia_superpixel_map.draw_limb()

##############################################################################
# Maps can also be rotated using the `~sunpy.map.GenericMap.rotate` method:

aia_rotated_submap = aia_submap.rotate(angle=10 * u.deg)

fig = plt.figure()
aia_rotated_submap.plot()
aia_rotated_submap.draw_limb()
aia_rotated_submap.draw_grid()

# Note: the data array is expanded so that none of the original data is lost
# through clipping.
plt.show()
