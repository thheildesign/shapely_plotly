# Shapely to Plotly

Shapely to Plotly plots Shapely geometries via Plotly.

## Installation
* Clone this repo.
* Add the repo's parent directory to your PYTHONPATH
* Install Shapely (https://shapely.readthedocs.io/en/stable/manual.html) and Plotly (https://plotly.com/python/) normally.
* Import and use shapely normally.
* Import and use Shapely to Plotly: `import shapeply_plotly`

## Getting Started

See [example1.py](example1.py) for the complete code.

### 1) Import shapely_plotly and shapely

```
import shapely_plotly as sh2p
import shapely as shp
```

Importing plotly is not essential, unless you are adding Plotly-specific details to the figures.

After importing `shapely_plotly`, Shaply geometry classes will magically have new plotly_...(...) functions:

* Plotting: `plotly_draw2d(...)`, `plotly_draw3d(...)`
* Style management (colors, lines, markers, etc.): `plotly_get_...(...)`,  `plotly_set_...(...)`
* Legend entries and object naming: `plotly_set_name(name)`

You can get documentation via Python's normal help system:

* `help(shp.Polygon)`
* `help(shp.Polygon.plotly_draw2d)`

### 3) Create a Shapely geometry normally
```
poly_points = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0), (0.0, 0.0)]
p = shp.Polygon(shell=poly_points)
```

### 4) Plot the Shapely geometry

The plotting routines add one or more Plotly scatter plots to a list.  The list of scatter plots are then 
shown in a figure.

```
plot_data = []`
p.plotly_draw2d(plot_data)
```

The scatter plot is now added to plot_data.

`print(f"Plotted {len(plot_data)} scatter plots.")`

### 5) Create Plotly figure and show it

The simple `show2d` and `show3d` helper functions are a good starting point if you want to create your own
figures.  They are at the end of the `plot.py` file.

`sh2pl.show2d(plot_data)`

Plotly will use different mechanisms to show the plot  depending on your system.  It typically opens it in a browser.

## 2D Plotting

2D plotting is done via the `plotly_draw2d` method: `shapely_object.plotly_draw2d(plot_data, ...)`.

Create a Python list to hold the Plotly plots.  The `plotly_draw2d` method will append one or more plots to the 
list. Objects drawn later will be drawn over the top of earlier objects.

Call `shapely_plotly.show2d(plot_data)` to draw and show the figure.  It will return the figure drawn. If you want to build the figure, but not show it yet, set `plotly_draw2d(show=False)`.

All geometries are drawn using Plotly Scatter plots, `plotly.graph_objects.Scatter`. 2D 
plotting ignores the Shapely z-coordinates.

## 3D Plotting

3D plotting is done via the `plotly_draw3d` method: `shapely_object.plotly_draw3d(plot_data, ...)`.

The z-dimension is taken from Shapely's z-coordinates.  Shapely is a 2D geometry engine, but allows attaching
z-coordinates to points and vertices.  Shapely otherwise ignores the z-coordinate. If the z-coordinate of a point is 
not defined, Shapely to Plotly assumes a value of zero.

Create a Python list to hold the Plotly plots.  The `plotly_draw3d` method will append one or more plots to the 
list. Objects drawn later will be drawn over the top of earlier objects.

Call `shapely_plotly.show3d(plot_data)` to draw and show the figure.  It will return the figure drawn. If you 
want to build the figure, but not show it yet, set `plotly_draw3d(show=False)`.

All geometries are drawn using Plotly Scatter3D plots, `plotly.graph_objects.Scatter3D`.  

Mixing 2D and 3D plots in the same plot_data is not recommended.  It 
will functionally work, but will not produce visually appealing results.

## Using Styles

Shapely to Plotly has an extensive style system for controlling:

* Line styles (colors, widths, dashes, etc.)
* Vertex markers (shape, color, size, etc.)
* Fill colors
* Legend entries and object names
* Arbitrary arguments to be passed to the underlying Plotly calls 

There are two ways to use the style system, both of which may be used interchangeably.
1) Styles may be associated Shapely objects directly.  The associated style will be automatically applied when the object is plotted.
2) Styles may be provided as arguments to the `plotly_draw#d(...)` call.

Styles are cascading.  Every `Style` object may have a parent `Style`, and unspecified attributes will default to the parent's
style.  This allows you to define base styles, and then make derivatives off that style for specific categories of objects.

We first describe how styles are defined, and then describe how they are applied.  Finally we describe the details
of the cascading behavior.

### Style Attributes

The shapely_plotly.Style class holds all style information.  `Style` contains the following attributes.  

* `parent`:  The parent style which supplies default values.  See **Cascading Styles** below.

* `line_style`: Colors, width and dash mode for lines.  This used for LineString, LinearRing, MultiLineString, 
  and Polygon exterior line segments.  It is also used for any collection containing those elements.
                           `None` means no lines.

* `vertex_style`: Marker style used for the ends/vertices of lines.  This applies to the same geometries
                           as `line_style`.
                           `None` means no markers.

* `hole_line_style`:  The line style is used for internal holes/voids inside a polygon.
                           `None` means no lines.
        
* `hole_vertex_style`: The marker style is used for the vertices for holes/voids inside a polygon.
                           `None` means no markers.

* `fill_color`: The fill color used when drawing 2D polygons.  It is a Plotly string color name.
                           `None` means no fill.

* `point_style`: The marker style is used for Point/MultiPoint objects.
                           `None` will cause an assertion.

* `legend_group`:  A string name for a legend group.  All geometries in the same legend group will
                              be shown/hidden together in the Plotly interface.

* `scatter_kwargs`:  Arbitrary keyword arguments passed to Plotly's `Scatter(...)` plot, using Python's
                                `**kwargs` facility.  This provides a mechanism to access Plotly features not
 directly supported by Shapely to Plotly.  

These attributes can be set using named parameters when the `Style` is constructed:

```
style = Style(line_style = {...})
```

Or they can be modified later using accessors of the same name:

```commandline
style = Style()
style.line_style = {...}
```

The attributes may be a Plotly line style, marker style or color string.

#### Line Styles (`line_style`, `hole_line_style`)

Line styles maybe one of:

1) A dictionary mapping controls to values.  Plotly provides a large repertoire of controls.  Some common attributes are: 

* `"color"`: Color of the line, a Plotly color string
       
* `"width"`: Width of line in points, a number.

Example:
```commandline
style = Style(
   line_style = {
        "color":shapely_plotly.rgb(200,0,200, 0.5),
        "width":5
   }
)
```

2) A Plotly line style object.  For 2D plotting use `plotly.graph_objects.scatter.Line`.   
For 3D plotting use `plotly.graph_objects.scatter3d.Line`

Example:
```commandline
p_line_style = plotly.graph_objects.scatter.Line(...)
style = Style(
   line_style = p_line_style
)
```


Many other attributes are available.  See the Plotly documentation:
* https://plotly.com/python-api-reference/generated/plotly.graph_objects.scatter.html#plotly.graph_objects.scatter.Line
* https://plotly.github.io/plotly.py-docs/generated/plotly.graph_objects.scatter3d.html#plotly.graph_objects.scatter3d.Line

The same dictionary can be used for both 2D and 3D plotting, but intermixing Plotly 2D/3D line style objects will result
in a Plotly error.

#### Markers

Marker styles may be one of:

1) Dictionary mapping controls to values.  Plotly provides a large repertoire of controls.  Some common attributes are: 

* `"color"`: Color of marker as string.
* `"size"`:  Number.  Size of marker in points.
* `"symbol"`: String identifying symbol to use for the marker 
E.g 'circle', 'circle-open', 'cross', 'diamond', 'diamond-open', 'square', 'square-open', 'x'

2) A Plotly marker style object.  For 2D plotting use `plotly.graph_objects.scatter.Marker`.   
For 3D plotting use `plotly.graph_objects.scatter3d.Marker`

Many other attributes are available. See https://plotly.com/python/marker-style/ for details.

The same dictionary can be used for both 2D and 3D plotting, but intermixing 2D/3D Plotly marker style objects will result
in a Plotly error.

#### Colors

Plotly colors are strings.  The `shapely_plotly.rgb(...)` function provides a convenient way to build color strings
from RGB colors, including the alpha channel.

### Applying Styles

There are two ways styles can be applied to plots.  For either method the recommended usage
is to set up styles once at beginning, and then use those styles throughout the code.

Note that object style information is captured when the `plotly_draw*(...)` method is called.  Changes to `Styles`
after the draw method has been called will not dynamically alter plots nor have any effect.

#### Method 1: Apply the style to the Shapely geometry object

A `shapely_plotly.Style` object can be assigned to a geometry object using the `plotly_set_style` method.

```commandline
style = Style(...)
geometry.plotly_set_style(style)
```

Convenience functions also exist for all style attributes. For example:
```
geometry.plotly_set_line_style(...)
```

You do not need to set a style object first to use the convenience functions.

Note that the convenience function modify the style of the object, not merely that object.  So if multiple
objects share the same style, then all of them will be modified.

#### Method 2: Apply the style at the draw command.

Styles can be assigned when the `plotly_draw#(...)` method is called using the `style` keyword argument:

```commandline
style = Style(...)
goem.plotly_draw2d(style=style)
```

The `Style` given to the `plot_draw()` call will override any style assigned to the object.

### Cascading Styles

`Style` attributes may have a special value, `shapely_plotly.DEFAULT`, which means the style is not setting
that attribute.  In this case, the attribute
comes from the parent style, `Style.parent`.    Parent's can be arbitrarily nested, and
`shapely_plotly` will traverse parents until a value is found.

The `Style.parent` attribute may itself be `DEFAULT`, in which case the attribute comes from `shapely_plotly.default_style`, 
which is a legible if somewhat mundane style.

### Styles and Shapely Collections

Shapely has a number of classes for storing collections of geometries. 
* `MultiPoint`
* `MultiPolygon`
* `MultiLineString`
* `GeometryCollection`

In all cases, collections will be
plotted as a single object with a single name, legend group and style.  In fact, it is not possible to associate
names and styles with Shapely geometries inside of collections.  This is because Shapely creates a new
Python object every time a geometry is extracted from the collection, and hence will have no `Style` or name.

If you want individual styles or names for geometries inside a collection, you must store the geometry objects
separately in a suitable Python container and plot them individually.

### Plotly Scatter Arguments

This section provide reference information for how the `plotly.graph_objects.Scatter`/`Scatter3d` keyword arguments
are controlled by `shapely_plotly`.

See the Plotly documentation for a detailed understanding of these arguments.

* `line` - Controlled via `Style.line_style` or `Style.hole_line_style`.
* `marker` - Controlled via `Style.vertex_style`, `Style.hole_vertex_style` or `Style.point_style`.
* `mode` - Controlled based on whether the line style and/or point style is `None`.
* `fillcolor` - Controlled by `Style.fill_color`.  Only used for 2D polygons.
* `fill` - Set for filling 2D polygons only.
* `name` - Set to the object's name.
* `showlegend` - Set based on whether the object's name is `None`.
* `legendgroup` - Controlled by `Style.legend_group`.
In some cases `shapely_plotly` will create unique legend group names to internally tie objects together.

Any other arguments maybe set via the `Style.scatter_kwargs` facility. These 
keywords arguments are passed verbatim to `Scatter(...)` and are not
examined by `shapely_plotly`.  Do 
not set any of the keyword args listed above.
This will pass the same keyword argument twice, resulting in a Python error.


## Naming Objects and Legends

Shapely geometries may be named.  These names will appear as legend entries in the plots.  Legend entries can be
clicked to show/hide specific geometries.  

Names can be associated directly with Shapely objects, or the name may be given when `plotly_draw*(...)` is called.
The name given to the `plotly_draw*(...)` method will take precedence over previously assigned names.

To assign a name to a geometry use: `geom.plotly_set_name(name)`

To assign a name during at plot time, set the name parameter:  `geom.plotly_draw2d(plot_data, name=name)`

The name assigned at plot time will override any name assigned to the object.

If a name is assigned to the object, it will create a legend entry with that name for the object.  In Plotly,
clicking on legend entries will show/hide the objects.  If no name is assigned (or name is `None`), then no
legend entry will be created for the object.  It will always be visible.

Multiple objects can be associated together, so they are shown and hidden together in the Plotly 
interface. This is called a *legend group*.   The legend group is a string name for the group, 
and is set via `Style.legend_group`.  

Legend groups may also be assigned directly when plotting: `geom.plotly_draw2d(plot_data, legend_group=group_name)`

The associated objects may or may not have individual names, but at least one of the objects in the
group should have a name, or there will be no legend to control the visibility of the group.

This leads to four definable behaviors:

* **Name unset, legend group unset**.  No legend entry is created for the object.  It cannot be hidden.
* **Name set, legend group unset**.  A legend entry is created for the object.  The object can be individually hidden.
* **Name unset, legened group set**.  The 
object does not have a legend entry of its own, but can be hidden as part of the group. The 
group should have one (or more) objects with a name. A 
common usage is for one object in the group to have a name, and all the other objects to have their name unset.
* **Name set, legend group set**.  The object will have a legend entry. It can be hidden along with any other objects
in the group.

## Plotting Details for Shapely Geometries

Shapely objects are plotted as follows:

### `Point`
Points are plotted as a single scatter plot using markers only based on `Style.point_style`.

### `Polygon`
Polygons are complex in that they have an exterior polygon and zero or more internal holes or voids.

The exterior is plotted as a scatter plot using `Style.line_style` and `Style.vertex_style`.

For 2D plotting, all interior holes are plotted as a second scatter plot 
using `Style.hole_line_style` and `Style.hole_vertex_style`.  The fill is based on `Style.fill_color`.
Depending on the situation, this may require a third scatter plot.

For 3D plotting, all the holes are plotted as separate scatter plots 
using `Style.hole_line_style` and `Style.hole_vertex_style`.  Filling is not supported.

### `LineString`, `LinearRing`

Line strings and rings are plotted as a single scatter plot based on `Style.line_style` and `Style.vertex_style`.

### `MultiPoint`

MultiPoints are plotted as a single scatter plot using markers only based on `Style.point_style`.

### `MultiPolygon`

The polygones inside a `MultiPolygon` are all plotted individually, just like `Polygon`.  The style of the
`MultiPolygon` is used for all of them, and all of them are grouped under the name of the `MultiPolygon` if provided.
As described above, geometries contained in collections cannot have individual styles or names.

### `MultiLineString`

All the lines inside a MultiLineString are plotted as a single Scatter plot 
based on `Style.line_style` and `Stule.vertex_style`.

### `GeometryCollection`

All the geometries inside a `GeometryCollection` are plotted individually. The `Style` of the
`GeometryCollection` is used for all of them, and all of them are grouped under the name of the 
`GeometryCollection` if provided.
As described above, geometries contained in collections cannot have individual styles or names.
