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

ring_color = rgb(130, 0, 0)  # Deep read
ring_markers = dict(symbol="cross", color=ring_color, size=5)
ring_style = sh2pl.Style(point_style=ring_markers)

start_color = (0, 50, 250)
end_color = (20, 255, 20)


def fade_colors(c1, c2, fade):
    nfade = 1.0 - fade
    x = tuple(int(c1[i] * nfade + c2[i] * fade + 0.4) for i in range(3))
    return rgb(*x)


arc_styles = tuple(
    sh2pl.Style(line_style=dict(
        color=fade_colors(start_color, end_color, i * 0.01),
        width=6
    ))
    for i in range(101))

num_grains = 4000
num_arcs = 200
min_arc_d = 65.0
max_arc_d = 75.0
min_arc_l = pi * 2 / 3
max_arc_l = pi * 4 / 3
arc_incl = pi * 2 / 10
num_arc_points = 50

grain_points = np.zeros(shape=(num_grains, 3), dtype=float)

d = nprnd.uniform(100, 140, size=num_grains)
a = nprnd.uniform(0.0, 2 * pi, size=num_grains)

# X-coordinates
grain_points[:, 0] = d * np.cos(a)

# Y-coordinates
grain_points[:, 1] = d * np.sin(a)

# z-coordinates
grain_points[:, 2] = nprnd.uniform(-4.0, 4.0, size=num_grains)

grains = shp.MultiPoint(grain_points)
plot_data = []

grains.plotly_draw3d(plot_data, style=ring_style, name="Ring")

# Vectorized math for drawing the planet.
# The planet is represented by (num_arcs) arcs.
# Each arc starts and ends at a distance from the center of the planet (d_starts, d_ends)
# Each arc moves along inclinations (latitudes) from (lat_starts, lat_ends)
# Each arc moves around the planet from (longitudes) from (long_starts, long_ends)


# Used when building interpolated values (interpolate_start_end below)
arc_interp = np.linspace(0.0, 1.0, num_arc_points).reshape((num_arc_points, 1))


def interpolate_start_end(s, e):
    """
    Create a matrix that interpolates from start to end for each of num_arcs starts and ends in s and e.
    Returns a (num_arc_points, num_arcs) array.
    """
    deltas = e - s
    interp = arc_interp @ deltas.reshape((1, num_arcs))
    interp = np.add(interp, s.reshape((1, num_arcs)))
    return interp


# Starting latitude bases.  Except it is flipped/shifted below.
lat_bases = nprnd.uniform(0.0, pi / 2, size=num_arcs)
arc_style_is = (lat_bases / (pi / 2) * 100 + 0.5).astype(int)

# The end of the arc is beyond the start.
lat_ends = lat_bases + nprnd.uniform(0.0, arc_incl, size=num_arcs)

# Latitudes move from poles toward the equator.  Arcs may cross the equator, but not over the top of the poles.
lat_starts = pi / 2 - lat_bases
lat_ends = pi / 2 - lat_ends

# Randomly flip some start/ends from north to south hemisphere
lat_dir = nprnd.choice([-1, 1], size=num_arcs)
lat_starts *= lat_dir
lat_ends *= lat_dir

# Create interpolated arrays of latitudes for each arc (num_arc_points x num_arcs)
lat_arrays = interpolate_start_end(lat_starts, lat_ends)

# Longitudes
long_starts = nprnd.uniform(0.0, 2 * pi, size=num_arcs)
long_ends = long_starts + nprnd.uniform(min_arc_l, max_arc_l, size=num_arcs)
long_arrays = interpolate_start_end(long_starts, long_ends)

# Distances from center of planet
d_starts = nprnd.uniform(min_arc_d, max_arc_d, size=num_arcs)
d_ends = nprnd.uniform(min_arc_d, max_arc_d, size=num_arcs)
d_arrays = interpolate_start_end(d_starts, d_ends)

# Distance along the equitorial plane for each interpolated point.  This is used to compute x/y values.
plane_ds = d_arrays * np.cos(lat_arrays)  # Distance * cosine of latitude.

# X,Y,Z coordinates for each arc point
arc_points = np.zeros(shape=(num_arc_points, num_arcs, 3), dtype=float)
arc_points[:, :, 0] = np.cos(long_arrays) * plane_ds  # X : Distance along plane * cos of longitude.
arc_points[:, :, 1] = np.sin(long_arrays) * plane_ds  # Y : Distance along plane * sin of longitude.
arc_points[:, :, 2] = np.sin(lat_arrays) * d_arrays  # Z : Distance from center * sin of latitude.

# Plot the arcs.

name = "Planet"

for arc in range(num_arcs):
    # Get the x,y,z coordinates
    arc_geom_p = arc_points[:, arc, :]

    # Build the arc geometry
    arc_geom = shp.LineString(arc_geom_p)

    # Get the style (color) for the line.
    arc_style_i = arc_style_is[arc]
    arc_style = arc_styles[arc_style_i]

    # Plot it
    arc_geom.plotly_draw3d(plot_data, style=arc_style,
                           name=f'{name}_t{arc}', legend_group="PLanetLG", show_legend=(arc == 0))

sh2pl.show3d(plot_data)
