# Shapely to Plotly
## Introduction
Shapely to Plotly plots Shapely geometries via Plotly.
shapely_plotly will add `plotly_*(...)` methods to shapely objects, allowing them to be 
plotted on 2D or 3D Plotly graphs.  

Cascading styles are provided to control line style, 
marker style and fills.

## Release Notes

This is the v1.0 release.

* Original intended feature set is implemented
* For complete documentation see [docs/documentation.md](docs/documentation.md)
* All major features have been tested.  See [docs/testing.md](docs/testing.md) for details.

## Compatibility
Shapely to Plotly should be robust across a wide range of current platforms.

Shapely to Plotly runs on Linux and Windows. It has been tested on Windows 11, and Ubuntu 22.04.2 LTS via WSL 2.0.

Testing has been performed on Python 3.9 and 3.11.  

At least Shapely 2.0 is required.

## Installation
* Clone this repo.
* Add the repo's parent directory to your PYTHONPATH
* Install Shapely (https://shapely.readthedocs.io/en/stable/manual.html) and Plotly (https://plotly.com/python/) normally.
* Recommend installing Numpy (https://numpy.org/). Numpy is not needed by Shapely or Shapely to Plotly.  However it is an excellent way to build geometry, and is used by the examples [../examples](../examples).
* Import and use shapely normally.
* Import and use Shapely to Plotly: `import shapeply_plotly`


You will find that geometry objects have `plotly_draw2d(...)` 
and `plotly_draw3d(...)` methods.  

Use `shapely_plotly.show2d`  `shapely_plotly.show3d` to show your plots.  See these simple
helper functions in `plot.py` for example of creating and showing figures.

All Shapely geometry objects are supported:
* `Point`
* `Polygon`
* `LineString`
* `LinearRing`
* `MultiPoint`
* `MultiPolygon`
* `MultiLineString`
* `GeometryCollection`

See the try_*.py files for more detailed examples.

See [docs/documentation.md](docs/documentation.md) for complete documentation.

