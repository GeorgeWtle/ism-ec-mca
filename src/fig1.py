from init.const import *
from init.lib import *
from init.func import *

from load_data.GCMs import pr_trend_JJAS_SA, pr_change_JJAS_SA, land_mask

fig, axs = plt.subplots(
    subplot_kw = {'projection': ccrs.PlateCarree()},
    nrows = 2, ncols = 2,
    figsize = (TEXTWIDTH, TEXTWIDTH / 1.5)
)

plot_cartopy_contourf(
    pr_trend_JJAS_SA.mean(dim = "time"),
    ax = axs[0, 0],
    min = -1, max = 1, num = 11,
    cmap = "BrBG",
    grid_labels = {"bottom": "x", "left": "y"},
    cbar_label = "mm day$^{-1}$ 46 yr$^{-1}$",
    title = "Summer precipitation trend",
    tickstep = 2
)
plot_cartopy_contourf(
    pr_change_JJAS_SA.mean(dim = "time"),
    ax = axs[0, 1],
    min = -3, max = 3, num = 13,
    cmap = "BrBG",
    grid_labels = {"bottom": "x", "left": "y"},
    cbar_label = "mm day$^{-1}$",
    title = "Summer precipitation change",
    tickstep = 2
)

axs[0, 0].add_geometries([rect_India], crs = ccrs.PlateCarree(), edgecolor = "red", facecolor = 'none', zorder = 10)
axs[0, 1].add_geometries([rect_India], crs = ccrs.PlateCarree(), edgecolor = "red", facecolor = 'none', zorder = 10)
axs[0, 0].add_geometries([rect_India_land], crs = ccrs.PlateCarree(), edgecolor = "royalblue", facecolor = 'none', zorder = 10, lw = 0.8, ls = "--")
axs[0, 1].add_geometries([rect_India_land], crs = ccrs.PlateCarree(), edgecolor = "royalblue", facecolor = 'none', zorder = 10, lw = 0.8, ls = "--")

plot_cartopy_contourf(
    pr_trend_JJAS_SA.var(dim = "time"),
    ax = axs[1, 0],
    min = 0.2, max = 3, num = 15,
    cmap = "GnBu",
    grid_labels = {"bottom": "x", "left": "y"},
    cbar_label = "(mm day$^{-1}$ 46 yr$^{-1}$)$^2$",
    undercolor = "white",
    tickstep = 2
)
plot_cartopy_contourf(
    pr_change_JJAS_SA.var(dim = "time"),
    ax = axs[1, 1],
    min = 1, max = 7, num = 13,
    cmap = "GnBu",
    grid_labels = {"bottom": "x", "left": "y"},
    cbar_label = "(mm day$^{-1}$)$^2$",
    undercolor = "white",
    tickstep = 2
)


axs[1, 1].add_geometries([rect_India], crs = ccrs.PlateCarree(), edgecolor = "red", facecolor = 'none', zorder = 10)
axs[1, 0].add_geometries([rect_India], crs = ccrs.PlateCarree(), edgecolor = "red", facecolor = 'none', zorder = 10)
axs[1, 0].add_geometries([rect_India_land], crs = ccrs.PlateCarree(), edgecolor = "royalblue", facecolor = 'none', zorder = 10, lw = 0.8, ls = "--")
axs[1, 1].add_geometries([rect_India_land], crs = ccrs.PlateCarree(), edgecolor = "royalblue", facecolor = 'none', zorder = 10, lw = 0.8, ls = "--")

axs[0, 0].annotate("Inter model mean", xy = (-0.3, 0.5), xycoords = 'axes fraction', rotation = "vertical", va = "center")
axs[1, 0].annotate("Inter model variance", xy = (-0.3, 0.5), xycoords = 'axes fraction', rotation = "vertical", va = "center")

axs_flat = axs.flatten()
for i in range (4) :
    axs_flat[i].annotate(
        labels[i], xy = (0.05, 0.92), xycoords = 'axes fraction',
        va = "center", ha = "center",
        bbox = dict(boxstyle = "round", fc = "w", ec = "k", lw = 0.5),
        fontsize = 7
    )

plt.savefig("figures/fig1.pdf")