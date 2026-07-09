from init.const import *
from init.lib import *
from init.func import *

from load_data.GCMs import pr_change_JJAS, pr_clim_JJAS, mean_tas_change,land_mask

# Mean change - mm/day
pr_change_JJAS_ind = crop(
    pr_change_JJAS,
    box = box_India_2
)
mean_pr_change_JJAS_ind = spatial_mean(
    pr_change_JJAS_ind,
    as_float = False
)

pr_change_JJAS_ind_land = crop(
    mask(pr_change_JJAS, land_mask, 1),
    box = box_India_2
)
mean_pr_change_JJAS_ind_land = spatial_mean(
    pr_change_JJAS_ind_land,
    as_float = False
)

y_mm_day = [
    mean_pr_change_JJAS_ind,
    mean_pr_change_JJAS_ind_land
]

# Mean change - %
pr_clim_JJAS_ind = crop(
    pr_clim_JJAS, 
    box = box_India_2
)
mean_pr_clim_JJAS_ind = spatial_mean(
    pr_clim_JJAS_ind,
    as_float = False
)

pr_clim_JJAS_ind_land = crop(
    mask(pr_clim_JJAS, land_mask, 1),
    box = box_India_2
)
mean_pr_clim_JJAS_ind_land = spatial_mean(
    pr_clim_JJAS_ind_land,
    as_float = False
)

y_pct = [
    (mean_pr_change_JJAS_ind / mean_pr_clim_JJAS_ind) * 100,
    (mean_pr_change_JJAS_ind_land / mean_pr_clim_JJAS_ind_land) * 100
]

# Mean change - %/°C
y_pct_C = [
    y / mean_tas_change for y in y_pct
]

print("---")
print("range (all):", y_mm_day[0].min().values, y_mm_day[0].max().values, "mm/day")
print("range (land):", y_mm_day[1].min().values, y_mm_day[1].max().values, "mm/day")
print("---")
print("range (all):", y_pct[0].min().values, y_pct[0].max().values, "%")
print("range (land):", y_pct[1].min().values, y_pct[1].max().values, "%")
print("---")
print("range (all):", y_pct_C[0].min().values, y_pct_C[0].max().values, "%/°C")
print("range (land):", y_pct_C[1].min().values, y_pct_C[1].max().values, "%/°C")

_, axs = plt.subplots(
    figsize = (COLUMNWIDTH * 1.2, COLUMNWIDTH * GOLDEN_RATIO / 1.3),
    nrows = 1, ncols = 3
)

plt.subplots_adjust(wspace = 0.45)

# mm/day

axs[0].grid(axis = "x", alpha = 0.75)
axs[0].hlines(y = 0, xmin = 0, xmax = 3, colors = "grey", alpha = 0.75, lw = 1)
axs[0].grid(axis = "y", alpha = 0.2)

y_temp  = np.linspace(-1, 5, 1000)
for i, y in enumerate(y_mm_day) :
    axs[0].plot([i+1]*len(y[CMIP6_True]), y[CMIP6_True], "o", ms = 1, color = "#0C7BDC", alpha = 0.75, zorder = 6) # CMIP6
    axs[0].plot([i+1]*len(y[~CMIP6_True]), y[~CMIP6_True], "o", ms = 1, color = "#FFC20A", alpha = 0.75, zorder = 6) # CMIP5

    norm_y_6 = norm.pdf(y_temp, loc = np.mean(y[CMIP6_True]), scale = np.std(y[CMIP6_True]))
    norm_y_6 /= 1.5 * norm_y_6.max()
    norm_y_5 = norm.pdf(y_temp, loc = np.mean(y[~CMIP6_True]), scale = np.std(y[~CMIP6_True]))
    norm_y_5 /= 1.5 * norm_y_5.max()
    axs[0].plot(-norm_y_6 + i + 1, y_temp, lw = 1, color = "#0C7BDC")
    axs[0].fill_betweenx(
        y = y_temp, x1 = -norm_y_6 + i + 1, x2 = [i+1] * len(norm_y_6),
        color = "#0C7BDC",
        alpha = 0.2
    )
    axs[0].plot(-norm_y_5 + i + 1, y_temp, lw = 1, color = "#FFC20A")
    axs[0].fill_betweenx(
        y = y_temp, x1 = -norm_y_5 + i + 1, x2 = [i+1] * len(norm_y_6),
        color = "#FFC20A",
        alpha = 0.2
    )

axs[0].boxplot(
    y_mm_day, tick_labels = ["Indian\ndomain", "land\nonly"], patch_artist = True,
    boxprops = {"color": "k", "facecolor": "k", "alpha": 0.5}, whiskerprops = {"color": "k"}, capprops = {"color": "k"}, medianprops = {"color": "k"}, flierprops = {"markeredgecolor": "k", "markerfacecolor": "k", "marker" : "o", "markersize": 3},
    widths = 0.2,
    zorder = 5
)

axs[0].set_xlim(0, 3)
axs[0].set_ylim(-1, 3.25)
axs[0].set_ylabel("Mean precipitation change")
axs[0].set_title("mm day$^{-1}$")

# %

axs[1].grid(axis = "x", alpha = 0.75)
axs[1].hlines(y = 0, xmin = 0, xmax = 3, colors = "grey", alpha = 0.75, lw = 1)
axs[1].grid(axis = "y", alpha = 0.2)

y_temp  = np.linspace(-40, 130, 1000)
for i, y in enumerate(y_pct) :
    axs[1].plot([i+1]*len(y[CMIP6_True]), y[CMIP6_True], "o", ms = 1, color = "#0C7BDC", alpha = 0.75, zorder = 6) # CMIP6
    axs[1].plot([i+1]*len(y[~CMIP6_True]), y[~CMIP6_True], "o", ms = 1, color = "#FFC20A", alpha = 0.75, zorder = 6) # CMIP5

    norm_y_6 = norm.pdf(y_temp, loc = np.mean(y[CMIP6_True]), scale = np.std(y[CMIP6_True]))
    norm_y_6 /= 1.5 * norm_y_6.max()
    norm_y_5 = norm.pdf(y_temp, loc = np.mean(y[~CMIP6_True]), scale = np.std(y[~CMIP6_True]))
    norm_y_5 /= 1.5 * norm_y_5.max()
    axs[1].plot(-norm_y_6 + i + 1, y_temp, lw = 1, color = "#0C7BDC")
    axs[1].fill_betweenx(
        y = y_temp, x1 = -norm_y_6 + i + 1, x2 = [i+1] * len(norm_y_6),
        color = "#0C7BDC",
        alpha = 0.2
    )
    axs[1].plot(-norm_y_5 + i + 1, y_temp, lw = 1, color = "#FFC20A")
    axs[1].fill_betweenx(
        y = y_temp, x1 = -norm_y_5 + i + 1, x2 = [i+1] * len(norm_y_6),
        color = "#FFC20A",
        alpha = 0.2
    )

axs[1].boxplot(
    y_pct, tick_labels = ["Indian\ndomain", "land\nonly"], patch_artist = True,
    boxprops = {"color": "k", "facecolor": "k", "alpha": 0.5}, whiskerprops = {"color": "k"}, capprops = {"color": "k"}, medianprops = {"color": "k"}, flierprops = {"markeredgecolor": "k", "markerfacecolor": "k", "marker" : "o", "markersize": 3},
    widths = 0.2,
    zorder = 5
)

axs[1].set_xlim(0, 3)
axs[1].set_ylim(-40, 130)
axs[1].set_title("\%")

# % / °C

axs[2].grid(axis = "x", alpha = 0.75)
axs[2].hlines(y = 0, xmin = 0, xmax = 3, colors = "grey", alpha = 0.75, lw = 1)
axs[2].grid(axis = "y", alpha = 0.2)

y_temp  = np.linspace(-40, 130, 1000)
for i, y in enumerate(y_pct_C) :
    axs[2].plot([i+1]*len(y[CMIP6_True]), y[CMIP6_True], "o", ms = 1, color = "#0C7BDC", alpha = 0.75, zorder = 6) # CMIP6
    axs[2].plot([i+1]*len(y[~CMIP6_True]), y[~CMIP6_True], "o", ms = 1, color = "#FFC20A", alpha = 0.75, zorder = 6) # CMIP5

    norm_y_6 = norm.pdf(y_temp, loc = np.mean(y[CMIP6_True]), scale = np.std(y[CMIP6_True]))
    norm_y_6 /= 1.5 * norm_y_6.max()
    norm_y_5 = norm.pdf(y_temp, loc = np.mean(y[~CMIP6_True]), scale = np.std(y[~CMIP6_True]))
    norm_y_5 /= 1.5 * norm_y_5.max()
    axs[2].plot(-norm_y_6 + i + 1, y_temp, lw = 1, color = "#0C7BDC")
    axs[2].fill_betweenx(
        y = y_temp, x1 = -norm_y_6 + i + 1, x2 = [i+1] * len(norm_y_6),
        color = "#0C7BDC",
        alpha = 0.2
    )
    axs[2].plot(-norm_y_5 + i + 1, y_temp, lw = 1, color = "#FFC20A")
    axs[2].fill_betweenx(
        y = y_temp, x1 = -norm_y_5 + i + 1, x2 = [i+1] * len(norm_y_6),
        color = "#FFC20A",
        alpha = 0.2
    )

axs[2].boxplot(
    y_pct_C, tick_labels = ["Extended\nIndian\ndomain", "Land\nonly"], patch_artist = True,
    boxprops = {"color": "k", "facecolor": "k", "alpha": 0.5}, whiskerprops = {"color": "k"}, capprops = {"color": "k"}, medianprops = {"color": "k"}, flierprops = {"markeredgecolor": "k", "markerfacecolor": "k", "marker" : "o", "markersize": 3},
    widths = 0.2,
    zorder = 5
)

axs[2].set_xlim(0, 3)
axs[2].set_ylim(-10, 32.5)
axs[2].set_title("\% °C$^{-1}$")

# Legend
axs[1].hist([], color = "grey", alpha = 1, label = "CMIP5 and CMIP6")
axs[1].hist([], color = "#0C7BDC", alpha = 0.5, label = "CMIP6")
axs[1].hist([], color = "#FFC20A", alpha = 0.5, label = "CMIP5")

for i in range(3) :
    axs[i].set_xticklabels(labels = ["EISM\ndomain", "ISM\ndomain"], fontsize = 5, rotation = 0)

plt.figlegend(ncols = 3, loc = "lower center", bbox_to_anchor = (0.5, -0.06))

axs_flat = axs.flatten()
for i in range (len(axs_flat)) :
    axs_flat[i].annotate(
        labels[i], xy = (0.15, 0.96), xycoords = 'axes fraction',
        va = "center", ha = "center",
        bbox = dict(boxstyle = "round", fc = "w", ec = "k", lw = 0.5),
        fontsize = 7
    )

plt.savefig("figures/fig2.pdf")