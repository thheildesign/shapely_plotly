"""
Check Point 2D plotting.
"""

import random as rnd
from shapely_plotly.tests.utils.rnd_shapes import rnd_linestring_plot2d, rnd_multiline_plot2d
from shapely_plotly.tests.utils.run_main import run_main, TDef, start_end_id
from shapely_plotly.tests.utils.utils import do_test_geom_plot2d
from shapely_plotly.tests.utils.rnd_shapes import RndLineString2d, RndLineRing2d, do_test_geom_plot2d_v2

from shapely_plotly import show2d


test_list = []


def test_linestring_plot2d(test_num=None, show=False):
    """
    Self-checking randoms for linestrings - 2D
    """
    do_test_geom_plot2d_v2(test_num, show, RndLineString2d, "test_linestring_plot2d")
    return


test_list.append(TDef(test_linestring_plot2d, has_id=True, has_show=True))


def test_linering_plot2d(test_num=None, show=False):
    """
    Self-checking randoms for linerings - 2D
    """
    do_test_geom_plot2d_v2(test_num, show, RndLineRing2d, "test_linering_plot2d")
    return


test_list.append(TDef(test_linering_plot2d, has_id=True, has_show=True))


def test_multiline_plot2d(test_num=None, show=False):
    """
    Self-checking randoms for multi-linestrings - 2D
    """
    s, e = start_end_id(test_num, 100, 200)
    for i in range(s, e):
        do_test_geom_plot2d(i, show, rnd_multiline_plot2d, "test_multiline_plot2d")
    return


test_list.append(TDef(test_multiline_plot2d, has_id=True, has_show=True))


if __name__ == "__main__":
    run_main(test_list)
