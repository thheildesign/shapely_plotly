import random as rnd
from math import pi, sin, cos
import shapely as shp
from shapely_plotly.tests.utils.utils import rnd_style
import shapely_plotly as shpl


# -----------------------------------------------------------------
# Random coordinates
# -----------------------------------------------------------------


def rnd_coord(xoff, yoff, width=1.0, height=None):
    if height is None:
        height = width

    x = rnd.uniform(xoff, xoff + width)
    y = rnd.uniform(yoff, yoff + height)

    return x, y


def rnd_coords(xoff, yoff, width=1.0, height=None):
    if height is None:
        height = width

    l = rnd.randrange(10, 20)
    x = [rnd.uniform(xoff, xoff + width) for i in range(l)]
    y = [rnd.uniform(yoff, yoff + height) for i in range(l)]

    return x, y


def zip_xy(x, y):
    z = list(zip(x, y))
    return z


def fixed_rect_coords(xoff, yoff, width, height):
    x0 = xoff
    x1 = xoff + width
    y0 = yoff
    y1 = yoff + height
    x = [x0, x0, x1, x1]
    y = [y0, y1, y1, y0]

    x, y = complete_poly_coords(x, y)

    return x, y


def rnd_rect_coords(xoff, yoff, max_width=1.0, max_height=None):
    if max_height is None:
        max_height = max_width

    width = rnd.uniform(max_width * 0.5, max_width)
    height = rnd.uniform(max_height * 0.5, max_height)

    xoff = rnd.uniform(xoff, xoff + max_width - width)
    yoff = rnd.uniform(yoff, yoff + max_height - height)

    x, y = fixed_rect_coords(xoff, yoff, width, height)
    return x, y


def rnd_poly_coords(xoff, yoff, max_width=1.0, max_height=None):
    l = rnd.randrange(3, 20)

    if max_height is None:
        max_height = max_width

    while True:
        angles = [rnd.uniform(0, 2 * pi) for i in range(l)]
        angles.sort()

        fail = False
        for i in range(0, len(angles) - 1):
            if angles[i] == angles[i + 1]:
                fail = True
                break
        if not fail:
            break

    xs = []
    ys = []

    for a in angles:
        dx = cos(a)
        dy = sin(a)
        if abs(dx) > abs(dy):
            scale = 1.0 / abs(dx)
        else:
            scale = 1.0 / abs(dy)

        l = rnd.uniform(0.3, 1.0)
        x = dx * scale * l
        y = dy * scale * l

        x = (x + 1.0) * 0.5 * max_width + xoff
        y = (y + 1.0) * 0.5 * max_height + yoff
        xs.append(x)
        ys.append(y)

    xs, ys = complete_poly_coords(xs, ys)

    return xs, ys


def complete_poly_coords(x, y):
    """
    Randomly flip CW / CCW.
    Rotate to a random starting point.
    Add return to start coordinate.
    """
    if rnd.uniform(0.0, 1.0) < 0.5:
        # Flip to counter clockwise
        x.reverse()
        y.reverse()

    s = rnd.randrange(0, len(x))
    if s > 0:
        # Rotate to new starting point
        x = x[s:] + x[:s]
        y = y[s:] + y[:s]

    # Add return to start
    x.append(x[0])
    y.append(y[0])

    return x, y


# -----------------------------------------------------------------
# Random Shapely geometries
# -----------------------------------------------------------------


def rnd_shapely_point2d(expect_data, xoff, yoff, width=1.0, height=None):
    x, y = rnd_coord(xoff, yoff, width, height)
    p = shp.Point(x, y)
    expect_data["dims"] = "2d"
    expect_data["x"] = (x,)
    expect_data["y"] = (y,)
    return p


def rnd_shapely_multipoint2d(expect_data, xoff, yoff, width=1.0, height=None):
    x, y = rnd_coords(xoff, yoff, width, height)
    p = shp.MultiPoint(zip_xy(x, y))
    expect_data["dims"] = "2d"
    expect_data["x"] = tuple(x)
    expect_data["y"] = tuple(y)
    return p


def rnd_shapely_linestring(expect_data, xoff, yoff, width=1.0, height=None):
    x, y = rnd_coords(xoff, yoff, width, height)
    p = shp.LineString(zip_xy(x, y))
    expect_data["dims"] = "2d"
    expect_data["x"] = tuple(x)
    expect_data["y"] = tuple(y)
    return p


def rnd_shapely_multiline(expect_data, xoff, yoff, width=1.0, height=None):
    n = rnd.randrange(1, 5)
    xys = [None] * n
    ex, ey = [], []
    for i in range(n):
        x, y = rnd_coords(xoff + (width + 1) * i, yoff, width, height)
        xys[i] = zip_xy(x, y)
        if i > 0:
            ex.append(None)
            ey.append(None)
        ex.extend(x)
        ey.extend(y)
    expect_data["dims"] = "2d"
    expect_data["x"] = tuple(ex)
    expect_data["y"] = tuple(ey)

    p = shp.MultiLineString(xys)
    return p


def rnd_shapely_linering(expect_data, xoff, yoff, width=1.0, height=None):
    x, y = rnd_coords(xoff, yoff, width, height)
    p = shp.LinearRing(zip_xy(x, y))
    expect_data["dims"] = "2d"
    if (x[0] != x[-1]) or (y[0] != y[-1]):
        # Add closing point.
        expect_data["x"] = tuple(x) + (x[0],)
        expect_data["y"] = tuple(y) + (y[0],)
    else:
        # Already closed
        expect_data["x"] = tuple(x)
        expect_data["y"] = tuple(y)

    return p


def rnd_shapely_poly_simple(expect_data, xoff, yoff, width=1.0, height=None):
    if rnd.uniform(0.0, 1.0) < 0.2:
        x, y = rnd_rect_coords(xoff, yoff, width, height)
    else:
        x, y = rnd_poly_coords(xoff, yoff, width, height)

    p = shp.Polygon(shell=zip_xy(x, y))
    expect_data["dims"] = "2d"
    if (x[0] != x[-1]) or (y[0] != y[-1]):
        # Add closing point.
        expect_data["x"] = tuple(x) + (x[0],)
        expect_data["y"] = tuple(y) + (y[0],)
    else:
        # Already closed
        expect_data["x"] = tuple(x)
        expect_data["y"] = tuple(y)
    return p


def rnd_shapely_poly_complex(xoff, yoff, width=1.0, height=None):
    if height is None:
        height = width

    # Generate the hull
    while True:
        ext_x, ext_y = rnd_poly_coords(xoff, yoff, width, height)
        ext_xy = zip_xy(ext_x, ext_y)
        shell_p = shp.Polygon(shell=ext_xy)
        if shell_p.is_valid:
            break

    num_int = rnd.randrange(0, 10)
    if num_int > 0:
        # Build a list of hole positions.
        hoffsets = []
        for hx in range(3):
            hxoff = xoff + hx * width * 0.3 + width * 0.1
            for hy in range(3):
                hyoff = yoff + hy * height * 0.3 + height * 0.1
                hoffsets.append((hxoff, hyoff))

        # Scramble it.
        rnd.shuffle(hoffsets)

        holes = []
        for (hx, hy) in hoffsets[:num_int]:
            hole_x, hole_y = rnd_poly_coords(hx, hy, width * 0.2, height * 0.2)
            hole_p = shp.Polygon(shell=zip_xy(hole_x, hole_y))
            if not hole_p.is_valid:
                # Bad hole. skip.
                continue

            if not shell_p.contains(hole_p):
                # Hole not contained.
                continue

            holes.append(zip_xy(hole_x, hole_y))

        if len(holes) > 0:
            shell_p = shp.Polygon(shell=ext_xy, holes=holes)
            # assert shell_p.is_valid

    return shell_p


def rnd_shapely_geom_collection(expect_data_list, max_depth, xoff, yoff, width=1.0, height=None):
    n = rnd.randrange(1, 5)
    geoms = []

    if max_depth > 0:
        funcs = rnd_shapely_funcs
    else:
        # Exclude geometry collection
        funcs = rnd_shapely_funcs[:-1]

    for i in range(n):
        rnd_shapely_f = rnd.choice(funcs)
        if rnd_shapely_f is rnd_shapely_poly_complex:
            geom = rnd_shapely_poly_complex(xoff, yoff, width, height)
            geoms.append(geom)
            expect_data_list.append([]) # Fill in expected data later
        elif rnd_shapely_f is rnd_shapely_geom_collection:
            expect_data_sub_list = []
            geom = rnd_shapely_geom_collection(expect_data_sub_list, max_depth-1, xoff, yoff, width, height)
            expect_data_list.append(expect_data_sub_list) # Fill in expected data later
            geoms.append(geom)
        else:
            # Everything else works the same.
            expect_data = {}
            geom = rnd_shapely_f(expect_data, xoff, yoff, width, height)
            geoms.append(geom)
            expect_data_list.append(expect_data)

    geom_coll = shp.GeometryCollection(geoms)
    return geom_coll

# List of geometry building functions.  Used by the above.
rnd_shapely_funcs = [
    rnd_shapely_point2d,
    rnd_shapely_multipoint2d,
    rnd_shapely_linestring,
    rnd_shapely_multiline,
    rnd_shapely_linering,
    rnd_shapely_poly_simple,
    rnd_shapely_poly_complex,
    rnd_shapely_geom_collection
]

# -----------------------------------------------------------------
# Random geometry plotting functions - 2D
# -----------------------------------------------------------------


def rnd_generic_plot2d(plot_data, xoff, yoff, width, height, rnd_shapely_f, style_mode):
    """
    Generic random create and plot function for most geometry types.
    """
    expect_data = {}
    p = rnd_shapely_f(expect_data, xoff, yoff, width, height)
    rnd_plot2d(p, expect_data, plot_data, style_mode)
    return expect_data


def rnd_point_plot2d(plot_data, xoff, yoff, width=1.0, height=None):
    return rnd_generic_plot2d(plot_data, xoff,yoff, width, height, rnd_shapely_point2d, "point")


def rnd_multipoint_plot2d(plot_data, xoff, yoff, width=1.0, height=None):
    return rnd_generic_plot2d(plot_data, xoff,yoff, width, height, rnd_shapely_multipoint2d, "point")


def rnd_linestring_plot2d(plot_data, xoff, yoff, width=1.0, height=None):
    return rnd_generic_plot2d(plot_data, xoff,yoff, width, height, rnd_shapely_linestring, "line")


def rnd_multiline_plot2d(plot_data, xoff, yoff, width=1.0, height=None):
    return rnd_generic_plot2d(plot_data, xoff,yoff, width, height, rnd_shapely_multiline, "line")


def rnd_linering_plot2d(plot_data, xoff, yoff, width=1.0, height=None):
    return rnd_generic_plot2d(plot_data, xoff,yoff, width, height, rnd_shapely_linering, "line")


def rnd_poly_simple_plot2d(plot_data, xoff, yoff, width=1.0, height=None):
    return rnd_generic_plot2d(plot_data, xoff,yoff, width, height, rnd_shapely_poly_simple, "poly")


def rnd_poly_complex_plot2d(expect_data_list, plot_data, xoff, yoff, width=1.0, height=None):
    p = rnd_shapely_poly_complex(xoff, yoff, width, height)
    rnd_poly_plot2d(p, expect_data_list, plot_data)
    return


def rnd_multipoly_plot2d(expect_data_list, plot_data, xoff, yoff, width=1.0, height=None):
    if height is None:
        height = width

    n = rnd.randrange(1, 6)
    if n > 3:
        pheight = height * 0.45
        ystep = height * 0.55
        nx = (n + 1) // 2
    else:
        nx = n
        pheight = height
        ystep = 0.0

    pwidth = (1.0 - 0.1 * (nx - 1)) / nx
    xstep = pwidth + 0.1
    pwidth *= width
    xstep *= width

    geoms = []
    xpoff = xoff
    ypoff = yoff
    for i in range(n):
        poly = rnd_shapely_poly_complex(xpoff, ypoff, pwidth, pheight)
        geoms.append(poly)
        if i == (nx - 1):
            xpoff = xoff
            ypoff += ystep
        else:
            xpoff += xstep

    p = shp.MultiPolygon(geoms)

    data_start = len(plot_data)
    assert data_start == len(expect_data_list)

    pd_before = data_start
    # First we just plot the polygon collection, and get the style used.
    final_style = rnd_style_plot2d(p, plot_data, "poly")
    data_end = len(plot_data)

    # Build expected style data for all the plots.  All use the same final_style
    for poly in p.geoms:
        num_plot = add_normalized_poly_style_info(poly, expect_data_list, final_style, plot_data, pd_before)
        pd_before += num_plot

    assert pd_before == data_end  # Number of plots created and expected should be consistent.
    assert data_end == len(expect_data_list)

    # MultiPoly plots use a legend group to tie all poly's to the same legend entry.  We capture this from
    # the first plot in the series, and insist all plots use the same legend group.
    legend_group = plot_data[data_start].legendgroup
    for expect_data in expect_data_list[data_start:data_end]:
        expect_data["legendgroup"] = legend_group

    return p


def rnd_geometry_collection_plot2d(expect_data_list, plot_data, xoff, yoff, width=1.0, height=None):

    # We first build expected data into a local list.
    # This is because some cases have to be unrolled.
    geom_expect_data_list = []

    pd_before = len(plot_data)

    # Build the collection.
    geom_coll = rnd_shapely_geom_collection(geom_expect_data_list, 2, xoff, yoff, width, height)

    # Plot the collection.
    final_style = rnd_style_plot2d(geom_coll, plot_data, "collection")

    # Now we go and fill in the expected data for all the elements.
    add_normalized_collection_style_info(geom_coll, geom_expect_data_list, expect_data_list,
                                         final_style, plot_data, pd_before)

    if final_style.legend_group is None:
        # Had to create a random legend group.  Must copy across all the expected data.
        legend_group = plot_data[pd_before].legendgroup
        for expect_data in expect_data_list[pd_before:]:
            expect_data["legendgroup"] = legend_group

    return geom_coll

# -----------------------------------------------------------------
# Random plotting helper functions - 2D
# -----------------------------------------------------------------


def rnd_plot2d(geom, expect_data, plot_data, style_mode):
    """
    Randomly plot-2D a geometry object, applying a random style in one of four ways.

    with_fill - Whether the geometry needs a fill color.
    """

    final_style = rnd_style_plot2d(geom, plot_data, style_mode)
    add_normalized_style_info(expect_data, final_style, style_mode)
    return


def rnd_poly_plot2d(geom, expect_data_list, plot_data):
    """
    rnd_plot2d for polygons.  Polygons may create 1 to 3 plots depending on their needs.
    This function handles special cases for them.

    geom - The polygon to plot.
    expect_data_list - A list of expect_data.  It will be appended to.
    plot_data - Plot data.  Appended to.
    """

    pd_before = len(plot_data)
    # First we just plot the polygon.
    final_style = rnd_style_plot2d(geom, plot_data, "poly")
    pd_after = len(plot_data)
    num_plot = pd_after - pd_before
    assert num_plot >= 1
    assert num_plot <= 3

    add_normalized_poly_style_info(geom, expect_data_list, final_style, plot_data, pd_before, num_plot=num_plot)
    return


# Style_mode decoder map.
# Functions to grab 0) Line style, 1) marker style, 2) fill color, 3) with_fill
style_usage_map = {
    "point": (lambda s: None, lambda s: s.point_style, lambda s: None, False),
    "line": (lambda s: s.line_style, lambda s: s.vertex_style, lambda s: None, False),
    "hole": (lambda s: s.hole_line_style, lambda s: s.hole_vertex_style, lambda s: None, False),
    "poly": (lambda s: s.line_style, lambda s: s.vertex_style, lambda s: s.fill_color, True),
    "poly_fill": (lambda s: None, lambda s: None, lambda s: s.fill_color, True),
    "collection": (lambda s: s.line_style, lambda s: s.vertex_style, lambda s: s.fill_color, False),
}


def rnd_style_plot2d(geom, plot_data, style_mode):
    """
    Randomly plot-2D a geometry object, applying a random style in one of four ways.

    style_mode - What kind of style the object needs.  See style_usage_map map above.

    Returns: final_style - The random style used during plotting.
    """

    with_fill = style_usage_map[style_mode][3]

    # Four methods of applying a style:
    # a) Applied to object ahead of time.
    # c) Given to the draw call.
    # n) No style at all (default_style)
    # o) An ignored style set a head of time, overlaid by the actual style at call time.
    method = rnd.choice("acno")

    if method == "a":
        # a) Applied to object ahead of time.
        s = rnd_style(with_fill)
        geom.plotly_set_style(s)
        draw_style = shpl.DEFAULT
        final_style = s
    elif method == "c":
        # c) Given to the draw call.
        draw_style = rnd_style(with_fill)
        final_style = draw_style
    elif method == "n":
        # n) No style at all (default_style)
        draw_style = shpl.DEFAULT
        final_style = shpl.default_style
    elif method == "o":
        # o) An ignored style set a head of time, overlaid by the actual style at call time.
        s = rnd_style(with_fill)
        geom.plotly_set_style(s)
        draw_style = rnd_style(with_fill)
        final_style = draw_style

    geom.plotly_draw2d(plot_data, style=draw_style)

    return final_style


def add_normalized_poly_style_info(geom, expect_data_list, final_style, plot_data, pd_before, num_plot=None):
    """
    Add expected data to expect_data_list for the 1 to 3 plots created by drawing a polygon (geom).
    Unlike other geometries, polygons do not set dims and x/y as geometry creation time.
    For polygons, those values are complex and we wait until after the plots are made to create them.
    """
    if len(geom.interiors) > 0:
        # Has interioriors.  We have 1 to 3 plots.
        total_plots = 0

        # 1) Fill plot:
        if final_style.fill_color is not None:
            # For x,y I'm just going to take the polygon's x/ys for expected values.
            # This is a non-test.  I could rebuild the x/y lists, but it would just be repeating the
            # same code already in the polygon plot function.
            fill_plot_data = plot_data[pd_before]
            expect_data = {
                "dims": "2d",
                "x": tuple(fill_plot_data.x),
                "y": tuple(fill_plot_data.y)
            }

            assert len(fill_plot_data.x) == \
                   len(geom.exterior.xy[0]) + len(geom.interiors) + sum(len(i.xy[0]) for i in geom.interiors)

            add_normalized_style_info(expect_data, final_style, "poly_fill")
            expect_data_list.append(expect_data)
            total_plots += 1

        # 2) Exterior plot.
        if (final_style.line_style is not None) or (final_style.vertex_style is not None):
            ext = geom.exterior
            ext_x, ext_y = ext.xy
            expect_data = {
                "dims": "2d",
                "x": tuple(ext_x),
                "y": tuple(ext_y)
            }
            add_normalized_style_info(expect_data, final_style, "line")
            expect_data_list.append(expect_data)
            total_plots += 1

        # 3) Interiors plot.
        if (final_style.hole_line_style is not None) or (final_style.hole_vertex_style is not None):
            # Again, we just take the plot's xy coordinates.
            hole_plot_data = plot_data[pd_before + total_plots]
            expect_data = {
                "dims": "2d",
                "x": tuple(hole_plot_data.x),
                "y": tuple(hole_plot_data.y)
            }
            assert len(hole_plot_data.x) == \
                   len(geom.interiors) + sum(len(i.xy[0]) for i in geom.interiors) - 1

            add_normalized_style_info(expect_data, final_style, "hole")
            expect_data_list.append(expect_data)
            total_plots += 1

        assert (num_plot is None) or (num_plot == total_plots)

    else:
        # No interiors.  Just the one plot, and we can build just a single expected value like normal.
        assert (num_plot is None) or (num_plot == 1)
        expect_data = {
            "dims": "2d",
            "x": tuple(c[0] for c in geom.exterior.coords),
            "y": tuple(c[1] for c in geom.exterior.coords)
        }
        add_normalized_style_info(expect_data, final_style, "poly")
        expect_data_list.append(expect_data)
        total_plots = 1

    return total_plots

add_norm_map = {
    shp.Polygon: None, # Nonstandard.  Use add_normalized_poly_style_info,
    shp.MultiPolygon: None, # Nonstandard
    shp.GeometryCollection: None, # Nonstandard


}


style_mode_map = {
    shp.Point: "point",
    shp.MultiPoint: "point",
    shp.LineString: "line",
    shp.LinearRing: "line",
    shp.MultiLineString: "line"
}


def add_normalized_collection_style_info(geom_coll, geom_expect_data_list, expect_data_list, final_style,
                                         plot_data, plot_data_i):
    assert len(geom_coll.geoms) == len(geom_expect_data_list)

    for geom_i, geom in enumerate(geom_coll.geoms):
        expect_data = geom_expect_data_list[geom_i]
        geom_t = type(geom)

        if geom_t is shp.Polygon:
            num_plot = add_normalized_poly_style_info(geom, expect_data_list, final_style, plot_data, plot_data_i)
            plot_data_i += num_plot

        elif geom_t is shp.MultiPolygon:
            # Build expected style data for all the plots.  All use the same final_style
            for poly in geom.geoms:
                num_plot = add_normalized_poly_style_info(poly, expect_data_list, final_style, plot_data, plot_data_i)
                plot_data_i += num_plot

        elif geom_t is shp.GeometryCollection:
            plot_data_i = add_normalized_collection_style_info(geom, expect_data, expect_data_list, final_style,
                                                               plot_data, plot_data_i)

        else:
            # All other geometries are handled the same
            style_mode = style_mode_map[geom_t]
            add_normalized_style_info(expect_data, final_style, style_mode)
            expect_data_list.append(expect_data)
            plot_data_i += 1

    return plot_data_i


expected_no_line_style = {"color": "rgba(0,0,0,0)", "width": 0, "dash": None}


def add_normalized_style_info(expect_data, style, style_mode):
    """
    Add style info to the expected data, given the style itself, and the style_mode.
    """

    # Extract the appropriate style settings from the Style object.
    line_style, marker_style, fill_color = (f(style) for f in style_usage_map[style_mode][0:3])

    expect_data["fillcolor"] = fill_color
    if fill_color is None:
        expect_data["fill"] = None
    else:
        expect_data["fill"] = "toself"

    scatter_kwargs = style.scatter_kwargs
    if scatter_kwargs is None:
        expect_data["hovertext"] = None
    else:
        expect_data["hovertext"] = scatter_kwargs.get("hovertext", None)

    if "mode" in expect_data:
        mode = expect_data["mode"]
        has_lines = "lines" in mode
        has_markers = "markers" in mode
    else:
        has_lines = True
        has_markers = True

    if (line_style is not None) and (has_lines):
        expect_data["line"] = {
            "dash": None,  # FIXME
            "color": line_style["color"],
            "width": line_style["width"]
        }
    else:
        expect_data["line"] = None

    if (marker_style is not None) and (has_markers):
        expect_data["marker"] = {
            "color": marker_style["color"],
            "size": marker_style["size"],
            "symbol": marker_style["symbol"],
            "line": {"color": None, "width": None}
        }
    else:
        expect_data["marker"] = None

    # FIXME: TBD
    expect_data["legendgroup"] = style.legend_group
    expect_data["name"] = None
    expect_data["showlegend"] = False

    if "mode" not in expect_data:
        has_lines = line_style is not None
        has_markers = marker_style is not None
        if has_lines:
            if has_markers:
                mode = "lines+markers"
            else:
                mode = "lines"
        else:
            if has_markers:
                mode = "markers"
            else:
                # No lines or markers, so must have a fill.
                assert fill_color is not None, "Style should have lines, markers or a fill color"
                # In this case, what we do is lines mode, and then have no line.
                mode = "lines"
                expect_data["line"] = expected_no_line_style
        expect_data["mode"] = mode
