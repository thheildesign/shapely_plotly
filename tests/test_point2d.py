"""
Check Point 2D plotting.
"""

import random as rnd
from shapely_plotly.tests.utils.rnd_shapes import rnd_point_plot2d
from shapely_plotly.tests.utils.run_main import run_main, TDef, start_end_id
from shapely_plotly.tests.utils.utils import normalize_plot_obj

from shapely_plotly import show2d


def test_point_plot2d(test_num=None, show=False):
    s, e = start_end_id(test_num, 100, 200)
    for i in range(s, e):
        rnd.seed(i)
        do_test_point_plot2d(show)
    return


test_list = [
    TDef(test_point_plot2d, has_id=True, has_show=True)
]


def do_test_point_plot2d(show):
    plot_data = []
    expect_data = rnd_point_plot2d(plot_data, -2.0, -2.0, width=4.0)

    if show:
        show2d(plot_data)

    assert len(plot_data) == 1
    norm_data = normalize_plot_obj(plot_data[0])

    # FIXME: More meaningful checker.
    assert norm_data == expect_data


if __name__ == "__main__":
    run_main(test_list)
