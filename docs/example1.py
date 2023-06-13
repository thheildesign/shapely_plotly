
# Import shapely_plotly
import shapely_plotly as sh2pl

# Import shapely
import shapely as shp

# Importing plotly is not essential, unless you are adding plotly-specific details to the figures.

# After importing shapely_plotly, Shaply geometry classes will magically have new plotly_*(...) functions:
#   Plotting: plotly_draw2d, plotly_draw3d
#   Style (colors, lines, markers, etc.) management: plotly_get_*,  plotly_set_*
#   See docs and other examples for style management.
help(shp.Point.plotly_draw2d)

# Create a Shapely geometry as normal
poly_points = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0), (0.0, 0.0)]
p = shp.Polygon(shell=poly_points)

# The plotting routines add one or more Plotly scatter plots to a list.  The list of scatter plots are then plotted.
plot_data = []

# Plot the Shapely geometry
p.plotly_draw2d(plot_data)

# Note the scatter plot now added to plot_data.
print(f"Plotted {len(plot_data)} scatter plots.")

print("\nDrawing plots")
# Create Plotly figure and show it.
# The simple show2d and show3d helper functions are a good starting point if you want to create your own
# figures.  They are at the end of the plot.py file.
# Plotly will show the plot differently depending on your system.  It typically opens it in a browser.
sh2pl.show2d(plot_data)
