import random as rnd
from math import pi, sin, cos
import shapely as shp
from shapely_plotly.tests.utils.utils import rnd_style
import shapely_plotly as shpl


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


def rnd_rect_coords(xoff, yoff, max_width=1.0, max_height=None):
    if max_height is None:
        max_height = max_width

    width = rnd.uniform(max_width * 0.5, max_width)
    height = rnd.uniform(max_height * 0.5, max_height)

    x0 = xoff
    x1 = xoff + width
    y0 = yoff
    y1 = yoff + height
    x = [x0, x0, x1, x1]
    y = [y0, y1, y1, y0]

    x, y = complete_poly_coords(x, y)

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


def rnd_shapely_point2d(expect_data, xoff, yoff, width=1.0, height=None):
    x, y = rnd_coord(xoff, yoff, width, height)
    p = shp.Point(x, y)
    expect_data["dims"] = "2d"
    expect_data["x"] = (x,)
    expect_data["y"] = (y,)
    return p


def rnd_point_plot2d(plot_data, xoff, yoff, width=1.0, height=None):
    expect_data = {}
    p = rnd_shapely_point2d(expect_data, xoff, yoff, width, height)
    rnd_plot2d(p, expect_data, plot_data, "point")
    return expect_data


def rnd_shapely_multipoint2d(expect_data, xoff, yoff, width=1.0, height=None):
    x, y = rnd_coords(xoff, yoff, width, height)
    p = shp.MultiPoint(zip_xy(x, y))
    expect_data["dims"] = "2d"
    expect_data["x"] = tuple(x)
    expect_data["y"] = tuple(y)
    return p


def rnd_multipoint_plot2d(plot_data, xoff, yoff, width=1.0, height=None):
    expect_data = {}
    p = rnd_shapely_multipoint2d(expect_data, xoff, yoff, width, height)
    rnd_plot2d(p, expect_data, plot_data, "point")
    return expect_data


def rnd_shapely_linestring(expect_data, xoff, yoff, width=1.0, height=None):
    x, y = rnd_coords(xoff, yoff, width, height)
    p = shp.LineString(zip_xy(x, y))
    expect_data["dims"] = "2d"
    expect_data["x"] = tuple(x)
    expect_data["y"] = tuple(y)
    return p


def rnd_linestring_plot2d(plot_data, xoff, yoff, width=1.0, height=None):
    expect_data = {}
    p = rnd_shapely_linestring(expect_data, xoff, yoff, width, height)
    rnd_plot2d(p, expect_data, plot_data, "line")
    return expect_data


def rnd_shapely_multiline(expect_data, xoff, yoff, width=1.0, height=None):
    n = rnd.randrange(1, 5)
    xys = [None]*n
    ex, ey = [], []
    for i in range(n):
        x, y = rnd_coords(xoff + (width+1)*i, yoff, width, height)
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


def rnd_multiline_plot2d(plot_data, xoff, yoff, width=1.0, height=None):
    expect_data = {}
    p = rnd_shapely_multiline(expect_data, xoff, yoff, width, height)
    rnd_plot2d(p, expect_data, plot_data, "line")
    return expect_data


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


def rnd_linering_plot2d(plot_data, xoff, yoff, width=1.0, height=None):
    expect_data = {}
    p = rnd_shapely_linering(expect_data, xoff, yoff, width, height)
    rnd_plot2d(p, expect_data, plot_data, "line")
    return expect_data


def rnd_shapely_poly_simple(expect_data, xoff, yoff, width=1.0, height=None):
    if rnd.uniform(0.0, 1.0) < 0.2:
        x,y = rnd_rect_coords(xoff, yoff, width, height)
    else:
        x,y = rnd_poly_coords(xoff, yoff, width, height)

    p = shp.Polygon(shell=zip_xy(x,y))
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


def rnd_poly_simple_plot2d(plot_data, xoff, yoff, width=1.0, height=None):
    expect_data = {}
    p = rnd_shapely_poly_simple(expect_data, xoff, yoff, width, height)
    rnd_plot2d(p, expect_data, plot_data, "poly")
    return expect_data


def rnd_plot2d(geom, expect_data, plot_data, style_mode):
    """
    Randomly plot-2D a geometry object, applying a random style in one of four ways.

    with_fill - Whether the geometry needs a fill color.
    """

    with_fill = style_usage[style_mode][3]

    # Four methods of applying a style:
    # a) Applied to object ahead of time.
    # c) Given to the draw call.
    # n) No style at all (default_style)
    # o) An ignored style set a head of time, overlaid by the actual style at call time.
    method = rnd.choice("acno")

    if method == "a":
        s = rnd_style(with_fill)
        geom.plotly_set_style(s)
        draw_style = shpl.DEFAULT
        final_style = s
    elif method == "c":
        draw_style = rnd_style(with_fill)
        final_style = draw_style
    elif method == "n":
        draw_style = shpl.DEFAULT
        final_style = shpl.default_style
    elif method == "o":
        s = rnd_style(with_fill)
        geom.plotly_set_style(s)
        draw_style = rnd_style(with_fill)
        final_style = draw_style

    geom.plotly_draw2d(plot_data, style=draw_style)

    add_normalized_style_info(expect_data, final_style, style_mode)
    return


# Functions to grab 0) Line style, 1) marker style, 2) fill color, 3) with_fill
style_usage = {
    "point": (lambda s: None, lambda s: s.point_style, lambda s: None, False),
    "line": (lambda s: s.line_style, lambda s: s.vertex_style, lambda s: None, False),
    "poly": (lambda s: s.line_style, lambda s: s.vertex_style, lambda s: s.fill_color, True)
}


def add_normalized_style_info(expect_data, style, style_mode):
    line_style, marker_style, fill_color = (f(style) for f in style_usage[style_mode][0:3])

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
        expect_data["line"] = {'color': None, 'width': None, 'dash': None}

    if (marker_style is not None) and (has_markers):
        expect_data["marker"] = {
            "color": marker_style["color"],
            "size": marker_style["size"],
            "symbol": marker_style["symbol"],
            "line": {"color": None, "width": None}
        }
    else:
        expect_data["marker"] = {'color': None, 'size': None, 'symbol': None, 'line': {'color': None, 'width': None}}

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
                assert fill_color is not None , "Style should have lines, markers or a fill color"
                # In this case, what we do is lines mode, and then have no line.
                mode = "lines"
        expect_data["mode"] = mode
