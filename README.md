# Shapely to Plotly
## Introduction
Shapely to Plotly plots Shapely geometries via Plotly.
shapely_plotly will add `plotly_*(...)` methods to shapely objects, allowing them to be 
plotted on 2D or 3D Plotly graphs.  
Cascading styles are provided to control line style, 
marker style and fills.

This is a v0.3 release.  Please be understanding.
* Original intended feature set is implemented
* For documentation see [docs/documentation.md](docs/documentation.md)
* Code documentation is nominally complete, but needs review
* Testing has been ad hoc and minimal.

## Installation
* Clone this repo.
* Add this directories parent to your PYTHONPATH
* Install Shapely (https://shapely.readthedocs.io/en/stable/manual.html) and Plotly (https://plotly.com/python/) as normal.
* import and use shapely as normal.
* `import shapeply_plotly`

You will find that geometry objects have `plotly_draw2d(...)` 
and `plotly_draw3d(...)` methods.  

Use `shapely_plotly.show2d`  `shapely_plotly.show3d` to show your plots.  See these simple
helper functions in `plot.py` for example of creating and showing figures.

All shapely geometry objects that I am aware of are supported:
* `Point`
* `Polygon`
* `LineString`
* `LinearRing`
* `MultiPoint`
* `MultiPolygon`
* `MultiLineString`
* `GeometryCollection`

See the try_*.py files for more detailed examples.

