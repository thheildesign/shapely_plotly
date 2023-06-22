import random as rnd
from string import ascii_letters, digits, punctuation

import plotly.graph_objects as graph
import shapely_plotly as shpl

rnd_chars = ascii_letters + digits + punctuation

marker_symbols = [
    'circle', 'circle-open', 'cross', 'diamond', 'diamond-open', 'square', 'square-open', 'x'
]


def normalize_plot_data(plot_data):
    """
    Read Scatter plot plots and convert to dictionaries in a standard form
    """
    norm_data = [None] * len(plot_data)
    for i, plot_obj in enumerate(plot_data):
        norm_obj = normalize_plot_obj(plot_obj)
        norm_data[i] = norm_obj

    return norm_data


norm_fields_2d = [
    "fill",
    "fillcolor",
    "hovertext",
    "legendgroup",
    "mode",
    "name",
    "showlegend",
    "x",
    "y"
]


def normalize_plot_obj(plot_obj):
    """
    Normalize a Scatter/Scatter3d object.
    """
    d = {}
    if isinstance(plot_obj, graph.Scatter):
        d["dims"] = "2d"
        is_3d = False
        norm_fields = norm_fields_2d
    else:
        assert isinstance(plot_obj, graph.Scatter3d)
        d["dims"] = "3d"
        is_3d = True
        norm_fields = "fixme"

    # Grab all the easy fields
    for field in norm_fields:
        d[field] = getattr(plot_obj, field)

    # Normalize line and marker styles to dictionaries
    d["line"] = normalize_line_style(plot_obj.line)
    d["marker"] = normalize_marker_style(plot_obj.marker)

    return d


def normalize_line_style(line_style):
    """
    Normalize a Scatter.Line or Scatter3d.Line
    """
    d = {}

    for field in ["color", "width"]:
        d[field] = getattr(line_style, field)

    if hasattr(line_style, "dash"):
        d["dash"] = line_style.dash

    return d


def normalize_marker_style(marker_style):
    """
    Normalize a Scatter.Marker or Scatter3d.Marker object
    """
    d = {}

    for field in ["color", "size", "symbol"]:
        d[field] = getattr(marker_style, field)

    d["line"] = normalize_line_style(marker_style.line)

    return d


def rnd_color():
    """
    Generate a random color with possible alpha
    """
    r, g, b = (rnd.randrange(256) for i in range(3))

    a = max(0.0, min(1.0, rnd.uniform(-0.5, 1.5)))

    return shpl.rgb(r, g, b, a)


def rnd_style(with_fill):
    s = shpl.Style()

    if rnd.uniform(0.0, 1.0) < 0.5:
        s.parent = rnd_style(with_fill)

    s.line_style, s.vertex_style, s.fill_color = rnd_style_elements(with_fill)
    s.hole_line_style, s.hole_vertex_style, _ = rnd_style_elements(False)
    s.point_style = rnd_marker_style()
    u = rnd.uniform(0.0, 1.0)
    if u < 0.2:
        s.legend_group = None
    elif u < 0.4:
        s.legend_group = shpl.DEFAULT
    else:
        s.legend_group = rnd_string()

    u = rnd.uniform(0.0, 1.0)
    if u < 0.2:
        s.scatter_kwargs = {}
    elif u < 0.4:
        s.scatter_kwargs = shpl.DEFAULT
    else:
        s.scatter_kwargs = {"hovertext": rnd_string()}

    check_style(s)
    return s


def rnd_style_elements(with_fill):
    e_bits = 8 if with_fill else 4
    elements = rnd.randrange(1, e_bits)

    if elements & 1:
        if rnd.uniform(0.0, 1.0) < 0.2:
            line_style = shpl.DEFAULT
        else:
            line_style = rnd_line_style()
    else:
        line_style = None

    if elements & 2:
        if rnd.uniform(0.0, 1.0) < 0.2:
            vertex_style = shpl.DEFAULT
        else:
            vertex_style = rnd_marker_style()
    else:
        vertex_style = None

    if elements & 3:
        if rnd.uniform(0.0, 1.0) < 0.2:
            fill_color = shpl.DEFAULT
        else:
            fill_color = rnd_color()
    else:
        fill_color = None

    return line_style, vertex_style, fill_color


def rnd_line_style():
    d = {
        "color": rnd_color(),
        "width": rnd.randrange(1, 8)
    }

    return d


def rnd_marker_style():
    d = {
        "color": rnd_color(),
        "size": rnd.randrange(1, 8),
        "symbol": rnd.choice(marker_symbols)
    }

    return d


def rnd_string():
    l = rnd.randrange(5, 20)
    s = "".join(rnd.choice(rnd_chars) for i in range(l))
    return s


def check_style(s):
    """
    Test all Style elements to make sure they give the correct values.
    """

    for attr in [
        "line_style",
        "vertex_style",
        "hole_line_style",
        "hole_vertex_style",
        "fill_color",
        "point_style",
        "legend_group",
        "scatter_kwargs"
    ]:
        base_v = getattr(s, "_" + attr)
        if base_v is shpl.DEFAULT:
            exp_v = getattr(s.parent, attr)
        else:
            exp_v = base_v

        assert getattr(s, attr) == exp_v

    return


rnd.seed(1)
for i in range(1000):
    s = rnd_style(rnd.randrange(2))
