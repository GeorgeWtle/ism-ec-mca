from init.const import *
from init.lib import *
from init.func import *

from process.LOOCV import M, Y_hat, MSE
from load_data.GCMs import pr_change_JJAS_SA

MSE_india = crop(MSE, box = box_India_2)
MSE_india_land = mask(MSE_india, mask = crop(land_mask, box = box_India_2), mval = 1)
MSE_india_sea = mask(MSE_india, mask = crop(land_mask, box = box_India_2), mval = 0)

var_eps = ((pr_change_JJAS_SA - Y_hat).var(dim = "time"))
var_eps_india = crop(var_eps, box = box_India_2)
var_eps_india_land = mask(var_eps_india, mask = crop(land_mask, box = box_India_2), mval = 1)
var_eps_india_sea = mask(var_eps_india, mask = crop(land_mask, box = box_India_2), mval = 0)

var_Y = pr_change_JJAS_SA.var(dim = "time")
var_Y_india = crop(var_Y, box = box_India_2)
var_Y_india_land = mask(var_Y_india, mask = crop(land_mask, box = box_India_2), mval = 1)
var_Y_india_sea = mask(var_Y_india, mask = crop(land_mask, box = box_India_2), mval = 0)

percentile = 10
m = 2

var_eps_var_Y_m = (var_eps_india.sel(nb_of_mode = m) / var_Y_india).values.flatten() * 100
var_eps_var_Y_m = var_eps_var_Y_m[~np.isnan(var_eps_var_Y_m)]

var_eps_var_Y_land_m = (var_eps_india_land.sel(nb_of_mode = m) / var_Y_india_land).values.flatten() * 100
var_eps_var_Y_land_m = var_eps_var_Y_land_m[~np.isnan(var_eps_var_Y_land_m)]

var_eps_var_Y_sea_m = (var_eps_india_sea.sel(nb_of_mode = m) / var_Y_india_sea).values.flatten() * 100
var_eps_var_Y_sea_m = var_eps_var_Y_sea_m[~np.isnan(var_eps_var_Y_sea_m)]

print(
    f"Percentile {percentile} for total PR  :",
    100 - np.percentile(var_eps_var_Y_m, percentile), "%"
)
print(
    f"Percentile {percentile} for land PR   :",
    100 - np.percentile(var_eps_var_Y_land_m, percentile), "%"
)

print(
    f"Percentile {percentile} for sea PR    :",
    100 - np.percentile(var_eps_var_Y_sea_m, percentile), "%"
)

print(
    f"Mean reduction for total PR   :",
    100 - np.mean(var_eps_var_Y_m), "%"
)

print(
    f"Mean reduction for land PR    :",
    100 - np.mean(var_eps_var_Y_land_m), "%"
)

print(
    f"Mean reduction for sea PR     :",
    100 - np.mean(var_eps_var_Y_sea_m), "%"
)

target = 33

print(
    ((100 - var_eps_var_Y_m >= target).sum() / len(var_eps_var_Y_m)) * 100,
    f"% of total grid points suggest at least a reduction of {target} %"
)

print(
    ((100 - var_eps_var_Y_land_m >= target).sum() / len(var_eps_var_Y_land_m)) * 100,
    f"% of land  grid points suggest at least a reduction of {target} %"
)

print(
    ((100 - var_eps_var_Y_sea_m >= target).sum() / len(var_eps_var_Y_sea_m)) * 100,
    f"% of sea   grid points suggest at least a reduction of {target} %"
)

colors_box2 = ["red","royalblue", "green"]
modes_colors = ["red"] * 5

fig, axs = plt.subplots(
    nrows = 1, ncols = 2,
    figsize = (TEXTWIDTH, TEXTWIDTH / 2),
)

### Efficiency - Var(eps)/Var(y) ###

axs[0].set_title(r"$Var(\boldsymbol{\mathsf{E}}^{(m)}) \big / Var(\boldsymbol{\mathsf{Y}})$")

axs[0].hlines(y = 100, xmin = 0, xmax = M+1, lw = 1, colors = "k", alpha = 0.5)

x = np.linspace(0, 150, 1000)

for m in range (M) :
    
    var_eps_var_Y_m = (var_eps_india.isel(nb_of_mode = m) / var_Y_india).values.flatten() * 100
    var_eps_var_Y_m = var_eps_var_Y_m[~np.isnan(var_eps_var_Y_m)]
    kde_var_eps = gaussian_kde(var_eps_var_Y_m)
    kde_var_eps_np = kde_var_eps(x)
    kde_var_eps_np /= 1.3 * kde_var_eps_np.max()

    var_eps_var_Y_land_m = (var_eps_india_land.isel(nb_of_mode = m) / var_Y_india_land).values.flatten() * 100
    var_eps_var_Y_land_m = var_eps_var_Y_land_m[~np.isnan(var_eps_var_Y_land_m)]
    kde_var_eps_land = gaussian_kde(var_eps_var_Y_land_m)
    kde_var_eps_land_np = kde_var_eps_land(x)
    kde_var_eps_land_np /= 1.3 * kde_var_eps_land_np.max()
    kde_var_eps_land_np /= 2
    
    var_eps_var_Y_sea_m = (var_eps_india_sea.isel(nb_of_mode = m) / var_Y_india_sea).values.flatten() * 100
    var_eps_var_Y_sea_m = var_eps_var_Y_sea_m[~np.isnan(var_eps_var_Y_sea_m)]
    kde_var_eps_sea = gaussian_kde(var_eps_var_Y_sea_m)
    kde_var_eps_sea_np = kde_var_eps_sea(x)
    kde_var_eps_sea_np /= 1.3 * kde_var_eps_sea_np.max()
    kde_var_eps_sea_np /= 2
    
    axs[0].plot(-kde_var_eps_land_np + 1 + m, x, color = colors_box2[1], alpha = 1, lw = 0.75, ls = "--")
    axs[0].plot(-kde_var_eps_sea_np + 1 + m, x, color = colors_box2[2], alpha = 1, lw = 0.75, ls = "--")
    axs[0].plot(-kde_var_eps_np + 1 + m, x, color = modes_colors[m])
    axs[0].fill_betweenx(
        y = x, x1 = -kde_var_eps_np + 1 + m, x2 = [m + 1] * len(kde_var_eps_np),
        color = modes_colors[m], alpha = 0.3
    )
    axs[0].boxplot(
        var_eps_var_Y_m, positions = [m + 1], patch_artist = True,
        boxprops = {"color": colors["red"][5], "facecolor": colors["red"][3]}, whiskerprops = {"color": colors["red"][5]}, capprops = {"color": colors["red"][5]}, medianprops = {"color": colors["red"][5]}, flierprops = {"markeredgecolor": colors["red"][5], "markerfacecolor": colors["red"][5], "marker" : "o", "markersize": 1.5},
        widths = 0.1,
        zorder = 10
    )
    axs[0].scatter([m+1], spatial_mean(var_eps_india / var_Y_india, as_float = False).isel(nb_of_mode = m) * 100, s = 2, color = modes_colors[m], zorder = 51)


axs[0].plot([i for i in range (1, M+1)], spatial_mean(var_eps_india / var_Y_india, as_float = False).values * 100, "o-", lw = 1, ms = 3, color = "k", zorder = 50)

axs[0].grid(axis = "both", alpha = 0.5)
axs[0].set_ylabel("\%")
axs[0].set_xticks([i for i in range (1, M+1)])
axs[0].set_xlabel("Number of modes")
axs[0].set_xlim(0, M+0.5)
axs[0].set_ylim(20, 140)

####################################

### Robustness - MSE/Var(eps) ######

axs[1].set_title(r"$\boldsymbol{\mathrm{MSE}}^{(m)} \big / Var(\boldsymbol{\mathsf{Y}})$")

axs[1].hlines(y = 100, xmin = 0, xmax = M+1, lw = 1, colors = "k", alpha = 0.5)

y = np.linspace(0, 150, 1000)

for m in range (M) :

    MSE_var_Y_m =  (MSE_india.isel(nb_of_mode = m) / var_Y_india).values.flatten() * 100
    MSE_var_Y_m = MSE_var_Y_m[~np.isnan(MSE_var_Y_m)]
    kde_MSE = gaussian_kde(MSE_var_Y_m)
    kde_MSE_np = kde_MSE(y)
    kde_MSE_np /= 1.3 * kde_MSE_np.max()
    MSE_var_Y_m_rbst_frac = ((MSE_var_Y_m < 100).sum() / len(MSE_var_Y_m)) * 100
    
    MSE_var_Y_land_m =  (MSE_india_land.isel(nb_of_mode = m) / var_Y_india_land).values.flatten() * 100
    MSE_var_Y_land_m = MSE_var_Y_land_m[~np.isnan(MSE_var_Y_land_m)]
    kde_MSE_land = gaussian_kde(MSE_var_Y_land_m)
    kde_MSE_land_np = kde_MSE_land(y)
    kde_MSE_land_np /= 1.3 * kde_MSE_land_np.max()
    kde_MSE_land_np /= 2
    MSE_var_Y_land_m_rbst_frac = ((MSE_var_Y_land_m < 100).sum() / len(MSE_var_Y_land_m)) * 100
    
    MSE_var_Y_sea_m =  (MSE_india_sea.isel(nb_of_mode = m) / var_Y_india_sea).values.flatten() * 100
    MSE_var_Y_sea_m = MSE_var_Y_sea_m[~np.isnan(MSE_var_Y_sea_m)]
    kde_MSE_sea = gaussian_kde(MSE_var_Y_sea_m)
    kde_MSE_sea_np = kde_MSE_sea(y)
    kde_MSE_sea_np /= 1.3 * kde_MSE_sea_np.max()
    kde_MSE_sea_np /= 2
    MSE_var_Y_sea_m_rbst_frac = ((MSE_var_Y_sea_m < 100).sum() / len(MSE_var_Y_sea_m)) * 100

    axs[1].plot(-kde_MSE_land_np + 1 + m, y, color = colors_box2[1], alpha = 1, lw = 0.75, ls = "--")
    axs[1].plot(-kde_MSE_sea_np + 1 + m, y, color = colors_box2[2], alpha = 1, lw = 0.75, ls = "--")
    axs[1].plot(-kde_MSE_np + 1 + m, y, color = modes_colors[m])
    axs[1].fill_betweenx(
        y = y, x1 = -kde_MSE_np + 1 + m, x2 = [m + 1] * len(kde_MSE_np),
        color = modes_colors[m], alpha = 0.3
    )
    axs[1].boxplot(
        MSE_var_Y_m, positions = [m + 1], patch_artist = True,
        boxprops = {"color": colors["red"][5], "facecolor": colors["red"][3]}, whiskerprops = {"color": colors["red"][5]}, capprops = {"color": colors["red"][5]}, medianprops = {"color": colors["red"][5]}, flierprops = {"markeredgecolor": colors["red"][5], "markerfacecolor": colors["red"][5], "marker" : "o", "markersize": 1.5},
        widths = 0.1,
        zorder = 10
    )
    axs[1].scatter([m+1], spatial_mean(MSE_india / var_Y_india, as_float = False).isel(nb_of_mode = m) * 100, s = 2, color = modes_colors[m], zorder = 51)
    
    axs[1].annotate(f"{int(MSE_var_Y_m_rbst_frac)}\%", color = colors_box2[0], xy = (m+1, 40), va = "center", ha = "center", fontsize = 5, bbox = dict(fc = "w", ec = "w", pad = 0.2))
    axs[1].annotate(f"{int(MSE_var_Y_land_m_rbst_frac)}\%", color = colors_box2[1], xy = (m+1, 34), va = "center", ha = "center", fontsize = 5, bbox = dict(fc = "w", ec = "w", pad = 0.2))
    axs[1].annotate(f"{int(MSE_var_Y_sea_m_rbst_frac)}\%", color = colors_box2[2], xy = (m+1, 28), va = "center", ha = "center", fontsize = 5, bbox = dict(fc = "w", ec = "w", pad = 0.2))

axs[1].plot([i for i in range (1, M+1)], spatial_mean(MSE_india / var_Y_india, as_float = False).values * 100, "o-", lw = 1, ms = 3, color = "k", zorder = 50)

# Legend
axs[0].plot([], [], color = colors_box2[1], ls = "--", label = "Land only")
axs[0].plot([], [], color = colors_box2[2], ls = "--", label = "Ocean only")

axs[1].grid(axis = "both", alpha = 0.5)
axs[1].set_ylabel("\%")
axs[1].set_xticks([i for i in range (1, M+1)])
axs[1].set_xlabel("Number of modes")
axs[1].set_xlim(0, M+0.5)
axs[1].set_ylim(20, 140)

plt.subplots_adjust(wspace = 0.3)

plt.figlegend(ncols = 2, loc = "lower center", bbox_to_anchor = (0.5, -0.12))

axs_flat = axs.flatten()
for i in range (len(axs_flat)) :
    axs_flat[i].annotate(
        labels[i], xy = (0.05, 0.95), xycoords = 'axes fraction',
        va = "center", ha = "center",
        bbox = dict(boxstyle = "round", fc = "w", ec = "k", lw = 0.5),
        fontsize = 7
    )

plt.savefig("figures/fig10.pdf")