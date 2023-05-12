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

all_defaults_style = Style()


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


# shapely Point
def plot_point3d(sh_point, data, style=DEFAULT, name=DEFAULT):
    if sh_point.has_z:
        z = sh_point.z
    else:
        z = 0.0

    style, name, show_legend = resolve_info(sh_point, style, name)

    assert style.point_style is not None
    scat = graph.Scatter3d(x=[sh_point.x], y=[sh_point.y], z=[z],
                           marker=style.point_style,
                           name=name, showlegend=show_legend,
                           mode="markers")

    data.append(scat)
    return


sh.Point.plotly_draw3d = plot_point3d


# shapely Point
def plot_point2d(sh_point, data, style=DEFAULT, name=DEFAULT):
    style, name, show_legend = resolve_info(sh_point, style, name)

    assert style.point_style is not None
    scat = graph.Scatter(x=[sh_point.x], y=[sh_point.y],
                           marker=style.point_style,
                           name=name, showlegend=show_legend,
                           mode="markers")

    data.append(scat)
    return


sh.Point.plotly_draw2d = plot_point2d


# shaeply MultiPoint
def plot_multipoint3d(sh_multipoint, data, style=DEFAULT, name=DEFAULT):
    points = sh_multipoint.geoms
    xs = [p.x for p in points]
    ys = [p.y for p in points]
    zs = [p.z if p.has_z else 0 for p in points]

    style, name, show_legend = resolve_info(sh_multipoint, style, name)
    assert style.point_style is not None

    scat = graph.Scatter3d(x=xs, y=ys, z=zs,
                           marker=style.point_style,
                           name=name, showlegend=show_legend,
                           mode="markers")
    data.append(scat)
    return


sh.MultiPoint.plotly_draw3d = plot_multipoint3d


def plot_multipoint2d(sh_multipoint, data, style=DEFAULT, name=DEFAULT):
    points = sh_multipoint.geoms
    xs = [p.x for p in points]
    ys = [p.y for p in points]

    style, name, show_legend = resolve_info(sh_multipoint, style, name)
    assert style.point_style is not None

    scat = graph.Scatter(x=xs, y=ys,
                           marker=style.point_style,
                           name=name, showlegend=show_legend,
                           mode="markers")
    data.append(scat)
    return


sh.MultiPoint.plotly_draw2d = plot_multipoint2d


def plot_lines_style_info(geom, style, name, as_hole):
    style, name, show_legend = resolve_info(geom, style, name)

    if as_hole:
        line_style = style.hole_line_style
        marker_style = style.hole_line_point_style
    else:
        line_style = style.line_style
        marker_style = style.line_point_style

    if line_style is None:
        if marker_style is None:
            # Invisible
            return
        mode = "markers"
    else:
        if marker_style is None:
            mode = "lines"
        else:
            mode = "lines+markers"

    return mode, line_style, marker_style, name, show_legend

def plot_lines3d(geom, xs, ys, zs, data, style, name, as_hole):
    mode, line_style, marker_style, name, show_legend = plot_lines_style_info(geom, style, name, as_hole)

    scat = graph.Scatter3d(x=xs, y=ys, z=zs,
                           line=line_style,
                           marker=marker_style,
                           name=name, showlegend=show_legend,
                           mode=mode)
    data.append(scat)
    return


def plot_lines2d(geom, xs, ys, data, style, name, as_hole):
    mode, line_style, marker_style, name, show_legend = plot_lines_style_info(geom, style, name, as_hole)

    scat = graph.Scatter(x=xs, y=ys,
                           line=line_style,
                           marker=marker_style,
                           name=name, showlegend=show_legend,
                           mode=mode)
    data.append(scat)
    return


# shapely LineString
def plot_line_string3d(sh_line_string, data, style=DEFAULT, name=DEFAULT, as_hole=False):
    coords = sh_line_string.coords
    n = len(coords)
    xs = [None] * n
    ys = [None] * n
    if sh_line_string.has_z:
        zs = [None] * n
        for i, c in enumerate(coords):
            xs[i] = c[0]
            ys[i] = c[1]
            zs[i] = c[2]
    else:
        zs = [0.0] * n
        for i, c in enumerate(coords):
            xs[i] = c[0]
            ys[i] = c[1]

    plot_lines3d(sh_line_string, xs, ys, zs, data, style, name, as_hole)
    return


sh.LineString.plotly_draw3d = plot_line_string3d


def plot_line_string2d(sh_line_string, data, style=DEFAULT, name=DEFAULT, as_hole=False):
    coords = sh_line_string.coords
    n = len(coords)
    xs, ys = sh_line_string.xy
    xs = list(xs)
    ys = list(ys)

    xs[2] = None
    ys[2] = None

    plot_lines2d(sh_line_string, xs, ys, data, style, name, as_hole)
    return


sh.LineString.plotly_draw2d = plot_line_string2d

# shapely LinearRing
# - We can use the same drawing function as line string, because shapely duplicates the start coord at the end.
sh.LinearRing.plotly_draw3d = plot_line_string3d


# shapely Polygon
def plot_polygon3d(sh_polygon, data, style=DEFAULT, name=DEFAULT):
    ext = sh_polygon.exterior
    plot_line_string3d(ext, data, style, name)

    for ixt in sh_polygon.interiors:
        plot_line_string3d(ixt, data, style, name, as_hole=True)

    return


def plot_polygon2d(sh_polygon, data, style=DEFAULT, name=DEFAULT):

    mode, line_style, marker_style, name, show_legend = plot_lines_style_info(sh_polygon, style, name, as_hole=False)

    ext = sh_polygon.exterior
    ext_n = len(ext.coords)
    ext_ccw = ext.is_ccw
    tot_c = ext_n
    num_i = len(sh_polygon.interiors)
    if num_i > 0:
        # We need coordinates for each internal hole
        # Plus a None separate to skip to it without drawing a border
        tot_c += sum(len(ixt.coords) for ixt in sh_polygon.interiors) + num_i

    xs = [None] * tot_c
    ys = [None] * tot_c
    xs[0:ext_n], ys[0:ext_n] = ext.xy

    index = ext_n
    for ixt in sh_polygon.interiors:
        # xs[index], ys[index] are already None
        index += 1
        n = len(ixt.coords)
        assert n >0 # Not support this yet.
        if ixt.is_ccw == ext_ccw:
            # Have to reverse the order.  The holes must have the opposite rotation of the exterior for
            # Plotly to draw it properly
            x,y = ixt.xy
            xs[index:index+n], ys[index:index+n] = reversed(x), reversed(y)
        else:
            xs[index:index+n], ys[index:index+n] = ixt.xy

        index += n

    scat = graph.Scatter(x=xs, y=ys,
                         line=line_style,
                         marker=marker_style,
                         name=name, showlegend=show_legend,
                         mode=mode, fill="toself")

    data.append(scat)


sh.Polygon.plotly_draw2d = plot_polygon2d


def plot_multiline3d(sh_multiline, data, style=DEFAULT, name=DEFAULT):
    # We plot this as a single scatter plot, but make the lines invisible to skip between lines.
    nl = len(sh_multiline.geoms)
    if nl == 0:
        return

    n_tot = sum(len(l.coords) for l in sh_multiline.geoms)
    num_point = n_tot + (nl - 1)  # We place a (None, None, None) coordinate in the breaks to make it disconnect.
    xs = [None] * num_point
    ys = [None] * num_point
    zs = [None] * num_point

    index = 0
    for il, l in enumerate(sh_multiline.geoms):
        coords = l.coords
        n = len(coords)
        assert (n > 0)  # FIXME: Not handling this case yet.

        if il > 0:
            # Not the first line.  Add break between line strings.
            xs[index], ys[index], zs[index] = (None, None, None)
            index += 1

        xs[index:index + n], ys[index:index + n] = l.xy

        if l.has_z:
            zs[index:index + n] = (c[2] for c in coords)
        else:
            zs[index:index + n] = 0.0

        index += n

    plot_lines3d(sh_multiline, xs, ys, zs, data, style, as_hole=False)
    return


sh.MultiLineString.plotly_draw3d = plot_multiline3d


def plot_multiline2d(sh_multiline, data, style=DEFAULT, name=DEFAULT):
    # We plot this as a single scatter plot, but make the lines invisible to skip between lines.
    nl = len(sh_multiline.geoms)
    if nl == 0:
        return

    n_tot = sum(len(l.coords) for l in sh_multiline.geoms)
    num_point = n_tot + (nl - 1)  # We place a (None, None, None) coordinate in the breaks to make it disconnect.
    xs = [None] * num_point
    ys = [None] * num_point

    index = 0
    for il, l in enumerate(sh_multiline.geoms):
        n = len(l.coords)
        assert (n > 0)  # FIXME: Not handling this case yet.

        if il > 0:
            # Not the first line.  Add break between line strings.
            xs[index], ys[index] = (None, None)
            index += 1

        xs[index:index + n], ys[index:index + n] = l.xy

        index += n

    plot_lines2d(sh_multiline, xs, ys, data, style, name, as_hole=False)
    return


sh.MultiLineString.plotly_draw2d = plot_multiline2d


# shapely GeometryCollection
def plot_geometry_collection3d(sh_geo_col, data, style=DEFAULT, name=DEFAULT):
    # Here we just give up and plot all the individual pieces.
    for g in sh_geo_col.geoms:
        g.plotly_draw3d(data, style, name)

    return


sh.GeometryCollection.plotly_draw3d = plot_geometry_collection3d

# shapely MultiPolygon
# We use the same approach for multi-polygone.
sh.MultiPolygon.plotly_draw3d = plot_geometry_collection3d

def plot_geometry_collection2d(sh_geo_col, data, style=DEFAULT, name=DEFAULT):
    # Here we just give up and plot all the individual pieces.
    for g in sh_geo_col.geoms:
        g.plotly_draw2d(data, style, name)

    return


sh.GeometryCollection.plotly_draw2d = plot_geometry_collection2d

# shapely MultiPolygon
# We use the same approach for multi-polygone.
sh.MultiPolygon.plotly_draw2d = plot_geometry_collection2d
