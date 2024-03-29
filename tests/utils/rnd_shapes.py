import random as rnd
from math import pi, sin, cos
import shapely as shp
from shapely_plotly.tests.utils.utils import rnd_style, rnd_string, normalize_plot_obj, compare_object
import shapely_plotly as shpl
from abc import ABC, abstractstaticmethod
from shapely_plotly.tests.utils.run_main import start_end_id


# -----------------------------------------------------------------
# Random coordinates
# -----------------------------------------------------------------


def rnd_coord(xoff, yoff, width=1.0, height=None):
    if height is None:
        height = width

    x = rnd.uniform(xoff, xoff + width)
    y = rnd.uniform(yoff, yoff + height)

    return x, y


def rnd_coords(xoff, yoff, width=1.0, height=None):
    if height is None:
        height = width

    l = rnd.randrange(10, 20)
    x = [rnd.uniform(xoff, xoff + width) for i in range(l)]
    y = [rnd.uniform(yoff, yoff + height) for i in range(l)]

    return x, y


def zip_xy(x, y):
    z = list(zip(x, y))
    return z


def fixed_rect_coords(xoff, yoff, width, height):
    x0 = xoff
    x1 = xoff + width
    y0 = yoff
    y1 = yoff + height
    x = [x0, x0, x1, x1]
    y = [y0, y1, y1, y0]

    x, y = complete_poly_coords(x, y)

    return x, y


def rnd_rect_coords(xoff, yoff, max_width=1.0, max_height=None):
    if max_height is None:
        max_height = max_width

    width = rnd.uniform(max_width * 0.5, max_width)
    height = rnd.uniform(max_height * 0.5, max_height)

    xoff = rnd.uniform(xoff, xoff + max_width - width)
    yoff = rnd.uniform(yoff, yoff + max_height - height)

    x, y = fixed_rect_coords(xoff, yoff, width, height)
    return x, y


def rnd_poly_coords(xoff, yoff, max_width=1.0, max_height=None):
    l = rnd.randrange(3, 20)

    if max_height is None:
        max_height = max_width

    while True:
        angles = [rnd.uniform(0, 2 * pi) for i in range(l)]
        angles.sort()

        fail = False
        for i in range(0, len(angles) - 1):
            if angles[i] == angles[i + 1]:
                fail = True
                break
        if not fail:
            break

    xs = []
    ys = []

    for a in angles:
        dx = cos(a)
        dy = sin(a)
        if abs(dx) > abs(dy):
            scale = 1.0 / abs(dx)
        else:
            scale = 1.0 / abs(dy)

        l = rnd.uniform(0.3, 1.0)
        x = dx * scale * l
        y = dy * scale * l

        x = (x + 1.0) * 0.5 * max_width + xoff
        y = (y + 1.0) * 0.5 * max_height + yoff
        xs.append(x)
        ys.append(y)

    xs, ys = complete_poly_coords(xs, ys)

    return xs, ys


def complete_poly_coords(x, y):
    """
    Randomly flip CW / CCW.
    Rotate to a random starting point.
    Add return to start coordinate.
    """
    if rnd.uniform(0.0, 1.0) < 0.5:
        # Flip to counter clockwise
        x.reverse()
        y.reverse()

    s = rnd.randrange(0, len(x))
    if s > 0:
        # Rotate to new starting point
        x = x[s:] + x[:s]
        y = y[s:] + y[:s]

    # Add return to start
    x.append(x[0])
    y.append(y[0])

    return x, y


# -----------------------------------------------------------------
# Random Shapely geometries
# -----------------------------------------------------------------

class RndGeometry(ABC):
    @abstractstaticmethod
    def rnd_shape_2d(xoff, yoff, width, height):
        """
        Produce a random shape of the given geometry.
        Also optionally produce prototype expected data.   This is typically the dimensions
        and the x/y coordinates, if known.
        Return (geom, proto_expected_data)
        """
        return

    @abstractstaticmethod
    def get_expected_data_2d(geom, proto_expected_data, final_style, final_name, plot_data, pd_start,
                             expected_data_list):
        """
        Compute expected_data for the plotted geometry, and add to expected_data list.
        geom - The geometry plotted
        proto_expected_data - from rnd_shape_2d.
        final_style - The style chosen during plotting.
        final_name - The name assigned during plotting.
        plot_data - The plots
        pd_start - The first plot in plot_data belonging to the geometry.
        expected_data - To be updated with needed expected data.
        """
        return

    @abstractstaticmethod
    def style_mode():
        """
        Get the style mode to use when adding random styles.
        """
        return


class RndPoint2d(RndGeometry):
    def rnd_shape_2d(xoff, yoff, width, height):
        """
        Produce a random shape of the given geometry.
        Also optionally produce prototype expected data.   This is typically the dimensions
        and the x/y coordinates, if known.
        Return (geom, proto_expected_data)
        """
        x, y = rnd_coord(xoff, yoff, width, height)
        geom = shp.Point(x, y)
        proto_expected_data = dict(
            dims="2d",
            x=(x,),
            y=(y,)
        )
        return geom, proto_expected_data

    @abstractstaticmethod
    def get_expected_data_2d(geom, proto_expected_data, final_style, final_name, plot_data, pd_start,
                             expected_data_list):
        """
        Compute expected_data for the plotted geometry, and add to expected_data list.
        geom - The geometry plotted
        proto_expected_data - from rnd_shape_2d.
        final_style - The style chosen during plotting.
        final_name - The name assigned during plotting.
        plot_data - The plots
        pd_start - The first plot in plot_data belonging to the geometry.
        expected_data - To be updated with needed expected data.
        """
        add_normalized_style_info(proto_expected_data, final_style, final_name, "point")
        expected_data_list.append(proto_expected_data)
        return

    @abstractstaticmethod
    def style_mode():
        return "point"


class RndMultiPoint2d(RndGeometry):
    def rnd_shape_2d(xoff, yoff, width, height):
        """
        Produce a random shape of the given geometry.
        Also optionally produce prototype expected data.   This is typically the dimensions
        and the x/y coordinates, if known.
        Return (geom, proto_expected_data)
        """
        x, y = rnd_coords(xoff, yoff, width, height)
        geom = shp.MultiPoint(zip_xy(x, y))
        proto_expected_data = dict(
            dims="2d",
            x=tuple(x),
            y=tuple(y)
        )

        return geom, proto_expected_data

    @abstractstaticmethod
    def get_expected_data_2d(geom, proto_expected_data, final_style, final_name, plot_data, pd_start,
                             expected_data_list):
        """
        Compute expected_data for the plotted geometry, and add to expected_data list.
        geom - The geometry plotted
        proto_expected_data - from rnd_shape_2d.
        final_style - The style chosen during plotting.
        final_name - The name assigned during plotting.
        plot_data - The plots
        pd_start - The first plot in plot_data belonging to the geometry.
        expected_data - To be updated with needed expected data.
        """
        add_normalized_style_info(proto_expected_data, final_style, final_name, "point")
        expected_data_list.append(proto_expected_data)
        return

    @abstractstaticmethod
    def style_mode():
        return "point"


class RndLineString2d(RndGeometry):
    def rnd_shape_2d(xoff, yoff, width, height):
        """
        Produce a random shape of the given geometry.
        Also optionally produce prototype expected data.   This is typically the dimensions
        and the x/y coordinates, if known.
        Return (geom, proto_expected_data)
        """
        x, y = rnd_coords(xoff, yoff, width, height)
        geom = shp.LineString(zip_xy(x, y))
        proto_expected_data = dict(
            dims="2d",
            x=tuple(x),
            y=tuple(y)
        )

        return geom, proto_expected_data

    @abstractstaticmethod
    def get_expected_data_2d(geom, proto_expected_data, final_style, final_name, plot_data, pd_start,
                             expected_data_list):
        """
        Compute expected_data for the plotted geometry, and add to expected_data list.
        geom - The geometry plotted
        proto_expected_data - from rnd_shape_2d.
        final_style - The style chosen during plotting.
        final_name - The name assigned during plotting.
        plot_data - The plots
        pd_start - The first plot in plot_data belonging to the geometry.
        expected_data - To be updated with needed expected data.
        """
        add_normalized_style_info(proto_expected_data, final_style, final_name, "line")
        expected_data_list.append(proto_expected_data)
        return

    @abstractstaticmethod
    def style_mode():
        return "line"


class RndLineRing2d(RndGeometry):
    def rnd_shape_2d(xoff, yoff, width, height):
        """
        Produce a random shape of the given geometry.
        Also optionally produce prototype expected data.   This is typically the dimensions
        and the x/y coordinates, if known.
        Return (geom, proto_expected_data)
        """
        x, y = rnd_coords(xoff, yoff, width, height)
        geom = shp.LinearRing(zip_xy(x, y))

        if (x[0] != x[-1]) or (y[0] != y[-1]):
            # Add closing point.
            x = tuple(x) + (x[0],)
            y = tuple(y) + (y[0],)
        else:
            # Already closed
            x = tuple(x)
            y = tuple(y)

        proto_expected_data = dict(
            dims="2d",
            x=x,
            y=y
        )

        return geom, proto_expected_data

    @abstractstaticmethod
    def get_expected_data_2d(geom, proto_expected_data, final_style, final_name, plot_data, pd_start,
                             expected_data_list):
        """
        Compute expected_data for the plotted geometry, and add to expected_data list.
        geom - The geometry plotted
        proto_expected_data - from rnd_shape_2d.
        final_style - The style chosen during plotting.
        final_name - The name assigned during plotting.
        plot_data - The plots
        pd_start - The first plot in plot_data belonging to the geometry.
        expected_data - To be updated with needed expected data.
        """
        add_normalized_style_info(proto_expected_data, final_style, final_name, "line")
        expected_data_list.append(proto_expected_data)
        return

    @abstractstaticmethod
    def style_mode():
        return "line"


class RndMultiLine2d(RndGeometry):
    def rnd_shape_2d(xoff, yoff, width, height):
        """
        Produce a random shape of the given geometry.
        Also optionally produce prototype expected data.   This is typically the dimensions
        and the x/y coordinates, if known.
        Return (geom, proto_expected_data)
        """

        n = rnd.randrange(1, 5)
        xys = [None] * n
        ex, ey = [], []
        for i in range(n):
            x, y = rnd_coords(xoff + (width + 1) * i, yoff, width, height)
            xys[i] = zip_xy(x, y)
            if i > 0:
                ex.append(None)
                ey.append(None)
            ex.extend(x)
            ey.extend(y)

        geom = shp.MultiLineString(xys)

        proto_expected_data = dict(
            dims="2d",
            x=tuple(ex),
            y=tuple(ey)
        )

        return geom, proto_expected_data

    @abstractstaticmethod
    def get_expected_data_2d(geom, proto_expected_data, final_style, final_name, plot_data, pd_start,
                             expected_data_list):
        """
        Compute expected_data for the plotted geometry, and add to expected_data list.
        geom - The geometry plotted
        proto_expected_data - from rnd_shape_2d.
        final_style - The style chosen during plotting.
        final_name - The name assigned during plotting.
        plot_data - The plots
        pd_start - The first plot in plot_data belonging to the geometry.
        expected_data - To be updated with needed expected data.
        """
        add_normalized_style_info(proto_expected_data, final_style, final_name, "line")
        expected_data_list.append(proto_expected_data)
        return

    @abstractstaticmethod
    def style_mode():
        return "line"


class RndPolySimple2d(RndGeometry):
    def rnd_shape_2d(xoff, yoff, width, height):
        """
        Produce a random shape of the given geometry.
        Also optionally produce prototype expected data.   This is typically the dimensions
        and the x/y coordinates, if known.
        Return (geom, proto_expected_data)
        """
        x, y = rnd_rect_coords(xoff, yoff, width, height)
        geom = shp.Polygon(shell=zip_xy(x, y))

        if (x[0] != x[-1]) or (y[0] != y[-1]):
            # Add closing point.
            x = tuple(x) + (x[0],)
            y = tuple(y) + (y[0],)
        else:
            # Already closed
            x = tuple(x)
            y = tuple(y)

        proto_expected_data = dict(
            dims="2d",
            x=x,
            y=y
        )

        return geom, proto_expected_data

    @abstractstaticmethod
    def get_expected_data_2d(geom, proto_expected_data, final_style, final_name, plot_data, pd_start,
                             expected_data_list):
        add_normalized_style_info(proto_expected_data, final_style, final_name, "poly")
        expected_data_list.append(proto_expected_data)

        return

    @abstractstaticmethod
    def style_mode():
        return "poly"


class RndPolyComplex2d(RndGeometry):
    def rnd_shape_2d(xoff, yoff, width, height):
        """
        Produce a random shape of the given geometry.
        Also optionally produce prototype expected data.   This is typically the dimensions
        and the x/y coordinates, if known.
        Return (geom, proto_expected_data)
        """
        # Generate the hull
        while True:
            ext_x, ext_y = rnd_poly_coords(xoff, yoff, width, height)
            ext_xy = zip_xy(ext_x, ext_y)
            shell_p = shp.Polygon(shell=ext_xy)
            if shell_p.is_valid:
                break

        num_int = rnd.randrange(0, 10)
        if num_int > 0:
            # Build a list of hole positions.
            hoffsets = []
            for hx in range(3):
                hxoff = xoff + hx * width * 0.3 + width * 0.1
                for hy in range(3):
                    hyoff = yoff + hy * height * 0.3 + height * 0.1
                    hoffsets.append((hxoff, hyoff))

            # Scramble it.
            rnd.shuffle(hoffsets)

            holes = []
            for (hx, hy) in hoffsets[:num_int]:
                hole_x, hole_y = rnd_poly_coords(hx, hy, width * 0.2, height * 0.2)
                hole_p = shp.Polygon(shell=zip_xy(hole_x, hole_y))
                if not hole_p.is_valid:
                    # Bad hole. skip.
                    continue

                if not shell_p.contains(hole_p):
                    # Hole not contained.
                    continue

                holes.append(zip_xy(hole_x, hole_y))

            if len(holes) > 0:
                shell_p = shp.Polygon(shell=ext_xy, holes=holes)
                # assert shell_p.is_valid

        return shell_p, None  # No proto-type expected data yet.  Depends on the style.

    @abstractstaticmethod
    def get_expected_data_2d(geom, proto_expected_data, final_style, final_name, plot_data, pd_start,
                             expected_data_list):
        """
        Compute expected_data for the plotted geometry, and add to expected_data list.

        Add expected data to expect_data_list for the 1 to 3 plots created by drawing a polygon (geom).
        Unlike other geometries, polygons do not set dims and x/y as geometry creation time.
        For polygons, those values are complex and we wait until after the plots are made to create them.

        geom - The geometry plotted
        proto_expected_data - from rnd_shape_2d.
        final_style - The style chosen during plotting.
        final_name - The name assigned during plotting.
        plot_data - The plots
        pd_start - The first plot in plot_data belonging to the geometry.
        expected_data - To be updated with needed expected data.
        """

        if len(geom.interiors) > 0:
            # Has interioriors.  We have 1 to 3 plots.
            total_plots = 0

            # 1) Fill plot:
            if final_style.fill_color is not None:
                # For x,y I'm just going to take the polygon's x/ys for expected values.
                # This is a non-test.  I could rebuild the x/y lists, but it would just be repeating the
                # same code already in the polygon plot function.
                fill_plot_data = plot_data[pd_start]
                expect_data = {
                    "dims": "2d",
                    "x": tuple(fill_plot_data.x),
                    "y": tuple(fill_plot_data.y)
                }

                assert len(fill_plot_data.x) == \
                       len(geom.exterior.xy[0]) + len(geom.interiors) + sum(len(i.xy[0]) for i in geom.interiors)

                add_normalized_style_info(expect_data, final_style, final_name, "poly_fill")
                expected_data_list.append(expect_data)
                total_plots += 1

            # 2) Exterior plot.
            if (final_style.line_style is not None) or (final_style.vertex_style is not None):
                ext = geom.exterior
                ext_x, ext_y = ext.xy
                expect_data = {
                    "dims": "2d",
                    "x": tuple(ext_x),
                    "y": tuple(ext_y)
                }
                add_normalized_style_info(expect_data, final_style, final_name, "line")
                expected_data_list.append(expect_data)
                total_plots += 1

            # 3) Interiors plot.
            if (final_style.hole_line_style is not None) or (final_style.hole_vertex_style is not None):
                # Again, we just take the plot's xy coordinates.
                hole_plot_data = plot_data[pd_start + total_plots]
                expect_data = {
                    "dims": "2d",
                    "x": tuple(hole_plot_data.x),
                    "y": tuple(hole_plot_data.y)
                }
                assert len(hole_plot_data.x) == \
                       len(geom.interiors) + sum(len(i.xy[0]) for i in geom.interiors) - 1

                add_normalized_style_info(expect_data, final_style, final_name, "hole")
                expected_data_list.append(expect_data)
                total_plots += 1

        else:
            # No interiors.  Just the one plot, and we can build just a single expected value like normal.
            expect_data = {
                "dims": "2d",
                "x": tuple(c[0] for c in geom.exterior.coords),
                "y": tuple(c[1] for c in geom.exterior.coords)
            }
            add_normalized_style_info(expect_data, final_style, final_name, "poly")
            expected_data_list.append(expect_data)

        return

    @abstractstaticmethod
    def style_mode():
        return "poly"


class RndMultiPoly2d(RndGeometry):
    def rnd_shape_2d(xoff, yoff, width, height):
        """
        Produce a random shape of the given geometry.
        Also optionally produce prototype expected data.   This is typically the dimensions
        and the x/y coordinates, if known.
        Return (geom, proto_expected_data)
        """

        # Produce 1 to 6 polygons in the multi-poly
        n = rnd.randrange(1, 6)

        # Arrange in one or two rows of 1 to 3.
        if n > 3:
            pheight = height * 0.45
            ystep = height * 0.55
            nx = (n + 1) // 2
        else:
            nx = n
            pheight = height
            ystep = 0.0

        pwidth = (1.0 - 0.1 * (nx - 1)) / nx
        xstep = pwidth + 0.1
        pwidth *= width
        xstep *= width

        # Produce the polygons.
        geoms = []
        xpoff = xoff
        ypoff = yoff
        for i in range(n):
            poly, _ = RndPolyComplex2d.rnd_shape_2d(xpoff, ypoff, pwidth, pheight)
            geoms.append(poly)
            if i == (nx - 1):
                xpoff = xoff
                ypoff += ystep
            else:
                xpoff += xstep

        geom = shp.MultiPolygon(geoms)
        return geom, None  # No proto-type expected data yet.  Depends on the style.

    @abstractstaticmethod
    def get_expected_data_2d(geom, proto_expected_data, final_style, final_name, plot_data, pd_start,
                             expected_data_list):
        """
        Compute expected_data for the plotted geometry, and add to expected_data list.

        Add expected data to expect_data_list for the 1 to 3 plots created by drawing a polygon (geom).
        Unlike other geometries, polygons do not set dims and x/y as geometry creation time.
        For polygons, those values are complex and we wait until after the plots are made to create them.

        geom - The geometry plotted
        proto_expected_data - from rnd_shape_2d.
        final_style - The style chosen during plotting.
        final_name - The name assigned during plotting.
        plot_data - The plots
        pd_start - The first plot in plot_data belonging to the geometry.
        expected_data - To be updated with needed expected data.
        """

        # Build expected style data for all the plots.  All use the same final_style
        for poly in geom.geoms:
            RndPolyComplex2d.get_expected_data_2d(poly, proto_expected_data, final_style, final_name, plot_data,
                                                  len(expected_data_list), expected_data_list)
        return

    @abstractstaticmethod
    def style_mode():
        return "poly"


class RndGeomCollection2d(RndGeometry):
    def rnd_shape_2d(xoff, yoff, width, height):
        """
        Produce a random shape of the given geometry.
        Also optionally produce prototype expected data.   This is typically the dimensions
        and the x/y coordinates, if known.
        Return (geom, proto_expected_data)
        """

        return RndGeomCollection2d.__rnd_shape_2d(xoff, yoff, width, height, 3)

    @staticmethod
    def __rnd_shape_2d(xoff, yoff, width, height, max_depth):
        n = rnd.randrange(1, 5)
        geoms = []
        protos = []
        if max_depth > 0:
            rnd_classes = rnd_geom_classes
        else:
            # Exclude geometry collection
            rnd_classes = rnd_geom_classes[:-1]

        for i in range(n):
            rnd_class = rnd.choice(rnd_classes)
            if rnd_class is RndGeomCollection2d:
                # Geometry collection needs the depth parameter to prevent run-away
                geom, proto_expected_data = rnd_class.__rnd_shape_2d(xoff, yoff, width, height, max_depth - 1)
            else:
                geom, proto_expected_data = rnd_class.rnd_shape_2d(xoff, yoff, width, height)

            geoms.append(geom)
            protos.append((rnd_class, proto_expected_data))

        geom = shp.GeometryCollection(geoms)
        return geom, protos

    @abstractstaticmethod
    def get_expected_data_2d(geom, proto_expected_data, final_style, final_name, plot_data, pd_start,
                             expected_data_list):
        """
        Compute expected_data for the plotted geometry, and add to expected_data list.

        Add expected data to expect_data_list for the 1 to 3 plots created by drawing a polygon (geom).
        Unlike other geometries, polygons do not set dims and x/y as geometry creation time.
        For polygons, those values are complex and we wait until after the plots are made to create them.

        geom - The geometry plotted
        proto_expected_data - from rnd_shape_2d.
        final_style - The style chosen during plotting.
        final_name - The name assigned during plotting.
        plot_data - The plots
        pd_start - The first plot in plot_data belonging to the geometry.
        expected_data - To be updated with needed expected data.
        """

        # Build expected style data for all the plots.  All use the same final_style
        for geom, (rnd_class, geom_proto) in zip(geom.geoms, proto_expected_data):
            rnd_class.get_expected_data_2d(geom, geom_proto, final_style, final_name, plot_data,
                                           len(expected_data_list), expected_data_list)

        return

    @abstractstaticmethod
    def style_mode():
        return "collection"


rnd_geom_classes = [
    RndPoint2d,
    RndMultiPoint2d,
    RndLineString2d,
    RndLineRing2d,
    RndMultiLine2d,
    RndPolySimple2d,
    RndPolyComplex2d,
    RndMultiPoly2d,
    RndGeomCollection2d
]



def do_rnd_geom_plotting(plot_data, expected_data_list, GeomClass, xoff, yoff, width=1.0, height=None):
    if height is None:
        height = width

    assert len(plot_data) == len(expected_data_list)

    # First build the geometry, and get initial expected data
    geom, proto_expected_data = GeomClass.rnd_shape_2d(xoff, yoff, width, height)

    pd_start = len(plot_data)

    # Now plot the geometry.
    final_style, final_name = rnd_style_plot2d(geom, plot_data, GeomClass.style_mode())

    # Next, build the expected data.
    GeomClass.get_expected_data_2d(geom, proto_expected_data, final_style, final_name,
                                   plot_data, pd_start, expected_data_list)

    assert len(plot_data) == len(expected_data_list)

    # All geometries work the same.  If multiple plots are needed, legend group and show legend are manipulated
    # to make them all under a single legend entry.
    num_plot = len(plot_data) - pd_start
    if num_plot > 1:
        if final_style.legend_group is None:
            # The legend group was generated randomly.  Get it from the first plot and expect all to be the same.
            legend_group = plot_data[pd_start].legendgroup
            for expect_data in expected_data_list[pd_start:]:
                expect_data["legendgroup"] = legend_group

        # Only first plot has show_legend = True
        show_legend = final_name is not None
        if show_legend:
            for expect_data in expected_data_list[pd_start:]:
                expect_data["showlegend"] = show_legend
                show_legend = False

    return


def do_test_geom_plot2d_v2(test_num, show, RndGeomClass, test_name):
    """
    Generic self-checking random test for many geometries - 2D.  One random test.
    """
    test_start, test_end = start_end_id(test_num, 100, 200)
    for test_num in range(test_start, test_end):
        rnd.seed(test_num)

        plot_data = []
        expect_data_list = []
        n = rnd.randrange(1, 4)

        for i in range(n):
            do_rnd_geom_plotting(plot_data, expect_data_list, RndGeomClass, -2.0, 2.0, 4.0, 4.0)

        if show:
            shpl.show2d(plot_data)

        norm_data = [normalize_plot_obj(d) for d in plot_data]

        compare_object("norm", norm_data, "expected", expect_data_list, f'{test_name}[{test_num}]')


# -----------------------------------------------------------------
# Random plotting helper functions - 2D
# -----------------------------------------------------------------


# Style_mode decoder map.
# Functions to grab 0) Line style, 1) marker style, 2) fill color, 3) with_fill
style_usage_map = {
    "point": (lambda s: None, lambda s: s.point_style, lambda s: None, False),
    "line": (lambda s: s.line_style, lambda s: s.vertex_style, lambda s: None, False),
    "hole": (lambda s: s.hole_line_style, lambda s: s.hole_vertex_style, lambda s: None, False),
    "poly": (lambda s: s.line_style, lambda s: s.vertex_style, lambda s: s.fill_color, True),
    "poly_fill": (lambda s: None, lambda s: None, lambda s: s.fill_color, True),
    "collection": (lambda s: s.line_style, lambda s: s.vertex_style, lambda s: s.fill_color, False),
}


def rnd_style_plot2d(geom, plot_data, style_mode):
    """
    Randomly plot-2D a geometry object, applying a random style in one of four ways.

    style_mode - What kind of style the object needs.  See style_usage_map map above.

    Returns: final_style - The random style used during plotting.
    """

    with_fill = style_usage_map[style_mode][3]

    # Four methods of applying a style:
    # a) Applied to object ahead of time.
    # c) Given to the draw call.
    # n) No style at all (default_style)
    # o) An ignored style set a head of time, overlaid by the actual style at call time.
    method = rnd.choice("acno")

    if method == "a":
        # a) Applied to object ahead of time.
        s = rnd_style(with_fill)
        geom.plotly_set_style(s)
        draw_style = shpl.DEFAULT
        final_style = s
    elif method == "c":
        # c) Given to the draw call.
        draw_style = rnd_style(with_fill)
        final_style = draw_style
    elif method == "n":
        # n) No style at all (default_style)
        draw_style = shpl.DEFAULT
        final_style = shpl.default_style
    elif method == "o":
        # o) An ignored style set a head of time, overlaid by the actual style at call time.
        s = rnd_style(with_fill)
        geom.plotly_set_style(s)
        draw_style = rnd_style(with_fill)
        final_style = draw_style

    # The same four methods are used for naming
    method = rnd.choice("acno")

    if method == "a":
        # a) Applied to object ahead of time.
        name = rnd_string()
        geom.plotly_set_name(name)
        draw_name = shpl.DEFAULT
        final_name = name
    elif method == "c":
        # c) Given to the draw call.
        draw_name = rnd_string()
        final_name = draw_name
    elif method == "n":
        # n) No style at all (default_name)
        draw_name = shpl.DEFAULT
        final_name = None
    elif method == "o":
        # o) An ignored style set a head of time, overlaid by the actual style at call time.
        s = rnd_string()
        geom.plotly_set_name(s)
        draw_name = rnd_string()
        final_name = draw_name

    geom.plotly_draw2d(plot_data, style=draw_style, name=draw_name)

    return final_style, final_name


expected_no_line_style = {"color": "rgba(0,0,0,0)", "width": 0, "dash": None}


def add_normalized_style_info(expect_data, style, name, style_mode):
    """
    Add style info to the expected data, given the style itself, and the style_mode.
    """

    # Extract the appropriate style settings from the Style object.
    line_style, marker_style, fill_color = (f(style) for f in style_usage_map[style_mode][0:3])

    expect_data["fillcolor"] = fill_color
    if fill_color is None:
        expect_data["fill"] = None
    else:
        expect_data["fill"] = "toself"

    scatter_kwargs = style.scatter_kwargs
    if scatter_kwargs is None:
        expect_data["hovertext"] = None
    else:
        expect_data["hovertext"] = scatter_kwargs.get("hovertext", None)

    if "mode" in expect_data:
        mode = expect_data["mode"]
        has_lines = "lines" in mode
        has_markers = "markers" in mode
    else:
        has_lines = True
        has_markers = True

    if (line_style is not None) and (has_lines):
        expect_data["line"] = {
            "dash": None,  # FIXME
            "color": line_style["color"],
            "width": line_style["width"]
        }
    else:
        expect_data["line"] = None

    if (marker_style is not None) and (has_markers):
        expect_data["marker"] = {
            "color": marker_style["color"],
            "size": marker_style["size"],
            "symbol": marker_style["symbol"],
            "line": {"color": None, "width": None}
        }
    else:
        expect_data["marker"] = None

    # FIXME: TBD
    expect_data["legendgroup"] = style.legend_group
    expect_data["name"] = name
    expect_data["showlegend"] = name is not None

    if "mode" not in expect_data:
        has_lines = line_style is not None
        has_markers = marker_style is not None
        if has_lines:
            if has_markers:
                mode = "lines+markers"
            else:
                mode = "lines"
        else:
            if has_markers:
                mode = "markers"
            else:
                # No lines or markers, so must have a fill.
                assert fill_color is not None, "Style should have lines, markers or a fill color"
                # In this case, what we do is lines mode, and then have no line.
                mode = "lines"
                expect_data["line"] = expected_no_line_style
        expect_data["mode"] = mode
