"""
Check Point 3D plotting.
"""

import random as rnd
from shapely_plotly.tests.utils.rnd_shapes_3d import do_test_geom_plot3d, RndPoint3d # , RndMultiPoint3d,
from shapely_plotly.tests.utils.run_main import run_main, TDef


test_list = []


def test_point_plot3d(test_num=None, show=False):
    """
    Self-checking randoms for points - 3D
    """
    do_test_geom_plot3d(test_num, show, RndPoint3d, "test_point_plot3d")
    return


test_list.append(TDef(test_point_plot3d, has_id=True, has_show=True))


# def test_multipoint_plot3d(test_num=None, show=False):
#     """
#     Self-checking randoms for multi-points - 3D
#     """
#     do_test_geom_plot3d_v2(test_num, show, RndMultiPoint3d, "test_multipoint_plot3d")
#     return
#
#
# test_list.append(TDef(test_multipoint_plot3d, has_id=True, has_show=True))


if __name__ == "__main__":
    run_main(test_list)
