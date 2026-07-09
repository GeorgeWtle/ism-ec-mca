from init.const import *
from init.lib import *
from init.func import *

from load_data.GCMs import pr_trend_JJAS, pr_change_JJAS

# MCA between pr_trend_JJAS and pr_change_JJAS
# LEFT FIELD X
box_X, mask_X, mval_X, left_lab = box_India_2, None, None, "IND2" # left: over EISM
# RIGHT FIELD Y
box_Y, mask_Y, mval_Y, right_lab = box_India_2, None, None, "IND2" # right: over EISM

X, Y, HM_X_SA, HM_X_init, HT_Y_SA, HT_Y_init, PC, EOF, HM_X, HM_Y, HT_X, HT_Y, expvar, expvar_pca = comp_HM_HT(
    pr_trend_JJAS, pr_change_JJAS,
    box_X = box_X, mask_X = mask_X, mval_X = mval_X,
    box_Y = box_Y, mask_Y = mask_Y, mval_Y = mval_Y
)

no_out = np.where(((PC["b"].isel(mode = 0) * -1) <= 2).values)[0]
out = np.where(((PC["b"].isel(mode = 0) * -1) > 2).values)[0]

# MCA between pr_trend_JJAS and pr_change_JJAS - NO OUTLIERS
# LEFT FIELD X
box_X, mask_X, mval_X, left_lab = box_India_2, None, None, "IND2" # left: over EISM
# RIGHT FIELD Y
box_Y, mask_Y, mval_Y, right_lab = box_India_2, None, None, "IND2" # right: over EISM

X_no_out, Y_no_out, HM_X_SA_no_out, HM_X_init_no_out, HT_Y_SA_no_out, HT_Y_init_no_out, PC_no_out, EOF_no_out, HM_X_no_out, HM_Y_no_out, HT_X_no_out, HT_Y_no_out, expvar_no_out, expvar_pca_no_out = comp_HM_HT(
    pr_trend_JJAS.isel(time = no_out), pr_change_JJAS.isel(time = no_out),
    box_X = box_X, mask_X = mask_X, mval_X = mval_X,
    box_Y = box_Y, mask_Y = mask_Y, mval_Y = mval_Y,
)

if X.units in ["mm day-1", "mm day-1 46 yr-1"] :
    cmap_X = "BrBG"
else :
    cmap_X = "RdBu_r"
if Y.units in ["mm day-1", "mm day-1 46 yr-1"] :
    cmap_Y = "BrBG"

if mask_X is None :
    rect_X = rect(box_X)
else :
    rect_X = rect(box_X, mask = mask_X, mval = mval_X)
if mask_Y is None :
    rect_Y = rect(box_Y)
else :
    rect_Y = rect(box_Y, mask = mask_Y, mval = mval_Y)

fig, axs = plt.subplots(
    subplot_kw = {'projection': ccrs.PlateCarree()},
    nrows = 3, ncols = 2,
    figsize = (TEXTWIDTH,TEXTWIDTH / 1.4)
)

weights = np.sqrt(np.cos(np.deg2rad(X.lat)))

EC_a_label = [f"a{i}" for i in range (4)]
EC_a_no_46_df = pd.DataFrame(
    [PC["a"].drop_sel(time = 46).isel(mode = i).values for i in range (4)],
    index = EC_a_label
).T # contains M ECs as columns

for m, m_lab in enumerate(["1st", "2nd"]) :

    plot_cartopy_contourf(
        crop(HM_X_init["slope"].isel(mode = m), box = box_Equatorial_India2) * -1,
        ax = axs[m, 0],
        min = -1, max = 1, step = 0.2,
        cmap = cmap_X,
        grid_labels = {"bottom": "x", "left": "y"},
        cbar_label = "mm day$^{-1}$ 46 yr$^{-1}$",
        cbar_ticks = np.arange(-1, 1.2, 0.2),
    )
    
    plot_pval(
        crop(HM_X_init["pval"].isel(mode = m), box = box_Equatorial_India2),
        ax = axs[m, 0],
        level = 0.05,
        fdr = True
    )
    
    axs[m, 0].add_geometries([rect_X], crs = ccrs.PlateCarree(), edgecolor = "red", facecolor = 'none', zorder = 10)

    plot_cartopy_contourf(
        crop(HT_Y_init["slope"].isel(mode = m), box_Equatorial_India2) * -1,
        ax = axs[m, 1],
        min = -1, max = 1, step = 0.2,
        cmap = cmap_Y,
        grid_labels = {"bottom": "x", "left": "y"},
        cbar_label = "mm day$^{-1}$",
        cbar_ticks = np.arange(-1, 1.2, 0.2),
    )

    plot_pval(
        crop(HT_Y_init["pval"].isel(mode = m), box = box_Equatorial_India2),
        ax = axs[m, 1],
        level = 0.05,
        fdr = True
    )

    axs[m, 1].add_geometries([rect_Y], crs = ccrs.PlateCarree(), edgecolor = "red", facecolor = 'none', zorder = 10)

plot_cartopy_contourf(
    crop(HM_X_init_no_out["slope"].isel(mode = 0), box = box_Equatorial_India2),
    ax = axs[2, 0],
    min = -1, max = 1, step = 0.2,
    cmap = cmap_X,
    grid_labels = {"bottom": "x", "left": "y"},
    cbar_label = "mm day$^{-1}$ 46 yr$^{-1}$",
    cbar_ticks = np.arange(-1, 1.2, 0.2),
)

plot_pval(
    crop(HM_X_init_no_out["pval"].isel(mode = 0), box = box_Equatorial_India2),
    ax = axs[2, 0],
    level = 0.05,
    fdr = True
)

axs[2, 0].add_geometries([rect_X], crs = ccrs.PlateCarree(), edgecolor = "red", facecolor = 'none', zorder = 10)

plot_cartopy_contourf(
    crop(HT_Y_init_no_out["slope"].isel(mode = 0), box = box_Equatorial_India2),
    ax = axs[2, 1],
    min = -1, max = 1, step = 0.2,
    cmap = cmap_Y,
    grid_labels = {"bottom": "x", "left": "y"},
    cbar_label = "mm day$^{-1}$",
    cbar_ticks = np.arange(-1, 1.2, 0.2),
)

plot_pval(
    crop(HT_Y_init_no_out["pval"].isel(mode = 0), box = box_Equatorial_India2),
    ax = axs[2, 1],
    level = 0.05,
    fdr = True
)

axs[2, 1].add_geometries([rect_Y], crs = ccrs.PlateCarree(), edgecolor = "red", facecolor = 'none', zorder = 10)

axs[0, 0].set_title("Homogeneous maps\n")
axs[0, 1].set_title("Heterogeneous maps\n")
axs[0, 0].annotate("1st mode", xy = (-0.22, 0.5), xycoords = 'axes fraction', rotation = "vertical", va = "center", ha = "center")
axs[1, 0].annotate("2nd mode", xy = (-0.22, 0.5), xycoords = 'axes fraction', rotation = "vertical", va = "center", ha = "center")
axs[2, 0].annotate("1st mode\n(no outliers)", xy = (-0.22, 0.5), xycoords = 'axes fraction', rotation = "vertical", va = "center", ha = "center")

axs_flat = axs.flatten()
for i in range (len(axs_flat)) :
    axs_flat[i].annotate(
        labels[i], xy = (0.05, 0.9), xycoords = 'axes fraction',
        va = "center", ha = "center",
        bbox = dict(boxstyle = "round", fc = "w", ec = "k", lw = 0.5),
        fontsize = 7
    )
    
plt.savefig("figures/fig6.pdf")