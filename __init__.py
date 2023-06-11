"""
A Python module for plotting shapely geometry objects with plotly.

All plotting is done by:

   plotly.graph_objects.Scatter(...) for 2D plotting
   plotly.graph_objects.Scatter3d(...) for 3D plotting.

The following shapely geometry objects may be plotted.

   GeometryCollection
   LineString
   LinearRing
   MultiLineString
   MultiPoint,
   MultiPolygon
   Point
   Polygon

"""
__version__ = "0.3.0"

from .style import (
    Style,
    rgb,
    default_style,
    DEFAULT,

    resolve_info  # Internal only.
)

from .plot import (
    show2d,
    show3d
)

del resolve_info
