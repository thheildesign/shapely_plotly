"""
Check Point 2D plotting.
"""

import random as rnd
from shapely_plotly.tests.utils.rnd_shapes import rnd_poly_simple_plot2d
from shapely_plotly.tests.utils.run_main import run_main, TDef, start_end_id
from shapely_plotly.tests.utils.utils import normalize_plot_obj, compare_object

from shapely_plotly import show2d


test_list = []


def test_poly_simple_plot2d(test_num=None, show=False):
    s, e = start_end_id(test_num, 100, 200)
    for i in range(s, e):
        do_test_geom_plot2d(i, show, rnd_poly_simple_plot2d)
    return


test_list.append(TDef(test_poly_simple_plot2d, has_id=True, has_show=True))


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
