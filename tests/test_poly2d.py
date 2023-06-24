"""
Check Point 2D plotting.
"""

import random as rnd
from shapely_plotly.tests.utils.rnd_shapes import rnd_poly_simple_plot2d, fixed_rect_coords, zip_xy
from shapely_plotly.tests.utils.run_main import run_main, TDef, start_end_id
from shapely_plotly.tests.utils.utils import normalize_plot_obj, compare_object

from shapely_plotly import show2d

import shapely_plotly as sh2pl
import shapely as shp

test_list = []


def test_poly_simple_plot2d(test_num=None, show=False):
    s, e = start_end_id(test_num, 100, 200)
    for i in range(s, e):
        do_test_geom_plot2d(i, show, rnd_poly_simple_plot2d)
    return


test_list.append(TDef(test_poly_simple_plot2d, has_id=True, has_show=True))


def viz_test_poly_rect_holes_plot2d(test_num=None, show=False):
    """
    The purpose of this test is to check the hole filling.  Plotly is a bit particular
    in the CW/CCW order of exteriors and interiors.  It is must be checked individually.

    It will produce a grid of 16 polygons.  Each will have a rectangular shell, and 9 rectangular
    holes.  They will look the same, but all will have different rotations and rotation directions.

    All holes should be empty. We use a consistent style here to highlight this property.
    """

    s, e = start_end_id(test_num, 100, 200)
    for i in range(s, e):
        do_test_poly_rect_holes_plot2d(i, show)
    return


def do_test_poly_rect_holes_plot2d(test_num, show):
    rnd.seed(test_num)

    plot_width = 100
    plot_height = 60
    grid_width = 4
    grid_height = 4

    r_width = plot_width/grid_width
    r_height = plot_height/grid_height

    p_width = r_width*0.8
    p_height = r_height*0.8

    s = sh2pl.Style()
    s.line_style = None
    s.fill_color = sh2pl.rgb(20,20,20)
    s.hole_line_style = dict(width=5, color=sh2pl.rgb(200,200,0))

    plot_data = []
    for gx in range(0, grid_width):
        x0 = gx*r_width
        for gy in range(0, grid_height):
            y0 = gy*r_height
            ext_x, ext_y = fixed_rect_coords(x0, y0, p_width, p_height)

            # Build a list of hole positions.
            hoffsets = []
            for hx in range(3):
                hxoff = x0 + hx*p_width*0.3 + p_width*0.1
                for hy in range(3):
                    hyoff = y0 + hy*p_height*0.3 + p_height*0.1
                    hoffsets.append((hxoff, hyoff))

            # Scramble it.
            rnd.shuffle(hoffsets)

            # Build the holes
            holes = []
            for hxoff, hyoff in hoffsets:
                int_x, int_y = fixed_rect_coords(hxoff, hyoff, p_width*0.2, p_height*0.2)
                holes.append(zip_xy(int_x, int_y))

            p = shp.Polygon(shell=zip_xy(ext_x, ext_y), holes=holes)
            p.plotly_draw2d(plot_data, style=s)

    if show:
        show2d(plot_data)

    return


test_list.append(TDef(viz_test_poly_rect_holes_plot2d, has_id=True, has_show=True))


def do_test_geom_plot2d(test_num, show, rnd_plot_f):
    rnd.seed(test_num)

    plot_data = []
    expect_data = []
    n = rnd.randrange(1, 4)

    for i in range(n):
        e = rnd_plot_f(plot_data, i*120, -50.0, width=100)
        expect_data.append(e)

    if show:
        show2d(plot_data)

    assert len(plot_data) == n
    norm_data = [normalize_plot_obj(d) for d in plot_data]

    compare_object("norm", norm_data, "expected", expect_data, f'test_point_plot2d[{test_num}]')

if __name__ == "__main__":
    run_main(test_list)
