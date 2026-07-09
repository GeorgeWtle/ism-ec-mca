from init.const import *
from init.lib import *
from init.func import *

from load_data.obs import *
from load_data.GCMs import pr_clim_JJAS, pr_trend_JJAS

pr_clim_obs_JJAS = xr.concat(
    [
        pr_clim_ERA5_JJAS,
        pr_clim_GPCP_JJAS,
        pr_clim_CMAP_JJAS,
        pr_clim_MSWEP_JJAS
    ],
    dim = "obs"
)

pr_trend_obs_JJAS = xr.concat(
    [
        pr_trend_ERA5_JJAS,
        pr_trend_GPCP_JJAS,
        pr_trend_CMAP_JJAS,
        pr_trend_MSWEP_JJAS
    ],
    dim = "obs"
)

pr_trend_obs_JJAS_SA = crop(pr_trend_obs_JJAS, box = box_SAsia)

pr_trend_JJAS_SA = crop(pr_trend_JJAS, box = box_SAsia)

fig, axs = plt.subplots(
    subplot_kw = {'projection': ccrs.PlateCarree()},
    nrows = 3, ncols = 2,
    figsize = (COLUMNWIDTH, 0.87 * (COLUMNWIDTH * GOLDEN_RATIO))
)
axs_flat = axs.flatten()

for i, lab in enumerate(["ERA5", "GPCP", "CMAP", "MSWEP"]) :

    _, pval= ttest_1samp(pr_trend_JJAS_SA, pr_trend_obs_JJAS_SA.isel(obs = i), axis = 0)
    xarray_pval= xr.DataArray(
        data = pval,
        coords = {
            'lat': pr_trend_JJAS_SA.lat,
            'lon': pr_trend_JJAS_SA.lon
        }
    )
    
    map = plot_cartopy_contourf(
        pr_trend_JJAS_SA.mean(dim = "time") - pr_trend_obs_JJAS_SA.isel(obs = i),
        ax = axs_flat[i],
        min = -3, max = 3, num = 11,
        cmap = "BrBG",
        grid_labels = {"bottom": "x", "left": "y"},
        colorbar = False,
        title = lab,
        cbar_loc = "right",
        tickstep = 4
    )

map1 = plot_cartopy_contourf(
    pr_trend_JJAS_SA.mean(dim = "time") - pr_trend_obs_JJAS_SA.mean(dim = "obs"),
    ax = axs_flat[4],
    min = -3, max = 3, num = 11,
    cmap = "BrBG",
    grid_labels = {"bottom": "x", "left": "y"},
    colorbar = False,
    title = "Obs. average",
    cbar_loc = "right",
    tickstep = 4
)

map2 = plot_cartopy_contourf(
    pr_trend_obs_JJAS_SA.var(dim = "obs"),
    ax = axs_flat[5],
    min = 0.2, max = 3, num = 13,
    cmap = "GnBu",
    grid_labels = {"bottom": "x", "left": "y"},
    colorbar = False,
    title = "Obs. variance",
    cbar_loc = "right",
    tickstep = 4,
    undercolor = "white"
)

fig.subplots_adjust(hspace = 0.4, top = 0.95)

cbar1 = fig.colorbar(
    map1,
    ax = axs[:, 0],
    orientation = 'horizontal',
    fraction = 0.025,
    pad = 0.05,
    ticks = [-3, 0, 3],
    label = "mm day$^{-1}$ 46yr$^{-1}$"
)

cbar2 = fig.colorbar(
    map2,
    ax = axs[:, 1],
    orientation = 'horizontal',
    fraction = 0.025,
    pad = 0.05,
    ticks = [0.2, 1.6, 3],
    label = "(mm day$^{-1}$ 46yr$^{-1}$)$^2$"
)

for i in range (6) :
    axs_flat[i].annotate(
        labels[i], xy = (0.07, 0.9), xycoords = 'axes fraction',
        va = "center", ha = "center",
        bbox = dict(boxstyle = "round", fc = "w", ec = "k", lw = 0.5),
        fontsize = 7
    )

plt.savefig("figures/fig5.pdf")
plt.close()