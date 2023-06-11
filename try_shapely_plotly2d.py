import shapely_plotly

rgb = shapely_plotly.rgb
import plotly.graph_objects as graph

import shapely as sh
import random as rnd

points = [sh.Point(rnd.random(), rnd.random()) for i in range(10)]

data = []
for i, p in enumerate(points):
    p.plotly_set_name(f"Point[{i}]")
    grey = rnd.randrange(0, 170)
    p.plotly_draw2d(data,
                    style=shapely_plotly.Style(
                        point_style={"color": rgb(grey, grey, grey), "symbol": "diamond", "size": 5},
                        scatter_kwargs={"hovertext":f"Custom hover text for Point[{i}]"}
                    )
                    )

points = [(rnd.random() + 2, rnd.random()) for i in range(10)]
l = sh.LineString(points)
l.plotly_set_line_style(line_style={"color": rgb(20, 20, 200), "width": 8})
l.plotly_set_name("Line String 1")
l.plotly_set_line_point_style({"color": "rgb(255,0,0)"})
l.plotly_draw2d(data)

points = [(rnd.random() + 2, rnd.random() + 2, rnd.random() * 0.1 + 1) for i in range(3)]
l = sh.LinearRing(points)
l.plotly_set_line_point_style({"color": "rgb(255,255,0)", "symbol": "cross", "size": 5})
l.plotly_set_name("Line Ring")
l.plotly_draw2d(data)

shp = [(4.0, 0.0), (6.0, 0.0), (6.0, 2.0), (4.0, 2.0), (4.0, 0.0)]
hop = [(4.5, 0.5), (5.5, 0.5), (5.5, 1.0), (4.5, 1.0), (4.5, 0.5)]
p = sh.Polygon(shell=shp, holes=[hop])
p.plotly_set_name("Polygon")
p.plotly_set_hole_line_style({"color": rgb(255, 0, 0), "width": 4})
p.plotly_set_fill_color(None)
p.plotly_draw2d(data)

points = [(rnd.random(), rnd.random() + 3, rnd.random()) for i in range(20)]
m = sh.MultiPoint(points)
m.plotly_set_name("MultiPoints")
m.plotly_draw2d(data)

points = [(rnd.random() * 0.5, rnd.random() * 0.5) for i in range(6)]

lpoints = []
for i in range(0, 5):
    p = [(c[0], c[1] + i + 3) for c in points]
    lpoints.append(p)

ml = sh.MultiLineString(lpoints)
ml.plotly_set_name("Multi-Line String")
ml.plotly_set_line_style({"color": "rgb(255,0,255)"})
ml.plotly_draw2d(data)

polys = []
for i in range(5):
    points = [(rnd.random() * 0.7 + 4.1, rnd.random() * 0.7 + i) for j in range(3)]
    points.append(points[0])
    p = sh.Polygon(shell=points)
    p.plotly_set_fill_color(rgb(255, 255, 0, 0.5))
    # p.plotly_set_fill_color(None)
    polys.append(p)

mpoly = sh.MultiPolygon(polys)
mpoly.plotly_set_name("Multi-Polygon")
mpoly.plotly_draw2d(data)

fig = graph.Figure(data=data)
fig.update_yaxes(scaleanchor="x", scaleratio=1)  # This forces plotly to keep the aspect ratio correct.
fig.show()

print("Done")
