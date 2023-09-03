"""
Check Line 2D plotting.
"""

from shapely_plotly.tests.utils.run_main import run_main, TDef
from shapely_plotly.tests.utils.rnd_shapes import RndLineString2d, RndLineRing2d, RndMultiLine2d, do_test_geom_plot2d_v2


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
    do_test_geom_plot2d_v2(test_num, show, RndMultiLine2d, "test_multiline_plot2d")
    return


test_list.append(TDef(test_multiline_plot2d, has_id=True, has_show=True))


if __name__ == "__main__":
    run_main(test_list)
