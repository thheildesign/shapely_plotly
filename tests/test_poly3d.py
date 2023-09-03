"""
Check Point 3D plotting.
"""

import random as rnd
from shapely_plotly.tests.utils.rnd_shapes_3d import (
    do_test_geom_plot3d, RndPolySimple3d, RndPolyComplex3d, RndMultiPoly3d, RndGeomCollection3d
)

from shapely_plotly.tests.utils.run_main import run_main, TDef

test_list = []


def test_poly_simple_plot3d(test_num=None, show=False):
    """
    Self-checking randoms for simple polygons (no holes) - 3D
    """
    do_test_geom_plot3d(test_num, show, RndPolySimple3d, "test_poly_simple_plot3d")
    return


test_list.append(TDef(test_poly_simple_plot3d, has_id=True, has_show=True))


def test_poly_complex_plot3d(test_num=None, show=False):
    """
    Self-checking randoms for complex polygons (arbitrary shapes, with arbitrary holes).
    """
    do_test_geom_plot3d(test_num, show, RndPolyComplex3d, "test_poly_complex_plot3d")
    return


test_list.append(TDef(test_poly_complex_plot3d, has_id=True, has_show=True))


def test_multipoly_plot3d(test_num=None, show=False):
    """
    Self-checking randoms for mulit-polygone plots - 3D.
    """
    do_test_geom_plot3d(test_num, show, RndMultiPoly3d, "test_multipoly_plot3d")
    return


test_list.append(TDef(test_multipoly_plot3d, has_id=True, has_show=True))


def test_geometry_collection_plot3d(test_num=None, show=False):
    """
    Self-checking randoms for geometry collections - 3D.

    These are not Polygons, but the test structure is the same, so we place it here.
    """
    do_test_geom_plot3d(test_num, show, RndGeomCollection3d, "test_geometry_collection_plot3d")
    return


test_list.append(TDef(test_geometry_collection_plot3d, has_id=True, has_show=True))


if __name__ == "__main__":
    run_main(test_list)
