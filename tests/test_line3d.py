"""
Check Line 3D plotting.
"""

from shapely_plotly.tests.utils.run_main import run_main, TDef
from shapely_plotly.tests.utils.rnd_shapes_3d import do_test_geom_plot3d, RndLineString3d, RndLineRing3d, RndMultiLine3d


test_list = []


def test_linestring_plot3d(test_num=None, show=False):
    """
    Self-checking randoms for linestrings - 3D
    """
    do_test_geom_plot3d(test_num, show, RndLineString3d, "test_linestring_plot3d")
    return


test_list.append(TDef(test_linestring_plot3d, has_id=True, has_show=True))


def test_linering_plot3d(test_num=None, show=False):
    """
    Self-checking randoms for linerings - 3D
    """
    do_test_geom_plot3d(test_num, show, RndLineRing3d, "test_linering_plot3d")
    return


test_list.append(TDef(test_linering_plot3d, has_id=True, has_show=True))


def test_multiline_plot3d(test_num=None, show=False):
    """
    Self-checking randoms for multi-linestrings - 3D
    """
    do_test_geom_plot3d(test_num, show, RndMultiLine3d, "test_multiline_plot3d")
    return


test_list.append(TDef(test_multiline_plot3d, has_id=True, has_show=True))


if __name__ == "__main__":
    run_main(test_list)
