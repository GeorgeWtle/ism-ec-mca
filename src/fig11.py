from init.const import *
from init.lib import *
from init.func import *

from load_data.obs import *
from load_data.GCMs import pr_change_JJAS, pr_trend_JJAS, pr_change_JJAS_SA, pr_trend_JJAS_SA

# plt.rcParams["savefig.bbox"] = None

M = 5

# MCA between pr_trend_JJAS and pr_change_JJAS
# LEFT FIELD X: pr_trend_JJAS
box_X, mask_X, mval_X, left_lab = box_India_2, None, None, "IND2" # left: over EISM
# RIGHT FIELD Y: pr_change_JJAS
box_Y, mask_Y, mval_Y, right_lab = box_India_2, None, None, "IND2" # right: over EISM

X, Y, PC, EOF, _, _, _, _, _, _ = comp_HM_HT(
    pr_trend_JJAS, pr_change_JJAS,
    box_X = box_X, mask_X = mask_X, mval_X = mval_X,
    box_Y = box_Y, mask_Y = mask_Y, mval_Y = mval_Y,
    MCA_only = True,
    M = M
)

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

EC_label = [f"a{i}" for i in range (M)]
EC_df = pd.DataFrame(
    [PC["a"].isel(mode = i).values for i in range (M)],
    index = EC_label
).T # contains M ECs as columns

gamma_ds = qr_multiple_reg(pr_change_JJAS_SA, EC_df) # get all heterogeneous maps

mca = xMCA(X, Y)
mca.apply_coslat()
mca.solve()

eofs = mca.eofs(n = M)
u, v = eofs["left"], eofs["right"]
pcs = mca.pcs(n = M, scaling = "eigen")
a, b = pcs["left"], pcs["right"]

weights = np.sqrt(np.cos(np.deg2rad(X.lat)))

Y_c_E5_list = []
Y_c_GPCP_list = []
Y_c_obs_list = []

for m in range (M):
    gamma_da = gamma_ds.isel(nb_of_mode = m)["slope"]
    # Y_c_m_E5 = xr.zeros_like(pr_change_JJAS_SA)
    # Y_c_m_GPCP = xr.zeros_like(pr_change_JJAS_SA)
    Y_c_m_obs = xr.zeros_like(pr_change_JJAS_SA)
    # Y_c_m_obs = xr.zeros_like(pr_change_JJAS_SA).expand_dims(
    #     obs=X_obs.obs
    # )
    for i in range(m+1):
        # a_i = u.isel(mode = i).fillna(0) @ (X_E5 - X).fillna(0)
        # a_i_E5 = ((u.isel(mode = i).fillna(0) * (X_E5 - X).fillna(0)) * weights).sum(dim = ["lon", "lat"])
        # a_i_GPCP = ((u.isel(mode = i).fillna(0) * (X_GPCP - X).fillna(0)) * weights).sum(dim = ["lon", "lat"])
        a_i_obs = ((u.isel(mode = i, drop = True).fillna(0) * (X_obs - X).fillna(0)) * weights).sum(dim = ["lon", "lat"])
        
        gamma_i = gamma_da.sel(coef = f"a{i}", drop = True)
        # Y_c_m_E5 += gamma_i * (a_i_E5 / a.isel(mode = i).std(dim = "time"))
        # Y_c_m_GPCP += gamma_i * (a_i_GPCP / a.isel(mode = i).std(dim = "time"))
        # Y_c_m_obs += gamma_i * (a_i_obs / a.isel(mode = i).std(dim = "time"))
        Y_c_m_obs = Y_c_m_obs + gamma_i * (a_i_obs / a.isel(mode = i, drop = True).std(dim = "time"))
    # Y_c_E5_list.append(Y_c_m_E5.copy(deep=True))
    # Y_c_GPCP_list.append(Y_c_m_GPCP.copy(deep=True))
    Y_c_obs_list.append(Y_c_m_obs.copy(deep=True))

# Y_c_E5 = xr.concat(Y_c_E5_list, dim="nb_of_mode")
# Y_c_E5 = Y_c_E5.assign_coords(nb_of_mode=range(1, M+1))
# Y_c_E5 = Y_SA + Y_c_E5

# Y_c_GPCP = xr.concat(Y_c_GPCP_list, dim="nb_of_mode")
# Y_c_GPCP = Y_c_GPCP.assign_coords(nb_of_mode=range(1, M+1))
# Y_c_GPCP = Y_SA + Y_c_GPCP

Y_c_obs = xr.concat(Y_c_obs_list, dim = "nb_of_mode")
Y_c_obs = Y_c_obs.assign_coords(nb_of_mode = range(1, M+1))
Y_c_obs = pr_change_JJAS_SA + Y_c_obs

m_best = 2

_, pval_Y_vs_Y_c_obs = ttest_ind(
    pr_change_JJAS_SA.expand_dims(obs = Y_c_obs.obs).transpose("obs", "time", "lat", "lon"),
    Y_c_obs.sel(nb_of_mode = m_best).transpose("obs", "time", "lat", "lon"),
    axis = 1, equal_var = False
)
xarray_pval_Y_vs_Y_c_obs = xr.DataArray(
    data = pval_Y_vs_Y_c_obs,
    coords = {
        'obs': Y_c_obs.obs,
        'lat': pr_change_JJAS_SA.lat,
        'lon': pr_change_JJAS_SA.lon
    },
    dims =("obs", "lat", "lon")
)

# print(xarray_pval_Y_vs_Y_c_obs.isel(obs = -1))

rect_India = rect(box_India_2)

fig, axs = plt.subplots(
    subplot_kw = {'projection': ccrs.PlateCarree()},
    nrows = 4, ncols = 1,
    figsize = (COLUMNWIDTH, TEXTHEIGHT * 0.85),
)

map0 = plot_cartopy_contourf(
    pr_change_JJAS_SA.mean(dim = "time"),
    ax = axs[0],
    min = -3, max = 3, num = 13,
    cmap = "BrBG",
    grid_labels = {"left": "y"},
    cbar_label = "mm day$^{-1}$ ",
    title = "Inter model mean"
)
cbar0 = map0.colorbar
# axs[0].annotate("Inter model mean", xy = (-0.3, 0.5), xycoords = 'axes fraction', rotation = "vertical", va = "center")

map1 = plot_cartopy_contourf(
    Y_c_obs.sel(nb_of_mode = m_best).isel(obs = -1).mean(dim = "time"),
    # Y_c_obs.sel(nb_of_mode = m_best).isel(obs = slice(0, 5)).mean(dim = ["obs", "time"]),
    # Y_c_obs.sel(obs = 4, nb_of_mode = m_best).mean(dim = "time"),
    ax = axs[1],
    min = -3, max = 3, num = 13,
    cmap = "BrBG",
    grid_labels = {"left": "y"},
    cbar_label = "mm day$^{-1}$ ",
    title = "Averaged constrained mean"
)
cbar1 = map1.colorbar
# axs[1].annotate("Average constrained mean", xy = (-0.3, 0.5), xycoords = 'axes fraction', rotation = "vertical", va = "center", ha = "center")
plot_pval(
    xarray_pval_Y_vs_Y_c_obs.isel(obs = -1),
    ax = axs[1],
    fdr = True,
    level = 0.1,
   pattern = "....."
)

map2 = plot_cartopy_contourf(
    Y_c_obs.sel(nb_of_mode = m_best).isel(obs = -1).mean(dim = "time") - pr_change_JJAS_SA.mean(dim = "time"),
    # Y_c_obs.sel(nb_of_mode = m_best).isel(obs = slice(0, 5)).mean(dim = ["obs", "time"]) - pr_change_JJAS_SA.mean(dim = "time"),
    # Y_c_obs.sel(obs = 4, nb_of_mode = m_best).mean(dim = "time") - pr_change_JJAS_SA.mean(dim = "time"),
    ax = axs[2],
    min = -1, max = 1, num = 13,
    cmap = "BrBG",
    grid_labels = {"left": "y"},
    cbar_label = "mm day$^{-1}$ ",
    title = "Average of the correction term",
    tickstep = 6
)
cbar2 = map2.colorbar
# axs[2].annotate("Average of the correction term", xy = (-0.3, 0.5), xycoords = 'axes fraction', rotation = "vertical", va = "center", ha = "center")

map3 = plot_cartopy_contourf(
    Y_c_obs.sel(nb_of_mode = m_best).isel(obs = slice(0,5)).mean(dim = "time").var(dim = "obs"),
    ax = axs[3],
    min = 0.05, max = 0.5, num = 10,
    cmap = "GnBu",
    grid_labels = {"bottom": "x", "left": "y"},
    cbar_label = "(mm day$^{-1}$)$^2$",
    title = "Variance of the correction term",
    undercolor = "white",
    tickstep = 3
)
cbar3 = map3.colorbar
# axs[3].annotate("Variance of the correction term", xy = (-0.3, 0.5), xycoords = 'axes fraction', rotation = "vertical", va = "center", ha = "center")

# cbar0.set_ticks([-3, -2, -1, 0, 1, 2, 3])
# cbar0.set_ticklabels([-3, -2, -1, 0, 1, 2, 3])

# plt.subplots_adjust(hspace = 0.2)

axs[0].add_geometries([rect_India], crs = ccrs.PlateCarree(), edgecolor = "red", facecolor = 'none', zorder = 10)
axs[1].add_geometries([rect_India], crs = ccrs.PlateCarree(), edgecolor = "red", facecolor = 'none', zorder = 10)
axs[2].add_geometries([rect_India], crs = ccrs.PlateCarree(), edgecolor = "red", facecolor = 'none', zorder = 10)
axs[3].add_geometries([rect_India], crs = ccrs.PlateCarree(), edgecolor = "red", facecolor = 'none', zorder = 10)

axs_flat = axs.flatten()
for i in range (len(axs_flat)) :
    axs_flat[i].annotate(
        labels[i], xy = (0.07, 0.9), xycoords = 'axes fraction',
        va = "center", ha = "center",
        bbox = dict(boxstyle = "round", fc = "w", ec = "k", lw = 0.5),
        fontsize = 7
    )

# plt.tight_layout()

plt.savefig("figures/fig11.pdf")

# plt.show()