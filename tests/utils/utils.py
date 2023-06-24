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

    # Polygons will sometimes be labled as fill toself even when there is no fill color.
    # In this case we ignore it, because filling with no fill color will not fill.  So we normalize it to None
    fill = plot_obj.fill
    d["fill"] = None if (plot_obj.fillcolor is None) else fill

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

    a = max(0.0, min(1.0, rnd.uniform(0.2, 1.5)))

    return shpl.rgb(r, g, b, a)


def rnd_style(with_fill):
    s = shpl.Style()

    if rnd.uniform(0.0, 1.0) < 0.5:
        s.parent = rnd_style(with_fill)

    s.line_style, s.vertex_style, s.fill_color = \
        rnd_style_elements(with_fill, s.parent.line_style, s.parent.vertex_style, s.parent.fill_color)
    s.hole_line_style, s.hole_vertex_style, _ = \
        rnd_style_elements(False, s.parent.hole_line_style, s.parent.hole_vertex_style, None)
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


def rnd_style_elements(with_fill, parent_line_style, parent_vertex_style, parent_fill_color):
    e_bits = 8 if with_fill else 4
    elements = rnd.randrange(1, e_bits)

    if elements & 1:
        if (parent_line_style is not None) and (rnd.uniform(0.0, 1.0) < 0.2):
            line_style = shpl.DEFAULT
        else:
            line_style = rnd_line_style()
    else:
        line_style = None

    if elements & 2:
        if (parent_vertex_style is not None) and  (rnd.uniform(0.0, 1.0) < 0.2):
            vertex_style = shpl.DEFAULT
        else:
            vertex_style = rnd_marker_style()
    else:
        vertex_style = None

    if elements & 4:
        if (parent_fill_color is not None ) and (rnd.uniform(0.0, 1.0) < 0.2):
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

compare_type_code = {
    int: "p",
    float: "p",
    bool: "p",
    type(None): "p",
    str: "p",
    list: "l",
    tuple: "l",
    dict: "d"
}


def compare_object(a_name, a, b_name, b, title):
    if a == b:  # Fast quick compare.  Common case.
        return

    at, bt = type(a), type(b)
    if at != bt:
        assert False, f'{title}: Type of {a_name}={at} differs from {b_name}={bt}'

    tc = compare_type_code[at]  # B must be the same.
    if tc == "p":
        assert False, f'{title}: {a_name}={repr(a)} differs from {b_name}={repr(b)}'

    if tc == "l":
        compare_list(a_name, a, b_name, b, title)

    elif tc == "d":
        compare_dict(a_name, a, b_name, b, title)

    assert False, f'{title}: Internal error comparing {a_name} and {b_name}.  Could not detect differences.'
    return


def compare_list(a_name, a, b_name, b, title):
    if len(a) != len(b):
        assert False, f'{title}: Lengths of {a_name}={len(a)} and {b_name}={len(b)} differ.'

    for i in range(len(a)):
        new_a_name = f'{a_name}[{i}]'
        new_b_name = f'{b_name}[{i}]'
        compare_object(new_a_name, a[i], new_b_name, b[i], title)

    return


def compare_dict(a_name, a, b_name, b, title):
    if len(b) > len(a):
        # B is larger.  Look for B keys not in A
        for k in b.keys():
            if k not in a:
                assert False, f'{title}: Key {repr(k)} in {b_name} but not in {a_name}'
        assert False, "Should not reach here"
    else:
        # A is larger or equal.  Look for A keys not in B
        for k in a.keys():
            if k not in b:
                assert False, f'{title}: Key {repr(k)} in {a_name} but not in {b_name}'

    # Keys match.  Check all values.
    
    for k in a.keys():
        kr = f'[{repr(k)}]'
        new_a_name = a_name + kr
        new_b_name = b_name + kr
        compare_object(new_a_name, a[k], new_b_name, b[k], title)

    return
