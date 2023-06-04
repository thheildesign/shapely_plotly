"""
The entire purpose of this file is to add methods to Shapely geometry classes.  No
symbols need be exported.

This file defines the plotting functions for different Shapely objects.
"""

from __future__ import annotations
import shapely as sh
import plotly.graph_objects as graph

from shapely_plotly import DEFAULT, resolve_info
import random as rnd

# ------------------------------------------------------------------------
# Plotting functions
# ------------------------------------------------------------------------

# FIXME: Add generic plotly parameter args to Style

# shapely Point
def plot_point3d(sh_point, data, style=DEFAULT, name=DEFAULT):
    """
    Plot point - 3D.

    :param sh_point: Shapely point object.
    :param data: List of plotly graph objects.  Graph is appended to this.
    :param style:  shapely_plotly Style object.  Overrides any style defined for sh_point.
    :param name:   Name for the object in Plotly plot.  Overrides any name defined for the sh_point.
    """

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
    """
    Plot point - 2D.

    :param sh_point: Shapely point object.
    :param data: List of plotly graph objects.  Graph is appended to this.
    :param style:  shapely_plotly Style object.  Overrides any style defined for sh_point.
    :param name:   Name for the object in Plotly plot.  Overrides any name defined for the sh_point.
    """

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
    """
    Plot multi-point - 3D.

    :param sh_multipoint: Shapely point object.
    :param data: List of plotly graph objects.  Graph is appended to this.
    :param style:  shapely_plotly Style object.  Overrides any style defined for sh_multipoint.
    :param name:   Name for the object in Plotly plot.  Overrides any name defined for the sh_multipoint.
    """

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
    """
    Plot multi-point - 2D.

    :param sh_multipoint: Shapely point object.
    :param data: List of plotly graph objects.  Graph is appended to this.
    :param style:  shapely_plotly Style object.  Overrides any style defined for sh_multipoint.
    :param name:   Name for the object in Plotly plot.  Overrides any name defined for the sh_multipoint.
    """

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
    """
    Internal function.  Get the line style info for a geometry object, based on
    parameters passed into a draw command, and style/name set for the object.
    """
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
    """
    Internal function.  Get style for lines and plot them, 3D.
    """
    if len(xs) == 0:
        # Empty line
        return

    mode, line_style, marker_style, name, show_legend = plot_lines_style_info(geom, style, name, as_hole)

    scat = graph.Scatter3d(x=xs, y=ys, z=zs,
                           line=line_style,
                           marker=marker_style,
                           name=name, showlegend=show_legend,
                           mode=mode)
    data.append(scat)
    return


def plot_lines2d(geom, xs, ys, data, style, name, as_hole):
    """
    Internal function.  Get style for lines and plot them, 2D.
    """
    if len(xs) == 0:
        # Empty line
        return

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
    """
    Plot line String/Ring - 3D.

    :param sh_line_string: Shapely point object.
    :param data: List of plotly graph objects.  Graph is appended to this.
    :param style:  shapely_plotly Style object.  Overrides any style defined for sh_line_string.
    :param name:   Name for the object in Plotly plot.  Overrides any name defined for the sh_line_string.
    """
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
    """
    Plot line String/Ring - 2D.

    :param sh_line_string: Shapely point object.
    :param data: List of plotly graph objects.  Graph is appended to this.
    :param style:  shapely_plotly Style object.  Overrides any style defined for sh_line_string.
    :param name:   Name for the object in Plotly plot.  Overrides any name defined for the sh_line_string.
    """
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
    """
    Plot Polygon - 3D.

    :param sh_polygon: Shapely point object.
    :param data: List of plotly graph objects.  Graph is appended to this.
    :param style:  shapely_plotly Style object.  Overrides any style defined for sh_polygon.
    :param name:   Name for the object in Plotly plot.  Overrides any name defined for the sh_polygon.
    """
    ext = sh_polygon.exterior
    plot_line_string3d(ext, data, style, name)

    for ixt in sh_polygon.interiors:
        plot_line_string3d(ixt, data, style, name, as_hole=True)

    return


sh.Polygon.plotly_draw3d = plot_polygon3d


def plot_polygon2d(sh_polygon, data, style=DEFAULT, name=DEFAULT):
    """
    Plot Polygon - 2D.

    :param sh_polygon: Shapely point object.
    :param data: List of plotly graph objects.  Graph is appended to this.
    :param style:  shapely_plotly Style object.  Overrides any style defined for sh_polygon.
    :param name:   Name for the object in Plotly plot.  Overrides any name defined for the sh_polygon.
    """

    mode, line_style, marker_style, name, show_legend = plot_lines_style_info(sh_polygon, style, name, as_hole=False)

    ext = sh_polygon.exterior
    ext_n = len(ext.coords)
    ext_ccw = ext.is_ccw
    tot_c = ext_n
    num_i = len(sh_polygon.interiors)
    has_interiors = num_i > 0
    if has_interiors:
        # We need coordinates for each internal hole
        # Plus a None separate to skip to it without drawing a border
        tot_c += sum(len(ixt.coords) for ixt in sh_polygon.interiors) + num_i

        # Note on interior holes and styles.
        # We have to plot the poly as a single scatter plot to get the filling right.
        # However, we have to change marker/line styles because the holes have a different style from the
        # outside line.  plotly doesn't support changing line/marker styles in the middle of a
        # scatter plot (in very easy/general ways).
        # So, what we do is we do one scatter plot for the fill, without markers or lines.
        # Then we do two more scatter plots, one for the outside line/markers and one for the hole line/markers.
        # Finally, we tie all three together using a randomly generated legend group (which we statistically
        # expect is not used by the user anyplace else).
        if show_legend:
            legend_group = "shapely_plotly_" + str(rnd.randrange(0, 1<<64))
        else:
            legend_group = None

        # Hole styles
        h_mode, h_line_style, h_marker_style, _, _ = plot_lines_style_info(sh_polygon, style, name, as_hole=True)

        # Save exterior styles for exterior plot.
        e_mode, e_line_style = mode, line_style

        # Substitue empty line plot for the main plot.
        mode = "lines"
        line_style = {"color":"rgba(0,0,0,0)", "width":0}  # Invisible lines for fill plot.
    else:
        legend_group = None

    # List of x/y coords.
    xs = [None] * tot_c
    ys = [None] * tot_c

    # For the outer shell
    xs[0:ext_n], ys[0:ext_n] = ext.xy

    index = ext_n
    for ixt in sh_polygon.interiors:
        # xs[index], ys[index] are already None
        index += 1
        n = len(ixt.coords)
        assert n > 0  # Not support this yet.
        if ixt.is_ccw == ext_ccw:
            # Have to reverse the order.  The holes must have the opposite rotation of the exterior for
            # Plotly to draw it properly
            x, y = ixt.xy
            xs[index:index + n], ys[index:index + n] = reversed(x), reversed(y)
        else:
            xs[index:index + n], ys[index:index + n] = ixt.xy

        index += n

    style_info, _, _ = resolve_info(sh_polygon, style, name)

    fill_color = style_info.fill_color
    # Plot with fill
    scat = graph.Scatter(x=xs, y=ys,
                         line=line_style,
                         marker=marker_style,
                         fillcolor=fill_color,
                         name=name, legendgroup=legend_group, showlegend=show_legend,
                         mode=mode, fill="toself")
    data.append(scat)

    if has_interiors:
        # Plot exterior lines and markers.
        scat = graph.Scatter(x=xs[0:ext_n], y=ys[0:ext_n],
                      line=e_line_style,
                      marker=marker_style,
                      name=name, showlegend=False, legendgroup=legend_group,
                      mode=e_mode
                      )
        data.append(scat)

        # Plot holes lines and markers.
        scat = graph.Scatter(x=xs[ext_n+1:], y=ys[ext_n+1:],
                      line=h_line_style,
                      marker=h_marker_style,
                      name=name, showlegend=False, legendgroup=legend_group,
                      mode=h_mode
                      )
        data.append(scat)

    return data


sh.Polygon.plotly_draw2d = plot_polygon2d


def plot_multiline3d(sh_multiline, data, style=DEFAULT, name=DEFAULT):
    """
    Plot Multi-line string - 3D.

    :param sh_multiline: Shapely point object.
    :param data: List of plotly graph objects.  Graph is appended to this.
    :param style:  shapely_plotly Style object.  Overrides any style defined for sh_multiline.
    :param name:   Name for the object in Plotly plot.  Overrides any name defined for the sh_multiline.

    Note: The legend will contain a single entry for a MultiLineString.  The name and style of the MultiLineString
    is used.  Any names/styles defined for the individual LineString objects are ignored.  Plot them individualized
    if you want individual legend entries or styles.
    """
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
    first_line = True
    for il, l in enumerate(sh_multiline.geoms):
        coords = l.coords
        n = len(coords)
        if n == 0:
            # Empty Line.  Yes, Shapely allows this.
            # In this case we have reserved space for a separater that we do not need.
            # We will correct length of xs,ys,zs at the end.
            # Meanwhile, just skip.
            continue

        if first_line:
            first_line = False
        else:
            # Not the first line.  Add break between line strings.
            xs[index], ys[index], zs[index] = (None, None, None)
            index += 1

        xs[index:index + n], ys[index:index + n] = l.xy

        if l.has_z:
            zs[index:index + n] = (c[2] for c in coords)
        else:
            zs[index:index + n] = 0.0

        index += n

    if index < num_point:
        # This can happen if there were empty lines in the list.
        if index == 0:
            # All empty!
            return

        # Discard the remaining unused points.
        del xs[index:]
        del ys[index:]
        del zs[index:]

    plot_lines3d(sh_multiline, xs, ys, zs, data, style, name, as_hole=False)
    return


sh.MultiLineString.plotly_draw3d = plot_multiline3d


def plot_multiline2d(sh_multiline, data, style=DEFAULT, name=DEFAULT):
    """
    Plot Multi-line string - 2D.

    :param sh_multiline: Shapely point object.
    :param data: List of plotly graph objects.  Graph is appended to this.
    :param style:  shapely_plotly Style object.  Overrides any style defined for sh_multiline.
    :param name:   Name for the object in Plotly plot.  Overrides any name defined for the sh_multiline.

    Note: The legend will contain a single entry for a MultiLineString.  The name and style of the MultiLineString
    is used.  Any names/styles defined for the individual LineString objects are ignored.  Plot them individualized
    if you want individual legend entries or styles.
    """
    # We plot this as a single scatter plot, but make the lines invisible to skip between lines.
    nl = len(sh_multiline.geoms)
    if nl == 0:
        return

    n_tot = sum(len(l.coords) for l in sh_multiline.geoms)
    num_point = n_tot + (nl - 1)  # We place a (None, None, None) coordinate in the breaks to make it disconnect.
    xs = [None] * num_point
    ys = [None] * num_point

    index = 0
    first_line = True
    for il, l in enumerate(sh_multiline.geoms):
        n = len(l.coords)

        if n == 0:
            # Empty Line.  Yes, Shapely allows this.
            # In this case we have reserved space for a separater that we do not need.
            # We will correct length of xs,ys,zs at the end.
            # Meanwhile, just skip.
            continue

        if first_line:
            first_line = False
        else:
            # Not the first line.  Add break between line strings.
            xs[index], ys[index] = (None, None)
            index += 1

        xs[index:index + n], ys[index:index + n] = l.xy

        index += n

    if index < num_point:
        # This can happen if there were empty lines in the list.
        if index == 0:
            # All empty!
            return

        # Discard the remaining unused points.
        del xs[index:]
        del ys[index:]

    plot_lines2d(sh_multiline, xs, ys, data, style, name, as_hole=False)
    return


sh.MultiLineString.plotly_draw2d = plot_multiline2d


# FIXME:  Name/styles of collections.  Hmmm... what to do?
# I could add a switch.
# I could also use the name/style of the collection, if defined, otherwise fall back to
# the style of the individual objects.  Making a single Scatter object containing all different
# types of objects will be complicated though.  Must think about that.

# shapely GeometryCollection
def plot_geometry_collection3d(sh_geo_col, data, style=DEFAULT, name=DEFAULT):
    """
    Plot geometry collection - 3D.

    :param sh_geo_col: Shapely point object.
    :param data: List of plotly graph objects.  Graph is appended to this.
    :param style:  shapely_plotly Style object.  Overrides any style defined for sh_geo_col.
    :param name:   Name for the object in Plotly plot.  Overrides any name defined for the sh_geo_col.

    Note: Unless defined above, the names and styles of the contained geometry objects are used.
    Any name/style defined for the Geometry Collection itself is ignored.
    """
    # Here we just give up and plot all the individual pieces.
    for g in sh_geo_col.geoms:
        g.plotly_draw3d(data, style, name)

    return


sh.GeometryCollection.plotly_draw3d = plot_geometry_collection3d

# shapely MultiPolygon
# We use the same approach for multi-polygone.
sh.MultiPolygon.plotly_draw3d = plot_geometry_collection3d


def plot_geometry_collection2d(sh_geo_col, data, style=DEFAULT, name=DEFAULT):
    """
    Plot geometry collection - 2D.

    :param sh_geo_col: Shapely point object.
    :param data: List of plotly graph objects.  Graph is appended to this.
    :param style:  shapely_plotly Style object.  Overrides any style defined for sh_geo_col.
    :param name:   Name for the object in Plotly plot.  Overrides any name defined for the sh_geo_col.

    Note: Unless defined above, the names and styles of the contained geometry objects are used.
    Any name/style defined for the Geometry Collection itself is ignored.
    """
    # Here we just give up and plot all the individual pieces.
    for g in sh_geo_col.geoms:
        g.plotly_draw2d(data, style, name)

    return


sh.GeometryCollection.plotly_draw2d = plot_geometry_collection2d

# shapely MultiPolygon
# We use the same approach for multi-polygone.
sh.MultiPolygon.plotly_draw2d = plot_geometry_collection2d
