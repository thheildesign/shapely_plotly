from __future__ import annotations
from weakref import WeakKeyDictionary

import shapely as sh
import plotly.graph_objects as graph

g3d = graph.scatter3d

DEFAULT = []

class Style:
    def __init__(self,
                 parent:Style = DEFAULT,
                 line_style: g3d.Line = DEFAULT,
                 line_point_style: g3d.Marker = DEFAULT,
                 hole_line_style: g3d.Line = DEFAULT,
                 hole_line_point_style: g3d.Marker = DEFAULT,
                 point_style: g3d.Marker = DEFAULT
                 ):
        if parent is DEFAULT:
            self.parent = default_style
        self._line_style = line_style
        self._line_point_style = line_point_style
        self._hole_line_style = hole_line_style
        self._hole_line_point_style = hole_line_point_style
        self._point_style = point_style
        return

    @property
    def line_style(self):
        if self._line_style is DEFAULT:
            return self.parent._line_style
        return self._line_style

    @line_style.setter
    def line_style(self, v):
        self._line_style = v

    @property
    def line_point_style(self):
        if self._line_point_style is DEFAULT:
            return self.parent._line_point_style
        return self._line_point_style

    @line_point_style.setter
    def line_point_style(self, v):
        self._line_point_style = v

    @property
    def hole_line_style(self):
        if self._hole_line_style is DEFAULT:
            return self.parent._hole_line_style
        return self._hole_line_style

    @hole_line_style.setter
    def hole_line_style(self, v):
        self._hole_line_style = v

    @property
    def hole_line_point_style(self):
        if self._hole_line_point_style is DEFAULT:
            return self.parent._hole_line_point_style
        return self._hole_line_point_style

    @hole_line_point_style.setter
    def hole_line_point_style(self, v):
        self._hole_line_point_style = v

    @property
    def point_style(self):
        if self._point_style is DEFAULT:
            return self.parent._point_style
        return self._point_style

    @point_style.setter
    def point_style(self, v):
        self._point_style = v


default_color = "rgb(0,180, 0)"
default_hole_color = "rgb(150, 0, 0)"

default_style = Style(
    parent=None,
    line_style={"color":default_color, "width":1},
    line_point_style=None,
    hole_line_style={"color":default_hole_color, "width":1},
    hole_line_point_style=None,
    point_style={"color":default_color, "size":3, "symbol":"circle"}
)


def rgb(r, g, b, a=1.0):
    if a == 1.0:
        return f'rgb({r},{g},{b})'

    return f'rgba({r},{g}<{b},{a})'


# Shapely geometries are not normal Python objects, and we cannot add fields to them
# Instead we keep meta-data (style, name) in a separate mapping from geometry objects to info.
# The mapping is weak, in that if the geometry object is collected, the mapping will be removed.
class GeometryInfo:
    """
    Plotly meta-data for shapely geometry objects.
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
    :param geom:
    :return: GeometryInfo
    """
    if geom in global_geom_data:
        info = global_geom_data[geom]
    else:
        info = GeometryInfo()
        global_geom_data[geom] = info

    return info


# Meta-data accessor functions

def geom_set_style(geom, style):
    """
    Set the style for a geometry
    :param geom:
    :param style:
    :return: None
    """
    info = geom_get_info(geom)
    info.style = style


def geom_set_line_style(geom, line_style):
    """
    Set the style for a geometry
    :param geom:
    :param style:
    :return: None
    """
    info = geom_get_info(geom)
    if info.style is DEFAULT:
        info.style = Style()

    info.style._line_style = line_style
    return


def geom_set_line_point_style(geom, line_point_style):
    """
    Set the style for a geometry
    :param geom:
    :param style:
    :return: None
    """
    info = geom_get_info(geom)
    if info.style is DEFAULT:
        info.style = Style()

    info.style._line_point_style = line_point_style
    return


def geom_set_hole_line_style(geom, hole_line_style):
    """
    Set the style for a geometry
    :param geom:
    :param style:
    :return: None
    """
    info = geom_get_info(geom)
    if info.style is DEFAULT:
        info.style = Style()

    info.style._hole_line_style = hole_line_style
    return


def geom_set_hole_line_point_style(geom, hole_line_point_style):
    """
    Set the style for a geometry
    :param geom:
    :param style:
    :return: None
    """
    info = geom_get_info(geom)
    if info.style is DEFAULT:
        info.style = Style()

    info.style._hole_line_point_style = hole_line_point_style
    return


def geom_set_point_style(geom, point_style):
    """
    Set the style for a geometry
    :param geom:
    :param style:
    :return: None
    """
    info = geom_get_info(geom)
    if info.style is DEFAULT:
        info.style = Style()

    info.style._point_style = point_style
    return


def geom_set_name(geom, name):
    """
    Set the name of a geometry
    :param geom:
    :param style:
    :return: None
    """
    info = geom_get_info(geom)
    info.name = name


def geom_get_style(geom):
    """
    Get the style for a geometry.
    :param geom:
    :return: The style.
    """
    info = geom_get_info(geom)
    return info.style


def geom_get_name(geom):
    """
    Get the name of a geometry.
    :param geom:
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
    cl.plotly_set_point_style = geom_set_point_style
    cl.plotly_get_name = geom_get_name
    cl.plotly_get_style = geom_get_style

default_info = GeometryInfo()
default_info.style = default_style

def resolve_info(geom, style, name):
    """
    Determine the style to use for a particular draw command.
    This will be the passed in style, if not DEFAULT.
    Otherwise the style specified for the geometry (geom.plotly_style)
    Otherwise the default style.

    :param geom:
    :param style:
    :param name:
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


