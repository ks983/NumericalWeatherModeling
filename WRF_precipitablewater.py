from netCDF4 import Dataset
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import cartopy.crs as crs
from cartopy.feature import NaturalEarthFeature

from wrf import (to_np, getvar, smooth2d, get_cartopy, cartopy_xlim,
                 cartopy_ylim, latlon_coords)

# Import WRF outputs
data = Dataset("wrfout_d01_2016-10-07_00_00_00")

# Get precipitable water variable
pw = getvar(data, "pw")

# Get coordinates
lats, lons = latlon_coords(pw)

# Get the mapping object
cart_proj = get_cartopy(pw)

# Create figure
fig = plt.figure(figsize=(12,6))

# Set the GeoAxes to the projection used by WRF
ax = plt.axes(projection=cart_proj)

# Download and add the states and coastlines
states = NaturalEarthFeature(category="cultural", scale="50m",
                             facecolor="none",
                             name="admin_1_states_provinces_shp")
ax.add_feature(states, linewidth=.5, edgecolor="black")
ax.coastlines('50m', linewidth=0.8)

# Add contour lines and filled contours for the variable
plt.contour(to_np(lons), to_np(lats), to_np(pw), 10, colors="black",
            transform=crs.PlateCarree())
plt.contourf(to_np(lons), to_np(lats), to_np(pw), 10,
             transform=crs.PlateCarree(),
             cmap=get_cmap("jet"))

# Add a color bar
plt.colorbar(ax=ax, shrink=.98)

# Set the map bounds
ax.set_xlim(cartopy_xlim(pw))
ax.set_ylim(cartopy_ylim(pw))

# Add the gridlines
ax.gridlines(color="black", linestyle="dotted")

plt.title("Precipitable Water (kg m-2")

plt.show()

plt.savefig("precipitablewater.png")


https://github.com/ks983/ClimateModeling/issues/1#issue-855417436
