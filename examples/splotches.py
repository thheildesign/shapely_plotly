"""
Planet with rings, in 3D.

Makes use of numpy.  Shapely works great with numpy!
"""

import numpy as np
import numpy.random as nprnd
from math import pi

import shapely as shp
import shapely_plotly as sh2pl
from shapely_plotly import rgb

fill_color = rgb(197, 224, 180)
ext_color = rgb(84, 130, 53)
int_color = rgb(244, 177, 131)
line_color = rgb(50, 50, 50)
point_color = rgb(0, 112, 192)

object_style = sh2pl.Style(
    point_style=dict(symbol="cross", color=point_color, size=5),
    line_style=dict(color=line_color, width=3)
)

splotch_style = sh2pl.Style(
    fill_color = fill_color,
    line_style = dict(color = ext_color, width=3),
    hole_line_style = dict(color=int_color, width=3)
)

scale_fact = 4
splotch_w = 250*scale_fact
splotch_h = 150*scale_fact
splotch_num_points = 100*scale_fact*scale_fact
splotch_rad = 15

erode_num_points = 30*scale_fact*scale_fact
erode_rad = 8

splotch_points = np.zeros(shape=(splotch_num_points, 2), dtype=float)
splotch_points[:, 0] = nprnd.uniform(0.0, splotch_w, size=splotch_num_points)
splotch_points[:, 1] = nprnd.uniform(0.0, splotch_h, size=splotch_num_points)

plot_data = []

splotch_mp = shp.MultiPoint(splotch_points)
splotches = splotch_mp.buffer(splotch_rad, quad_segs=32)

erode_points = np.zeros(shape=(erode_num_points, 2), dtype=float)
erode_points[:, 0] = nprnd.uniform(0.0, splotch_w, size=erode_num_points)
erode_points[:, 1] = nprnd.uniform(0.0, splotch_h, size=erode_num_points)

erode_mp = shp.MultiPoint(erode_points)
erodes = erode_mp.buffer(erode_rad, quad_segs=32)

splotches = shp.difference(splotches, erodes)
splotches.plotly_draw2d(plot_data, style=splotch_style, name="Splotch Area")

erode_mp.plotly_draw2d(plot_data, style=object_style, name ="Erode Points")

# erodes.plotly_draw2d(plot_data, name="Erodes")

sh2pl.show2d(plot_data)
print("done")
