# Shapely on Plotly
### Introduction
Shapely on Plotly plots shapely geometries via plotly.
shapely_plotly will add `plotly_*(...)` methods to shapely objects, allowing them to be 
plotted on 2D or 3D Plotly graphs.  
Cascading styles are provided to control line style, 
marker style and fills.

This is a v0.1 release.  Please be understanding.
* Documentation consists of this README and the try_shapely_plotly*.py examples.
* Code structure is unrefined.
* Code documentation is present but incomplete
* Testing has been ad hoc and minimal.

That being said, the code is not complicated and seems to be working. 
There are no known features to add at this time.

### Installation
* Clone this repo.
* Set your PYTHONPATH to this directory (`\_\_init\_\_.py` coming soon!)
* `import shapeply_plotly`
* import and use shapely as normal.

You will find that geometry objects have `plotly_draw2d(...)` 
and `plotly_draw3d(...)` methods.  

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

