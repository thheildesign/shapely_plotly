import random as rnd
from math import pi, sin, cos
import shapely as shp
from shapely_plotly.tests.utils.utils import rnd_style
import shapely_plotly as shpl

def rnd_coord(xoff, yoff, width=1.0, height=None):
    if height is None:
        height = width

    l = rnd.randrange(10, 20)
    x = rnd.randrange(xoff, xoff+width)
    y = rnd.randrange(yoff, yoff + height)

    return x, y

def rnd_coords(xoff, yoff, width=1.0, height=None):
    if height is None:
        height = width

    l = rnd.randrange(10, 20)
    x = [rnd.randrange(xoff, xoff+width) for i in range(l)]
    y = [rnd.randrange(yoff, yoff + height) for i in range(l)]

    return x, y

def zip_xy(x, y):
    z = list(zip(x,y))
    return z


def rnd_rect_coords(xoff, yoff, max_width=1.0, max_height=None):
    if max_height is None:
        max_height = max_width

    width = rnd.randrange(max_width*0.5, max_width)
    height = rnd.randrange(max_height*0.5, max_height)

    x0 = xoff
    x1 = xoff + width
    y0 = yoff
    y1 = yoff + height
    x = [x0, x0, x1, x1]
    y = [y0, y1, y1, y0]

    x,y = complete_poly_coords(x, y)

    return x,y


def rand_poly_coords(xoff, yoff, max_width=1.0, max_height=None):

    l = rnd.randrange(3, 20)

    while True:
        angles = [rnd.uniform(0, 2*pi) for i in range(l)]
        angles.sort()

        fail = False
        for i in range(0, len(angles)-1):
            if angles[i]==angles[i+1]:
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
            scale = 1.0/dx
        else:
            scale = 1.0/dy

        x = dx*scale
        y = dy*scale

        x = (x+1.0)*0.5*max_width + xoff
        y = (y+1.0)*0.5+max_height + yoff
        xs.append(x)
        ys.append(y)

    xs, yx = complete_poly_coords(xs, ys)

    return xs,ys


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


def rnd_shapely_point2d(xoff, yoff, width=1.0, height=None):
    x,y = rnd_coord(xoff, yoff, width, height)
    p = shp.Point(x, y)
    return p


def rnd_point_plot2d(plot_data, xoff, yoff, width=1.0, height=None):
    p = rnd_shapely_point2d(xoff, yoff, width, height)
    rnd_plot2d(p, plot_data, False)
    return


def rnd_plot2d(geom, plot_data, with_fill):
    """
    Randomly plot-2D a geometry object, applying a random style in one of four ways.

    with_fill - Whether the geometry needs a fill color.
    """

    s = rnd_style(with_fill)

    # Four methods of applying a style:
    # a) Applied to object ahead of time.
    # c) Given to the draw call.
    # n) No style at all (default_style)
    # o) An ignored style set a head of time, overlaid by the actual style at call time.
    method = rnd.choice("acno")

    if method=="a":
        s = rnd_style(with_fill)
        geom.set_style(s)
        draw_style = shpl.DEFAULT
        final_style = s
    elif method=="c":
        draw_style = rnd_style(with_fill)
        final_style = draw_style
    elif method=="n":
        draw_style = shpl.DEFAULT
        final_style = shpl.default_style
    elif method=="o":
        s = rnd_style(with_fill)
        geom.set_style(s)
        draw_style = rnd_style(with_fill)
        final_style = draw_style

    geom.plotly_draw2d(plot_data, style=draw_style)
    return final_style
