"""
Style management
"""

from __future__ import annotations
from weakref import WeakKeyDictionary

import shapely as sh

# Unique value used to identify when the DEFAULT (parent) style should be used.
DEFAULT = ["DEFAULT"]


class Style:
    """
    A cascading style defintion for plotting.
    Defines line and marker styles for lines and points.

    Style settings are passed directly to Plotly Scatter and Scatter3d functions via the
    line= and marker= keyword arguments.  See Plotly's documentation for details.  shapely_plotly
    makes no attempt to interpret or check these values.

    If any component is DEFAULT, the value will be take from the parent.  The default parent is
    shapely_plotly.default_style.

    Both 2D and 3D plotting will accept dictionaries of {"keyword":value}.  Some common keywards are:

    Lines:
       "color": Color of line as string.  See shapely_plotly.rgb function.
       "width": Number.  Width of line in points.

    Markers:
       "color":  Color of marker as string.
       "size":   Number.  Size of marker in points.
       "symbol": String identifying symbol to use for the marker 
                 E.g 'circle', 'circle-open', 'cross', 'diamond', 'diamond-open', 'square', 'square-open', 'x'
                 See https://plotly.com/python/marker-style/ for details.

    Many other keywords are available.  See the Plotly documentation for details.

    You may also use Plotly's style objects:
        plotly.graph_objects.scatter.Line  - 2D line style
        plotly.graph_objects.scatter.Marker - 2D marker style
        plotly.graph_objects.scatter3d.Line - 3D line style
        plotly.graph_objects.scatter3d.Marker - 3D marker style

    However, if you mix 2D/3D style objects (e.g. pass a 2D style to a plotly_draw3d function), plotly will
    abort with an error.  Dictionaries can be freely mixed between 2D and 3D plotting, as long as only
    attributes common to both are set.

    Note that object style information is captured when the plotly_draw*(...) method is called.  Changes to Styles()
    will not dynamically alter plots or have any effect once the draw method has been called.  The recommended usage
    is to set up styles once at beginning, and then use those styles throughout the code.

    """
    def __init__(self,
                 parent: Style = DEFAULT,
                 line_style=DEFAULT,
                 line_point_style=DEFAULT,
                 hole_line_style=DEFAULT,
                 hole_line_point_style=DEFAULT,
                 fill_color=DEFAULT,
                 point_style=DEFAULT
                 ):
        """
        Construct a style.

        :param parent:  The parent style is used for any components that are DEFAULT

        Style components.  All components default to DEFAULT.  Any DEFAULT component is taken from the parent.

        :param line_style: The style used for lines.  This used for LineString, LinearRing, and Polygon exterior
                           line segments.  It is also used for ny collection containing those elements.
        :param line_point_style: Marker style used for the ends/vertices of lines.  This applies to the same geometries
                           as line_style.

        :param hole_line_style:  This line style is used for internal holes/voids inside a polygon.
        :param hole_line_point_style: This marker style is used for the vertices for holes/voids inside a polygon.

        The hole_*_style applies only to 3D plotting.  2D plotting uses filling.

        :param point_style: This marker style is used for Point/MultiPoint objects.
        """

        # FIXME: No fill style for Polygons.

        if parent is DEFAULT:
            self.parent = default_style
        self._line_style = line_style
        self._line_point_style = line_point_style
        self._hole_line_style = hole_line_style
        self._hole_line_point_style = hole_line_point_style
        self._fill_color=fill_color
        self._point_style = point_style
        return

    # Style accessors.  If component is DEFAULT, get from parent, recursively.
    # Setters just reflect to the equivalent self._* field.

    @property
    def line_style(self):
        if self._line_style is DEFAULT:
            return self.parent.line_style
        return self._line_style

    @line_style.setter
    def line_style(self, v):
        self._line_style = v

    @property
    def line_point_style(self):
        if self._line_point_style is DEFAULT:
            return self.parent.line_point_style
        return self._line_point_style

    @line_point_style.setter
    def line_point_style(self, v):
        self._line_point_style = v

    @property
    def hole_line_style(self):
        if self._hole_line_style is DEFAULT:
            return self.parent.hole_line_style
        return self._hole_line_style

    @hole_line_style.setter
    def hole_line_style(self, v):
        self._hole_line_style = v

    @property
    def hole_line_point_style(self):
        if self._hole_line_point_style is DEFAULT:
            return self.parent.hole_line_point_style
        return self._hole_line_point_style

    @hole_line_point_style.setter
    def hole_line_point_style(self, v):
        self._hole_line_point_style = v

    @property
    def fill_color(self):
        if self._fill_color is DEFAULT:
            return self.parent.fill_color
        return self._fill_color

    @fill_color.setter
    def fill_color(self, v):
        self._fill_color = v

    #
    @property
    def point_style(self):
        if self._point_style is DEFAULT:
            return self.parent.point_style
        return self._point_style

    @point_style.setter
    def point_style(self, v):
        self._point_style = v

# Default style definition.  Boring but pleasant green, except Polygon holes are red.  No markers except for points.

default_color = "rgb(0,180, 0)"
default_fill_color = "rgba(0,220, 0, 0.3)"
default_hole_color = "rgb(150, 0, 0)"

default_style = Style(
    parent=None,
    line_style={"color": default_color, "width": 1},
    line_point_style=None,
    hole_line_style={"color": default_hole_color, "width": 1},
    hole_line_point_style=None,
    fill_color=default_fill_color,
    point_style={"color": default_color, "size": 3, "symbol": "circle"}
)


def rgb(r, g, b, a=1.0):
    """
    Convenience function.  Get a Plotly color string for R,G,B values, with optional alpha.

    :param r, g, b: Red, Green, Blue components.  Integer 0 to 255.
    :param a: Alpha component.  Float 0.0 to 1.0.  0.0 is invisible.  1.0 (default) is opaque.
    """

    if a == 1.0:
        return f'rgb({r},{g},{b})'

    return f'rgba({r},{g},{b},{a})'


class GeometryInfo:
    """
    Plotly meta-data for shapely geometry objects.

    Shapely geometries are not normal Python objects, and we cannot add fields to them.
    Instead we keep meta-data (style, name) in a separate mapping from geometry objects to info.
    The mapping is weak, in that if the geometry object is collected, the mapping will be removed.
    """

    def __init__(self):
        self.style = DEFAULT
        self.name = None
        return


# Mapping from geometry to meta-data
global_geom_data = WeakKeyDictionary()


def geom_get_info(geom):
    """
    Retrieve the meta-data for a geometry object.
    Will create new default meta-data object if no meta-data previously defined.
    :param geom:  Shapely object.
    :return: GeometryInfo
    """
    if geom in global_geom_data:
        info = global_geom_data[geom]
    else:
        info = GeometryInfo()
        global_geom_data[geom] = info

    return info


# Meta-data accessor functions

def geom_set_style(geom, style: Style):
    """
    Set the style object for a geometry

    :param geom:  Shapely object.
    :param style: New shapely_plotly.Style object.
    """
    info = geom_get_info(geom)
    info.style = style


def geom_set_line_style(geom, line_style):
    """
    Set the line style for a geometry
    Note, this will change the line style for all objects using that style.

    :param geom:  Shapely object.
    :param line_style: New line style.
    """
    info = geom_get_info(geom)
    if info.style is DEFAULT:
        info.style = Style()

    info.style._line_style = line_style
    return


def geom_set_line_point_style(geom, line_point_style):
    """
    Set the line end/vertex style for a geometry
    Note, this will change the line style for all objects using that style.

    :param geom:  Shapely object.
    :param line_point_style: New line marker style.
    """
    info = geom_get_info(geom)
    if info.style is DEFAULT:
        info.style = Style()

    info.style._line_point_style = line_point_style
    return


def geom_set_hole_line_style(geom, hole_line_style):
    """
    Set the line style for Polygon holes
    Note, this will change the hole line style for all objects using that style.

    :param geom:  Shapely object.
    :param hole_line_style: New line style.
    """
    info = geom_get_info(geom)
    if info.style is DEFAULT:
        info.style = Style()

    info.style._hole_line_style = hole_line_style
    return


def geom_set_hole_line_point_style(geom, hole_line_point_style):
    """
    Set the hole vertex style for a Polygon holes.
    Note, this will change the hole vertex style for all objects using that style.

    :param geom:  Shapely object.
    :param hole_line_point_style: New marker style.
    """
    info = geom_get_info(geom)
    if info.style is DEFAULT:
        info.style = Style()

    info.style._hole_line_point_style = hole_line_point_style
    return


def geom_set_fill_color(geom, fill_color):
    """
    Set the style for a geometry
    Note, this will change the point style for all objects using that style.

    :param geom:  Shapely object.
    :param fill_color: New point marker style.
    """
    info = geom_get_info(geom)
    if info.style is DEFAULT:
        info.style = Style()

    info.style._fill_color = fill_color
    return

def geom_set_point_style(geom, point_style):
    """
    Set the style for a geometry
    Note, this will change the point style for all objects using that style.

    :param geom:  Shapely object.
    :param point_style: New point marker style.
    """
    info = geom_get_info(geom)
    if info.style is DEFAULT:
        info.style = Style()

    info.style._point_style = point_style
    return


def geom_set_name(geom, name: str):
    """
    Set the name of a geometry.  The name will show up in the plot legend, and also on object tool tips.
    :param geom:  Shapely object.
    :param name:  New geometry name.
    """
    info = geom_get_info(geom)
    info.name = name


def geom_get_style(geom):
    """
    Get the style for a geometry.  You can directly manipulate the Style object to change all objects
    using that style.

    :param geom:  Shapely object.
    :return: The Style() object.
    """
    info = geom_get_info(geom)
    return info.style


def geom_get_name(geom):
    """
    Get the name of a geometry.
    :param geom: Shepely object.
    :return: The name.
    """
    info = geom_get_info(geom)
    return info.name


# Add accessor functions to the geometry classes
for cl in [sh.Point, sh.Polygon, sh.LineString, sh.LinearRing, sh.MultiPoint,
           sh.MultiPolygon, sh.MultiLineString, sh.GeometryCollection]:
    cl.plotly_set_name = geom_set_name
    cl.plotly_set_style = geom_set_style
    cl.plotly_set_line_style = geom_set_line_style
    cl.plotly_set_line_point_style = geom_set_line_point_style
    cl.plotly_set_hole_line_style = geom_set_hole_line_style
    cl.plotly_set_hole_line_point_style = geom_set_hole_line_point_style
    cl.plotly_set_fill_color = geom_set_fill_color
    cl.plotly_set_point_style = geom_set_point_style
    cl.plotly_get_name = geom_get_name
    cl.plotly_get_style = geom_get_style


# Default geometry object metadata.
default_info = GeometryInfo()
default_info.style = default_style


def resolve_info(geom, style, name):
    """
    Determine the style to use for a particular draw command.
    This will be the passed in style, if not DEFAULT.
    Otherwise the style specified for the geometry
    Otherwise the default style.

    The name is handled similarly.

    :param geom:  Shapely object.
    :param style:  Style passed into the draw command.
    :param name:  Name passed into the draw command.
    :return: Style object.
    """

    # We will need to get info if either is DEFAULT
    if (style is DEFAULT) or (name is DEFAULT):
        if geom in global_geom_data:
            info = global_geom_data[geom]
        else:
            info = default_info

    # Resolve style
    #  1) Value passed in
    #  2) Value from style
    #  3) default_style
    if style is DEFAULT:
        if info.style is DEFAULT:
            style = default_style
        else:
            style = info.style

    # Resolve name:
    #  1) Value passed in
    #  2) Info value (defaults to None)
    if name is DEFAULT:
        name = info.name

    if name is None:
        # Plot empty name, do not show in legend.
        return style, "", False

    return style, name, True
