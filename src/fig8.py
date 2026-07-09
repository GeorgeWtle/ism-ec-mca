from init.const import *
from init.lib import *
from init.func import *

from load_data.obs import *
from load_data.GCMs import pr_trend_JJAS, pr_change_JJAS, pr_clim_JJAS, pr_trend_JJAS_MIROC6, pr_change_JJAS_MIROC6, pr_clim_JJAS_MIROC6
from load_data.GCMs import tas_clim_JJAS, ua850_clim_JJAS, va850_clim_JJAS

CMIP6_True = np.array(pr_trend_JJAS.models_CMIP6).astype(bool)
CMIP6_True_no_46 = np.delete(CMIP6_True, 46)

# MCA between pr_trend_JJAS and pr_change_JJAS
# LEFT FIELD X: pr_trend_JJAS
box_X, mask_X, mval_X, left_lab = box_India_2, None, None, "IND2" # left: over EISM
# RIGHT FIELD Y: pr_change_JJAS
box_Y, mask_Y, mval_Y, right_lab = box_India_2, None, None, "IND2" # right: over EISM

X, Y, HM_X_SA, HM_X_init, HT_Y_SA, HT_Y_init, PC, EOF, HM_X, HM_Y, HT_X, HT_Y, expvar, expvar_pca = comp_HM_HT(
    pr_trend_JJAS, pr_change_JJAS,
    box_X = box_X, mask_X = mask_X, mval_X = mval_X,
    box_Y = box_Y, mask_Y = mask_Y, mval_Y = mval_Y
)

no_out = np.where(((PC["b"].isel(mode = 0) * -1) <= 2).values)[0]
out = np.where(((PC["b"].isel(mode = 0) * -1) > 2).values)[0]

X_MIROC6 = crop(pr_trend_JJAS_MIROC6 , box = box_X)
Y_MIROC6 = crop(pr_change_JJAS_MIROC6 , box = box_X)

pr_trend_obs_JJAS_list = [
    pr_trend_ERA5_JJAS,
    pr_trend_GPCP_JJAS,
    pr_trend_CMAP_JJAS,
    pr_trend_MSWEP_JJAS
]
    
pr_trend_obs_JJAS = xr.concat(
    pr_trend_obs_JJAS_list,
    dim = "obs"
)
pr_trend_obs_JJAS = xr.concat(
    pr_trend_obs_JJAS_list + [pr_trend_obs_JJAS.mean(dim = "obs")],
    dim = "obs"
)
pr_trend_obs_JJAS.attrs["dataset"] = ["ERA5", "GPCP", "MSWEP", "CMAP", "Mean"]
X_obs = crop(pr_trend_obs_JJAS, box = box_X)

# PCA with pr_clim_JJAS
# LEFT FIELD X: pr_clim_JJAS
box_X2, mask_X2, mval_X2, left_lab2 = box_Equatorial_India, None, None, "TROP"

# RIGHT FIELD Y: pr_clim_JJAS
box_Y2, mask_Y2, mval_Y2, right_lab2 = box_Equatorial_India, None, None, "TROP"

X2, Y2, HM_X_SA2, HM_X_init2, HT_Y_SA2, HT_Y_init2, PC2, EOF2, HM_X2, HM_Y2, HT_X2, HT_Y2, expvar2, expvar_pca2 = comp_HM_HT(
    pr_clim_JJAS, pr_clim_JJAS,
    box_X = box_X2, mask_X = mask_X2, mval_X = mval_X2,
    box_Y = box_Y2, mask_Y = mask_Y2, mval_Y = mval_Y2,
)

pr_clim_obs_JJAS_list = [
    pr_clim_ERA5_JJAS,
    pr_clim_GPCP_JJAS,
    pr_clim_CMAP_JJAS,
    pr_clim_MSWEP_JJAS
]
    
pr_clim_obs_JJAS = xr.concat(
    pr_clim_obs_JJAS_list,
    dim = "obs"
)
pr_clim_obs_JJAS = xr.concat(
    pr_clim_obs_JJAS_list + [pr_clim_obs_JJAS.mean(dim = "obs")],
    dim = "obs"
)
pr_clim_obs_JJAS.attrs["dataset"] = ["ERA5", "GPCP", "MSWEP", "CMAP", "Mean"]
X2_obs = crop(pr_clim_obs_JJAS, box = box_X2)

X2_MIROC6 = crop(pr_clim_JJAS_MIROC6 , box = box_X2)

if X2.units in ["mm day-1", "mm day-1 46 yr-1"] :
    cmap_X2 = "BrBG"
else :
    cmap_X2 = "RdYlBu_r"
if Y2.units in ["mm day-1", "mm day-1 46 yr-1"] :
    cmap_Y2 = "BrBG"

if mask_X2 is None :
    rect_X2 = rect(box_X2)
else :
    rect_X2 = rect(box_X2, mask = mask_X2, mval = mval_X2)
if mask_Y2 is None :
    rect_Y2 = rect(box_Y2)
else :
    rect_Y2 = rect(box_Y2, mask = mask_Y2, mval = mval_Y2)

fig = plt.figure(figsize = (TEXTWIDTH, TEXTWIDTH / 1.5))

gs = gridspec.GridSpec(
    2, 2,
    figure = fig,
    wspace=0.3
)
ax_map1 = fig.add_subplot(gs[0, 0], projection = ccrs.PlateCarree(180))
ax_map2 = fig.add_subplot(gs[0, 1], projection = ccrs.PlateCarree(180))
ax_sc1 = fig.add_subplot(gs[1, 0])
ax_sc2 = fig.add_subplot(gs[1, 1])
axs = [ax_map1, ax_map2, ax_sc1, ax_sc2]

EC2_a_label = [f"a{i}" for i in range (4)]
EC2_a_df = pd.DataFrame(
    [PC2["a"].isel(mode = i).values for i in range (4)],
    index = EC2_a_label
).T # contains M ECs as columns

EC2_a_no_46_df = pd.DataFrame(
    [PC2["a"].drop_sel(time = 46).isel(mode = i).values for i in range (4)],
    index = EC2_a_label
).T # contains M ECs as columns

gamma_clim_TAS_ds = qr_multiple_reg(tas_clim_JJAS, EC2_a_df)
gamma_clim_PR_ds = qr_multiple_reg(pr_clim_JJAS, EC2_a_df)
gamma_clim_ua850_ds = qr_multiple_reg(ua850_clim_JJAS.drop_sel(time = 46), EC2_a_no_46_df)
gamma_clim_va850_ds = qr_multiple_reg(va850_clim_JJAS.drop_sel(time = 46), EC2_a_no_46_df)

reg_map_clim_TAS = gamma_clim_TAS_ds.sel(nb_of_mode = 1).sel(coef = f"a0")
reg_map_clim_PR = gamma_clim_PR_ds.sel(nb_of_mode = 1).sel(coef = f"a0")
reg_map_clim_ua850 = gamma_clim_ua850_ds.sel(nb_of_mode = 1).sel(coef = f"a0")
reg_map_clim_va850 = gamma_clim_va850_ds.sel(nb_of_mode = 1).sel(coef = f"a0")

pval_ua850_clim_temp = false_discovery_control(np.nan_to_num(reg_map_clim_ua850["pval"], nan = 1))
pval_ua850_clim = xr.zeros_like(reg_map_clim_ua850["pval"])
pval_ua850_clim.values = pval_ua850_clim_temp

pval_va850_clim_temp = false_discovery_control(np.nan_to_num(reg_map_clim_va850["pval"], nan = 1))
pval_va850_clim = xr.zeros_like(reg_map_clim_va850["pval"])
pval_va850_clim.values = pval_va850_clim_temp

plot_cartopy_contourf(
    crop(HM_X_init2["slope"].isel(mode = 0), box = [40, 280, -60, 40]),
    ax = axs[0],
    min = -1, max = 1, step = 0.2,
    cmap = "BrBG",
    grid_labels = {"top": "x", "left": "y"},
    title = "Regression with precipitation mean state",
    cbar_label = "mm day$^{-1}$",
    cbar_loc = "bottom",
)

plot_pval(
    crop(reg_map_clim_PR["pval"], box = [40, 280, -60, 40]),
    ax = axs[0],
    level = 0.05,
    fdr = True,
    pattern = "...."
)

plot_cartopy_contourf(
    crop(reg_map_clim_TAS["slope"], box = [40, 280, -60, 40]),
    ax = axs[1],
    min = -1, max = 1, step = 0.2,
    cmap = "RdYlBu_r",
    grid_labels = {"top": "x", "left": "y"},
    title = "Regression with surface temperature mean state",
    cbar_label = "°C",
    cbar_loc = "bottom",
)

_, qk_clim = plot_wind(
    crop(reg_map_clim_ua850["slope"], box = [40, 280, -60, 40]), crop(reg_map_clim_va850["slope"], box = [40, 280, -60, 40]),
    ax = axs[1],
    C = crop(pval_ua850_clim * pval_va850_clim, box = [40, 280, -60, 40]),
    ref = 1,
    scale = 25,
    regrid_shape = 15,
    width = 0.0025,
    keyx = 0.05,
    keyy = -0.15,
    key_label = " m s$^{-1}$"
)

qk_clim.text.set_fontsize(6)

axs[0].add_geometries([rect_X2], crs = ccrs.PlateCarree(), edgecolor = "red", facecolor = 'none', zorder = 10)
axs[1].add_geometries([rect_X2], crs = ccrs.PlateCarree(), edgecolor = "red", facecolor = 'none', zorder = 10)

weights = np.sqrt(np.cos(np.deg2rad(X.lat)))

PC_a_std = ((EOF["u"].isel(mode = 0).fillna(0) * (X - X.mean(dim = "time")).fillna(0)) * weights).sum(dim = ["lon", "lat"]).std(dim = "time")
PC_b_std = ((EOF["v"].isel(mode = 0).fillna(0) * (Y - Y.mean(dim = "time")).fillna(0)) * weights).sum(dim = ["lon", "lat"]).std(dim = "time")

PC_a_obs_0 = ((EOF["u"].isel(mode = 0).fillna(0) * (X_obs - X.mean(dim = "time")).fillna(0)) * weights).sum(dim = ["lon", "lat"]) / PC_a_std
PC_a_MIROC6_0 = ((EOF["u"].isel(mode = 0).fillna(0) * (X_MIROC6 - X.mean(dim = "time")).fillna(0)) * weights).sum(dim = ["lon", "lat"]) / PC_a_std
PC_b_MIROC6_0 = ((EOF["v"].isel(mode = 0).fillna(0) * (Y_MIROC6 - Y.mean(dim = "time")).fillna(0)) * weights).sum(dim = ["lon", "lat"]) / PC_b_std

PC2_a_std = ((EOF2["u"].isel(mode = 0).fillna(0) * (X2 - X2.mean(dim = "time")).fillna(0)) * weights).sum(dim = ["lon", "lat"]).std(dim = "time")
PC2_b_std = ((EOF2["v"].isel(mode = 0).fillna(0) * (Y2 - Y2.mean(dim = "time")).fillna(0)) * weights).sum(dim = ["lon", "lat"]).std(dim = "time")

PC2_a_obs_0 = ((EOF2["u"].isel(mode = 0).fillna(0) * (X2_obs - X2.mean(dim = "time")).fillna(0)) * weights).sum(dim = ["lon", "lat"]) / PC2_a_std
PC2_a_MIROC6_0 = ((EOF2["u"].isel(mode = 0).fillna(0) * (X2_MIROC6 - X2.mean(dim = "time")).fillna(0)) * weights).sum(dim = ["lon", "lat"]) / PC2_a_std

axs[2].set_axisbelow(True)
axs[2].grid(alpha = 0.5)
axs[2].scatter(PC2_a_MIROC6_0, PC_b_MIROC6_0 * -1, s = 2, c = "red")
axs[2].scatter(PC2["b"].isel(mode = 0)[out], PC["b"].isel(mode = 0)[out] * -1, c = colors["grey"][4], s = 17)
axs[2].scatter(PC2["b"].isel(mode = 0)[CMIP6_True], PC["b"].isel(mode = 0)[CMIP6_True] * -1, s = 2, c = "#0C7BDC")
axs[2].scatter(PC2["b"].isel(mode = 0)[~CMIP6_True], PC["b"].isel(mode = 0)[~CMIP6_True] * -1, s = 2, c = "#FFC20A")
axs[2].scatter(PC2["b"].isel(mode = 0, time = 35), PC["b"].isel(mode = 0, time = 35) * -1, c = "#0C7BDC", edgecolor = "red", lw = 1, s = 15)

axs[2].set_xlabel("PC of precipitation mean state (1st mode)")
axs[2].set_ylabel(r"$\mathbf{v}_1^T \boldsymbol{\mathsf{Y}}$" + " - precipitation change")

axs[3].set_axisbelow(True)
axs[3].grid(alpha = 0.5)
axs[3].scatter(PC2_a_MIROC6_0, PC_a_MIROC6_0 * -1, s = 2, c = "red")
axs[3].scatter(PC2["b"].isel(mode = 0)[out], PC["a"].isel(mode = 0)[out] * -1, c = colors["grey"][4], s = 17)
axs[3].scatter(PC2["b"].isel(mode = 0)[CMIP6_True], PC["a"].isel(mode = 0)[CMIP6_True] * -1, s = 2, c = "#0C7BDC")
axs[3].scatter(PC2["b"].isel(mode = 0)[~CMIP6_True], PC["a"].isel(mode = 0)[~CMIP6_True] * -1, s = 2, c = "#FFC20A")
axs[3].scatter(PC2["b"].isel(mode = 0, time = 35), PC["a"].isel(mode = 0, time = 35) * -1, c = "#0C7BDC", edgecolor = "red", lw = 1, s = 15)

axs[3].set_xlabel("PC of precipitation mean state (1st mode)")
axs[3].set_ylabel(r"$\mathbf{u}_1^T \boldsymbol{\mathsf{X}}$" + " - precipitation trend")

for i in range(2, 4) :
    ymax = np.max(np.abs([axs[i].get_ylim()]))
    xmax = np.max(np.abs([axs[i].get_xlim()]))
    axs[i].set_ylim(-ymax, ymax)
    axs[i].set_xlim(-xmax, xmax)

for i in [2, 3] : 
    axs[i].vlines([PC2_a_obs_0.isel(obs = -1)], ymin = -4, ymax = 4, colors = colors["green"][8], zorder = -50, lw = 0.8)
    axs[i].fill_betweenx(
        y = [-10, 10],
        x1 = PC2_a_obs_0.isel(obs = -1) - PC2_a_obs_0.isel(obs = slice(0, 4)).std(dim = "obs"),
        x2 = PC2_a_obs_0.isel(obs = -1) + PC2_a_obs_0.isel(obs = slice(0, 4)).std(dim = "obs"),
        color = colors["green"][6],
        alpha = 0.3,
        lw = 0,
        zorder = -51
    )

    axs[i].fill_betweenx(
        y = [-10, 10],
        x1 = PC2_a_MIROC6_0.mean(dim = "run") - PC2_a_MIROC6_0.std(dim = "run"),
        x2 = PC2_a_MIROC6_0.mean(dim = "run") + PC2_a_MIROC6_0.std(dim = "run"),
        color = colors["red"][6],
        alpha = 0.2,
        lw = 0,
        zorder = -51
    )

axs[3].hlines([PC_a_obs_0.isel(obs = -1) * -1], xmin = -4, xmax = 4, colors = colors["green"][8], zorder = -50, lw = 0.8)
axs[3].fill_between(
    x = [-10, 10],
    y1 = PC_a_obs_0.isel(obs = -1)*-1 - PC_a_obs_0.isel(obs = slice(0, 4)).std(dim = "obs"),
    y2 = PC_a_obs_0.isel(obs = -1)*-1 + PC_a_obs_0.isel(obs = slice(0, 4)).std(dim = "obs"),
    color = colors["green"][6],
    alpha = 0.3,
    lw = 0,
    zorder = -51
)

axs[3].fill_between(
    x = [-10, 10],
    y1 = PC_a_MIROC6_0.mean(dim = "run")*-1 - PC_a_MIROC6_0.std(dim = "run"),
    y2 = PC_a_MIROC6_0.mean(dim = "run")*-1 + PC_a_MIROC6_0.std(dim = "run"),
    color = colors["red"][6],
    alpha = 0.2,
    lw = 0,
    zorder = -51
)

# Legend
axs[2].scatter([], [], c = "#0C7BDC", s = 2, label = "CMIP6")
axs[2].scatter([], [], c = "#FFC20A", s = 2, label = "CMIP5")
axs[2].scatter([], [], c = "red", s = 2, label = "MIROC6")
axs[2].plot([], [], color = colors["green"][8], lw = 0.8, label = "Obs. mean")
axs[2].hist(
    [],
    color = colors["red"][6],
    alpha = 0.2,
    label = "$\pm$ 1 MIROC6 std"
)
axs[2].hist(
    [],
    color = colors["green"][6],
    alpha = 0.3,
    label = "$\pm$ 1 obs. std"
)

plt.figlegend(ncols = 3, loc = "lower center", bbox_to_anchor = (0.5, -0.1))

axs_flat = axs
for i in range (4) :
    axs_flat[i].annotate(
        labels[i], xy = (0.95, 0.1), xycoords = 'axes fraction',
        va = "center", ha = "center",
        bbox = dict(boxstyle = "round", fc = "w", ec = "k", lw = 0.5),
        fontsize = 7
    )
    
plt.savefig("figures/fig8.pdf")