"""
Check Point 2D plotting.
"""

import random as rnd
from shapely_plotly.tests.utils.rnd_shapes import RndPoint2d, RndMultiPoint2d, do_test_geom_plot2d_v2
from shapely_plotly.tests.utils.run_main import run_main, TDef


test_list = []


def test_point_plot2d(test_num=None, show=False):
    """
    Self-checking randoms for points - 2D
    """
    do_test_geom_plot2d_v2(test_num, show, RndPoint2d, "test_point_plot2d")
    return


test_list.append(TDef(test_point_plot2d, has_id=True, has_show=True))


def test_multipoint_plot2d(test_num=None, show=False):
    """
    Self-checking randoms for multi-points - 2D
    """
    do_test_geom_plot2d_v2(test_num, show, RndMultiPoint2d, "test_multipoint_plot2d")
    return


test_list.append(TDef(test_multipoint_plot2d, has_id=True, has_show=True))


if __name__ == "__main__":
    run_main(test_list)
