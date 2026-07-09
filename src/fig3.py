from init.const import *
from init.lib import *
from init.func import *

from load_data.GCMs import pr_trend_JJAS, pr_change_JJAS, land_mask
from load_data.GCMs import tas_TS, tas_NH_TS, tas_SH_TS, tas_AMTG_N_TS, tas_AMTG_S_TS

pr_trend_JJAS_trop, pr_change_JJAS_trop = crop(pr_trend_JJAS, box_Trop), crop(pr_change_JJAS, box_Trop)

# 1. Correlation between JJAS pr trend and JJAS pr change
corr_pr_trend_change_JJAS_trop = xr.corr(
    pr_trend_JJAS_trop,
    pr_change_JJAS_trop,
    dim = "time"
)

# 2. Correlation between GMT trend and JJAS pr change
tas_TS_Y = tas_TS.resample(time = "1YE").mean()
tas_TS_Y_1979_2024_trend = temporal_regression(
    tas_TS_Y
    .sel(time = slice("1979", "2024"))
    .groupby("time.year")
    .mean(dim = "time")
)["slope"]

tas_TS_Y_1979_2024_trend_std = tas_TS_Y_1979_2024_trend / tas_TS_Y_1979_2024_trend.std()
tas_TS_Y_1979_2024_trend_std = tas_TS_Y_1979_2024_trend_std.rename({"model": "time"})

corr_GMT = xr.corr(
    tas_TS_Y_1979_2024_trend_std.assign_coords(time=np.arange(69)),
    pr_change_JJAS_trop,
    dim = "time"
)

# 3. Correlation between ITHG trend and JJAS pr change
tas_TS_ITHG = tas_NH_TS - tas_SH_TS
tas_TS_ITHG_Y = tas_TS_ITHG.resample(time = "1YE").mean()
tas_TS_ITHG_Y_1979_2024_trend = temporal_regression(
    tas_TS_ITHG_Y
    .sel(time = slice("1979", "2024"))
    .groupby("time.year")
    .mean(dim = "time")
)["slope"]

tas_TS_ITHG_Y_1979_2024_trend_std = tas_TS_ITHG_Y_1979_2024_trend / tas_TS_ITHG_Y_1979_2024_trend.std()
tas_TS_ITHG_Y_1979_2024_trend_std = tas_TS_ITHG_Y_1979_2024_trend_std.rename({"model": "time"})

corr_ITHG = xr.corr(
    tas_TS_ITHG_Y_1979_2024_trend_std.assign_coords(time=np.arange(69)),
    pr_change_JJAS_trop,
    dim = "time"
)

# 4. Correlation between AMTG trend and JJAS pr change
tas_TS_AMTG = tas_AMTG_N_TS - tas_AMTG_S_TS
tas_TS_AMTG_Y = tas_TS_AMTG.resample(time = "1YE").mean()
tas_TS_AMTG_Y_1979_2024_trend = temporal_regression(
    tas_TS_AMTG_Y
    .sel(time = slice("1979", "2024"))
    .groupby("time.year")
    .mean(dim = "time")
)["slope"]

tas_TS_AMTG_Y_1979_2024_trend_std = tas_TS_AMTG_Y_1979_2024_trend / tas_TS_AMTG_Y_1979_2024_trend.std()
tas_TS_AMTG_Y_1979_2024_trend_std = tas_TS_AMTG_Y_1979_2024_trend_std.rename({"model": "time"})

corr_AMTG = xr.corr(
    tas_TS_AMTG_Y_1979_2024_trend_std.assign_coords(time=np.arange(69)),
    pr_change_JJAS_trop,
    dim = "time"
)

corr_list = [
    corr_pr_trend_change_JJAS_trop,
    corr_GMT,
    corr_ITHG,
    corr_AMTG
]

pval_list = []
n = pr_trend_JJAS_trop.time.size

for corr in corr_list :
    
    t_stat = corr * np.sqrt((n - 2) / (1 - corr**2))
    corr_pval = xr.apply_ufunc(
        lambda x: 2 * (1 - t.cdf(np.abs(x), df = n - 2)),
        t_stat,
        vectorize = True,
        dask = "parallelized",
        output_dtypes = [float],
    )

    corr_pval.name = "p_value"
    pval_list.append(corr_pval)

fig, axs = plt.subplots(
    subplot_kw = {'projection': ccrs.PlateCarree()},
    nrows = 4, ncols = 1,
    figsize = (COLUMNWIDTH, COLUMNWIDTH * 0.7 * GOLDEN_RATIO)
)

grid_labels = {"left": "y"}

for i in range(4) :
    
    corr = corr_list[i]
    pval = pval_list[i]
    
    if i == 3 :
        grid_labels = {"bottom": "x", "left": "y"}

    map = plot_cartopy_contourf(
        corr,
        ax = axs[i],
        min = -1, max = 1, step = 0.25,
        cmap = "RdBu",
        grid = True,
        grid_labels = grid_labels,
        colorbar = False,
    )

    plot_pval(
        pval,
        ax = axs[i],
        level = 0.05,
        fdr = True,
        pattern = "...."
    )
    
    axs[i].add_geometries([rect_India], crs = ccrs.PlateCarree(), edgecolor = "red", facecolor = 'none', zorder = 10)

for i, lab in enumerate(["Correlation with future ISMR change\n\nPrecipitation trends", "GMT trend", "IHTG trends", "AMTG trends"]) :
    axs[i].set_title(lab)

cbar = fig.colorbar(
    map,
    ax = axs, 
    orientation = "horizontal",
    location = "bottom",
    pad = 0.08, 
    fraction = 0.05
)
cbar.set_label(r"$\rho$")

axs_flat = axs.flatten()
for i in range (4) :
    axs_flat[i].annotate(
        labels[i], xy = (0.03, 0.75), xycoords = 'axes fraction',
        va = "center", ha = "center",
        bbox = dict(boxstyle = "round", fc = "w", ec = "k", lw = 0.5),
        fontsize = 7,
        zorder = 1001
    )

plt.savefig("figures/fig3.pdf")