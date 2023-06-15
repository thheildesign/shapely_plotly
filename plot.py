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

# Used to generate unique legend group IDs
group_index = 0


def unique_legend_group():
    """
    Generate a unique legend group name.

    This consists of an incrementing index, and a random 64b number.
    """
    global group_index
    idx = group_index
    group_index += 1
    legend_group = f"shapely_plotly_{idx}_{rnd.randrange(0, 1 << 64)}"
    return legend_group


# ------------------------------------------------------------------------
# Plotting functions
# ------------------------------------------------------------------------


# shapely Point
def plot_point3d(sh_point, data, style=DEFAULT, name=DEFAULT, legend_group=DEFAULT):
    """
    Plot point - 3D.

    :param sh_point: Shapely point object.
    :param data: List of plotly graph objects.  Graph is appended to this.
    :param style:  shapely_plotly Style object.  Overrides any style defined for sh_point.
    :param name:   Name for the object in Plotly plot.  Overrides any name defined for the sh_point.
    :param legend_group   Legend group to use (groups multiple items under a single legend).  Overrides style.
    """

    if sh_point.has_z:
        z = sh_point.z
    else:
        z = 0.0

    style, name, show_legend, legend_group = resolve_info(sh_point, style, name, legend_group)

    scat = graph.Scatter3d(x=[sh_point.x], y=[sh_point.y], z=[z],
                           marker=style.point_style,
                           name=name, showlegend=show_legend, legendgroup=legend_group,
                           mode="markers",
                           **style.scatter_kwargs)

    data.append(scat)
    return


sh.Point.plotly_draw3d = plot_point3d


# shapely Point
def plot_point2d(sh_point, data, style=DEFAULT, name=DEFAULT, legend_group=DEFAULT):
    """
    Plot point - 2D.

    :param sh_point: Shapely point object.
    :param data: List of plotly graph objects.  Graph is appended to this.
    :param style:  shapely_plotly Style object.  Overrides any style defined for sh_point.
    :param name:   Name for the object in Plotly plot.  Overrides any name defined for the sh_point.
    :param legend_group   Legend group to use (groups multiple items under a single legend).  Overrides style.
    """

    style, name, show_legend, legend_group = resolve_info(sh_point, style, name, legend_group)

    assert style.point_style is not None
    scat = graph.Scatter(x=[sh_point.x], y=[sh_point.y],
                         marker=style.point_style,
                         name=name, showlegend=show_legend, legendgroup=legend_group,
                         mode="markers",
                         **style.scatter_kwargs)

    data.append(scat)
    return


sh.Point.plotly_draw2d = plot_point2d


# Collection style behavior.
#
# Shapely supports a number of geometries that represent collections of other geometries.  These are:
#    MultiPoint
#    MultiPolygon
#    MultiLineString
#    GeometryCollection
#
# MultiPoint is just a collection of coordinates, not Point objects.  Similarly MultiLineString
# is a collection of lists of coordinates.  These are always plotted as single objects.
#
# With MultiPolygon and GeometryCollection, the contained items are other geometries, including
# possibly nested collections in the case of GeometryCollection.  These are also always plotted as single
# items.  All contained elements are plotted with the collection's style, and all are associated with the
# same legend entry.
#
# It turns out that shapely does not store the actual Python objects that represent the collection's
# geometries.  The collections will create new Python objects everytime the geometries are extracted.
# Because they are new Python objects, they can't have name/style associated with them.
#
# Hence, you cannot add names or styles to geometries added to collections.  The attributes will be lost
# when the geometries are accessed.
#
# If you need to plot contained geometries with individual styles, names or legend entries, keep them in a
# suitable Python container, and plot them individually.

# shaeply MultiPoint
def plot_multipoint3d(sh_multipoint, data, style=DEFAULT, name=DEFAULT, legend_group=DEFAULT):
    """
    Plot multi-point - 3D.

    :param sh_multipoint: Shapely point object.
    :param data: List of plotly graph objects.  Graph is appended to this.
    :param style:  shapely_plotly Style object.  Overrides any style defined for sh_multipoint.
    :param name:   Name for the object in Plotly plot.  Overrides any name defined for the sh_multipoint.
    :param legend_group   Legend group to use (groups multiple items under a single legend).  Overrides style.
    """

    points = sh_multipoint.geoms

    style, name, show_legend, legend_group = resolve_info(sh_multipoint, style, name, legend_group)

    # Plot as a single scatter graph
    xs = [p.x for p in points]
    ys = [p.y for p in points]
    zs = [p.z if p.has_z else 0 for p in points]

    assert style.point_style is not None

    scat = graph.Scatter3d(x=xs, y=ys, z=zs,
                           marker=style.point_style,
                           name=name, showlegend=show_legend, legendgroup=legend_group,
                           mode="markers",
                           **style.scatter_kwargs)
    data.append(scat)
    return


sh.MultiPoint.plotly_draw3d = plot_multipoint3d


def plot_multipoint2d(sh_multipoint, data, style=DEFAULT, name=DEFAULT, legend_group=DEFAULT):
    """
    Plot multi-point - 2D.

    :param sh_multipoint: Shapely point object.
    :param data: List of plotly graph objects.  Graph is appended to this.
    :param style:  shapely_plotly Style object.  Overrides any style defined for sh_multipoint.
    :param name:   Name for the object in Plotly plot.  Overrides any name defined for the sh_multipoint.
    :param legend_group   Legend group to use (groups multiple items under a single legend).  Overrides style.
    """

    points = sh_multipoint.geoms
    xs = [p.x for p in points]
    ys = [p.y for p in points]

    style, name, show_legend, legend_group = resolve_info(sh_multipoint, style, name, legend_group)
    assert style.point_style is not None

    scat = graph.Scatter(x=xs, y=ys,
                         marker=style.point_style,
                         name=name, showlegend=show_legend, legendgroup=legend_group,
                         mode="markers",
                         **style.scatter_kwargs)
    data.append(scat)
    return


sh.MultiPoint.plotly_draw2d = plot_multipoint2d


def __i_plot_lines_style_info(geom, style, name, legend_group, as_hole):
    """
    Internal function.  Get the line style info for a geometry object, based on
    parameters passed into a draw command, and style/name set for the object.

    Returns: mode, line_style, marker_style, name, show_legend, Style object
    """
    style, name, show_legend, legend_group = resolve_info(geom, style, name, legend_group)

    if as_hole:
        line_style = style.hole_line_style
        marker_style = style.hole_vertex_style
    else:
        line_style = style.line_style
        marker_style = style.vertex_style

    if line_style is None:
        if marker_style is None:
            # Invisible
            mode = None
        else:
            mode = "markers"
    else:
        if marker_style is None:
            mode = "lines"
        else:
            mode = "lines+markers"

    return mode, line_style, marker_style, name, show_legend, legend_group, style


def __i_plot_lines3d(geom, xs, ys, zs, data, style, name, show_legend, legend_group, as_hole):
    """
    Internal function.  Get style for lines and plot them, 3D.
    """
    if len(xs) == 0:
        # Empty line
        return

    mode, line_style, marker_style, name, n_show_legend, legend_group, style = \
        __i_plot_lines_style_info(geom, style, name, legend_group, as_hole)

    # The show legend parameter above will force the legend entry off.
    # Only show a legend if both that flag and the style and the name say it should be shown.
    show_legend = show_legend and n_show_legend
    if mode is None:
        # Invisible
        return

    scat = graph.Scatter3d(x=xs, y=ys, z=zs,
                           line=line_style,
                           marker=marker_style,
                           name=name, showlegend=show_legend, legendgroup=legend_group,
                           mode=mode,
                           **style.scatter_kwargs)
    data.append(scat)
    return


def __i_plot_lines2d(geom, xs, ys, data, style, name, legend_group, as_hole):
    """
    Internal function.  Get style for lines and plot them, 2D.
    """
    if len(xs) == 0:
        # Empty line
        return

    mode, line_style, marker_style, name, show_legend, legend_group, style = \
        __i_plot_lines_style_info(geom, style, name, legend_group, as_hole)

    if mode is None:
        # Invisible
        return

    scat = graph.Scatter(x=xs, y=ys,
                         line=line_style,
                         marker=marker_style,
                         name=name, showlegend=show_legend, legendgroup=legend_group,
                         mode=mode,
                         **style.scatter_kwargs)
    data.append(scat)
    return


def plot_line_string3d(sh_line_string, data, style=DEFAULT,
                       name=DEFAULT, show_legend=True, legend_group=DEFAULT):
    """
    Plot line String/Ring - 3D.

    :param sh_line_string: Shapely point object.
    :param data: List of plotly graph objects.  Graph is appended to this.
    :param style:  shapely_plotly Style object.  Overrides any style defined for sh_line_string.
    :param name:   Name for the object in Plotly plot.  Overrides any name defined for the sh_line_string.
    :param legend_group   Legend group to use (groups multiple items under a single legend).  Overrides style.
    """
    __i_plot_line_string3d(sh_line_string, data, style,
                           name, True, legend_group, as_hole=False)


# shapely LineString
def __i_plot_line_string3d(sh_line_string, data, style,
                           name, show_legend, legend_group, as_hole):
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

    __i_plot_lines3d(sh_line_string, xs, ys, zs, data, style, name, show_legend, legend_group, as_hole)
    return


sh.LineString.plotly_draw3d = plot_line_string3d


def plot_line_string2d(sh_line_string, data, style=DEFAULT, name=DEFAULT, legend_group=DEFAULT, as_hole=False):
    """
    Plot line String/Ring - 2D.

    :param sh_line_string: Shapely point object.
    :param data: List of plotly graph objects.  Graph is appended to this.
    :param style:  shapely_plotly Style object.  Overrides any style defined for sh_line_string.
    :param name:   Name for the object in Plotly plot.  Overrides any name defined for the sh_line_string.
    :param legend_group   Legend group to use (groups multiple items under a single legend).  Overrides style.
    """
    coords = sh_line_string.coords
    n = len(coords)
    xs, ys = sh_line_string.xy
    xs = list(xs)
    ys = list(ys)

    __i_plot_lines2d(sh_line_string, xs, ys, data, style, name, legend_group, as_hole)
    return


sh.LineString.plotly_draw2d = plot_line_string2d

# shapely LinearRing
# - We can use the same drawing function as line string, because shapely duplicates the start coord at the end.
sh.LinearRing.plotly_draw3d = plot_line_string3d


# shapely Polygon
def plot_polygon3d(sh_polygon, data, style=DEFAULT, name=DEFAULT, legend_group=DEFAULT):
    """
    Plot Polygon - 3D.

    :param sh_polygon: Shapely point object.
    :param data: List of plotly graph objects.  Graph is appended to this.
    :param style:  shapely_plotly Style object.  Overrides any style defined for sh_polygon.
    :param name:   Name for the object in Plotly plot.  Overrides any name defined for the sh_polygon.
    :param legend_group   Legend group to use (groups multiple items under a single legend).  Overrides style.
    """

    _, _, _, name, show_legend, legend_group, style = \
        __i_plot_lines_style_info(sh_polygon, style, name, legend_group, as_hole=False)

    # If the legend is shown and has the polygon hasinteriors, then force all plots onto the same legend group.
    # If one wasn't defined, then create a unique one.
    # create a unique one.
    if show_legend and (len(sh_polygon.interiors) > 0):
        if legend_group is None:
            legend_group = unique_legend_group()

    # Plot the exterior hull
    # FIXME: Misformed polygons?  Empty polygons?  Empty exterior with holes?
    __i_plot_line_string3d(sh_polygon.exterior, data, style, name, True, legend_group, False)

    # Plot the interior holes.  No name on these so no legend entry.
    # FIXME: Tool tips not right, because no name.  Need explicit show-legend to this call.
    for interior in sh_polygon.interiors:
        __i_plot_line_string3d(interior, data, style, name, False, legend_group, True)

    return


sh.Polygon.plotly_draw3d = plot_polygon3d


def plot_polygon2d(sh_polygon, data, style=DEFAULT, name=DEFAULT, legend_group=DEFAULT):
    """
    Plot Polygon - 2D.

    :param sh_polygon: Shapely point object.
    :param data: List of plotly graph objects.  Graph is appended to this.
    :param style:  shapely_plotly Style object.  Overrides any style defined for sh_polygon.
    :param name:   Name for the object in Plotly plot.  Overrides any name defined for the sh_polygon.
    :param legend_group   Legend group to use (groups multiple items under a single legend).  Overrides style.
    """

    mode, line_style, marker_style, name, show_legend, legend_group, style = \
        __i_plot_lines_style_info(sh_polygon, style, name, legend_group, as_hole=False)

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
            if legend_group is None:
                legend_group = unique_legend_group()

        # Hole styles
        h_mode, h_line_style, h_marker_style, _, _, _, _ = \
            __i_plot_lines_style_info(sh_polygon, style, name, legend_group, as_hole=True)

        # Save exterior styles for exterior plot.
        e_mode, e_line_style = mode, line_style

        # Substitue empty line plot for the main plot.
        mode = None

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

    fill_color = style.fill_color

    # We don't need this plot if neither the borders nor the fill are being drawn.
    need_fill_plot = (mode is not None) or (fill_color is not None)

    if need_fill_plot:
        if mode is None:
            # No lines or markers, only fill.
            mode = "lines"
            line_style = {"color": "rgba(0,0,0,0)", "width": 0}  # Invisible lines for fill plot.

        # Fill color == None means no fill.
        if fill_color is None:
            fill_mode = None
        else:
            fill_mode = "toself"

        # Plot with fill
        scat = graph.Scatter(x=xs, y=ys,
                             line=line_style,
                             marker=marker_style,
                             fillcolor=style.fill_color,
                             name=name, showlegend=show_legend, legendgroup=legend_group,
                             mode=mode, fill="toself",
                             **style.scatter_kwargs)

        data.append(scat)

        # Only need the above legend entry
        h_show_legend = False
        e_show_legend = False
    else:
        if h_mode is None:
            # Use exterior to draw legend.
            # h_show_legend is not used.
            e_show_legend = show_legend
        else:
            # Use holes to draw legend.
            h_show_legend = show_legend
            e_show_legend = False

    if has_interiors:
        # Plot exterior lines and markers.
        if e_mode is not None:
            scat = graph.Scatter(x=xs[0:ext_n], y=ys[0:ext_n],
                                 line=e_line_style,
                                 marker=marker_style,
                                 name=name, showlegend=h_show_legend, legendgroup=legend_group,
                                 mode=e_mode,
                                 **style.scatter_kwargs
                                 )
            data.append(scat)

        # Plot holes lines and markers.
        if h_mode is not None:
            scat = graph.Scatter(x=xs[ext_n + 1:], y=ys[ext_n + 1:],
                                 line=h_line_style,
                                 marker=h_marker_style,
                                 name=name, showlegend=e_show_legend, legendgroup=legend_group,
                                 mode=h_mode,
                                 **style.scatter_kwargs
                                 )
            data.append(scat)

    return data


sh.Polygon.plotly_draw2d = plot_polygon2d


def plot_multiline3d(sh_multiline, data, style=DEFAULT, name=DEFAULT, legend_group=DEFAULT):
    """
    Plot Multi-line string - 3D.

    :param sh_multiline: Shapely point object.
    :param data: List of plotly graph objects.  Graph is appended to this.
    :param style:  shapely_plotly Style object.  Overrides any style defined for sh_multiline.
    :param name:   Name for the object in Plotly plot.  Overrides any name defined for the sh_multiline.
    :param legend_group   Legend group to use (groups multiple items under a single legend).  Overrides style.

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

    __i_plot_lines3d(sh_multiline, xs, ys, zs, data, style, name, True, legend_group, as_hole=False)
    return


sh.MultiLineString.plotly_draw3d = plot_multiline3d


def plot_multiline2d(sh_multiline, data, style=DEFAULT, name=DEFAULT, legend_group=DEFAULT):
    """
    Plot Multi-line string - 2D.

    :param sh_multiline: Shapely point object.
    :param data: List of plotly graph objects.  Graph is appended to this.
    :param style:  shapely_plotly Style object.  Overrides any style defined for sh_multiline.
    :param name:   Name for the object in Plotly plot.  Overrides any name defined for the sh_multiline.
    :param legend_group   Legend group to use (groups multiple items under a single legend).  Overrides style.

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

    __i_plot_lines2d(sh_multiline, xs, ys, data, style, name, legend_group, as_hole=False)
    return


sh.MultiLineString.plotly_draw2d = plot_multiline2d


# shapely GeometryCollection
def plot_geometry_collection3d(sh_geo_col, data, style=DEFAULT, name=DEFAULT, legend_group=DEFAULT):
    """
    Plot geometry collection - 3D.

    :param sh_geo_col: Shapely point object.
    :param data: List of plotly graph objects.  Graph is appended to this.
    :param style:  shapely_plotly Style object.  Overrides any style defined for sh_geo_col.
    :param name:   Name for the object in Plotly plot.  Overrides any name defined for the sh_geo_col.
    :param legend_group   Legend group to use (groups multiple items under a single legend).  Overrides style.

    Note: Unless defined above, the names and styles of the contained geometry objects are used.
    Any name/style defined for the Geometry Collection itself is ignored.
    """
    geoms = tuple(sh_geo_col.geoms)

    if len(geoms) == 0:
        # Nothing to plot.
        return

    # Get style controls for this object.
    style, name, _, legend_group = resolve_info(sh_geo_col, style, name, legend_group)

    # Get unique legend group ID
    if legend_group is None:
        legend_group = unique_legend_group()

    for g in geoms:
        g.plotly_draw3d(data, style, name, legend_group)
        name = None  # Only the first geometry should have a name, and therefore generate a legend entry.

    return


sh.GeometryCollection.plotly_draw3d = plot_geometry_collection3d

# shapely MultiPolygon
# We use the same approach for multi-polygone.
sh.MultiPolygon.plotly_draw3d = plot_geometry_collection3d


def plot_geometry_collection2d(sh_geo_col, data, style=DEFAULT, name=DEFAULT, legend_group=DEFAULT):
    """
    Plot geometry collection - 2D.

    :param sh_geo_col: Shapely point object.
    :param data: List of plotly graph objects.  Graph is appended to this.
    :param style:  shapely_plotly Style object.  Overrides any style defined for sh_geo_col.
    :param name:   Name for the object in Plotly plot.  Overrides any name defined for the sh_geo_col.
    :param legend_group   Legend group to use (groups multiple items under a single legend).  Overrides style.
    """
    geoms = tuple(sh_geo_col.geoms)

    if len(geoms) == 0:
        # Nothing to plot.
        return

    # Get style controls for this object.
    style, name, _, legend_group = resolve_info(sh_geo_col, style, name, legend_group)

    # Get unique legend group ID
    if legend_group is None:
        legend_group = unique_legend_group()

    # Single legend and use this style.
    for g in geoms:
        g.plotly_draw2d(data, style, name, legend_group)
        name = None  # Only the first geometry should have a name, and therefore generate a legend entry.

    return


sh.GeometryCollection.plotly_draw2d = plot_geometry_collection2d

# shapely MultiPolygon
# We use the same approach for multi-polygone.
sh.MultiPolygon.plotly_draw2d = plot_geometry_collection2d


def show2d(data, show=True):
    """
    Create figure and show.  Suitable for viewing 2D plots.
    """
    fig = graph.Figure(data=data)
    fig.update_yaxes(scaleanchor="x", scaleratio=1)  # This forces plotly to keep the aspect ratio correct.

    if show:
        fig.show()

    return fig


def show3d(data, show=True):
    """
    Create figure and show.  Suitable for viewing 3D plots.
    """
    scene = dict(
        aspectmode="data",  # this string can be 'data', 'cube', 'auto', 'manual'
        aspectratio=dict(x=1, y=1, z=1)
    )

    layout = graph.Layout(
        scene=dict(
            aspectmode="data",  # this string can be 'data', 'cube', 'auto', 'manual'
            aspectratio=dict(x=1, y=1, z=1)
        )
    )
    fig = graph.Figure(data=data, layout=layout)

    if show:
        fig.show()

    return fig
