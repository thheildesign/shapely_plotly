import shapely_plotly

rgb = shapely_plotly.rgb
import plotly.graph_objects as graph

import shapely as sh
import random as rnd

sat_cols = (
    (0, 1, 2),
    (0, 2, 1),
    (1, 0, 2),
    (1, 2, 0),
    (2, 0, 1),
    (2, 1, 0)
)


def rnd_sat_rgb():
    full, other, z = rnd.choice(sat_cols)
    rgb_values = [-1, -1, -1]
    rgb_values[full] = 255
    rgb_values[other] = rnd.randrange(0, 256)
    rgb_values[z] = 0
    c = rgb(*rgb_values)
    return c


def rnd_collection(name, x_off, y_off):
    points = [(rnd.random() + x_off, rnd.random() + y_off, rnd.random()) for i in range(20)]
    sh_points = [sh.Point(p[0], p[1]) for p in points]
    collection = sh.GeometryCollection(sh_points)
    collection.plotly_set_name(name)
    collection.plotly_set_point_style({"size": 5, "color": rnd_sat_rgb()})
    return collection


plot_data2d = []
for i in range(4):
    c = rnd_collection(f"Collection {i}", i*2, 0)
    c.plotly_draw2d(plot_data2d)

shapely_plotly.show2d(plot_data2d)

plot_data3d = []
for i in range(4):
    c = rnd_collection(f"Collection {i}", i * 2, 0)
    c.plotly_draw3d(plot_data3d)

shapely_plotly.show3d(plot_data3d)

print("Done")
