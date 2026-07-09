from init.const import *
from init.lib import *
from init.func import *

from load_data.obs import *
from load_data.GCMs import pr_trend_JJAS, pr_change_JJAS, pr_trend_JJAS_MIROC6, pr_change_JJAS_MIROC6
from load_data.GCMs import pr_trend_JJAS_SA, pr_change_JJAS_SA, pr_trend_JJAS_MIROC6_SA, pr_change_JJAS_MIROC6_SA
from load_data.GCMs import land_mask
from load_data.GCMs import pr_TS_India_6, pr_TS_India_5


# LEFT FIELD X
box_X, mask_X, mval_X, left_lab = box_India_2, None, None, "IND2" # left: over India

# RIGHT FIELD Y
box_Y, mask_Y, mval_Y, right_lab = box_India_2, None, None, "IND2" # right: over India (smaller region than box_India)

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

M = 5

X, Y, PC, EOF, _, _, _, _, _, _ = comp_HM_HT(
    pr_trend_JJAS, pr_change_JJAS,
    box_X = box_X, mask_X = mask_X, mval_X = mval_X,
    box_Y = box_Y, mask_Y = mask_Y, mval_Y = mval_Y,
    MCA_only = True,
    M = M
)

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

Y_c_obs = xr.concat(Y_c_obs_list, dim="nb_of_mode")
Y_c_obs = Y_c_obs.assign_coords(nb_of_mode=range(1, M+1))
Y_c_obs = pr_change_JJAS_SA + Y_c_obs

Y_IND = crop(pr_change_JJAS, box = box_India_2)
Y_IND_land = mask(Y_IND, crop(land_mask, box = box_India_2), 1)

Y_c_obs_IND = crop(Y_c_obs, box = box_India_2)
Y_c_obs_IND_land = mask(Y_c_obs_IND, crop(land_mask, box = box_India_2), 1)

# Mean change
## mm/day
y_mm_day_ind = spatial_mean(Y_IND, as_float = False).values # all
y_mm_day_ind_land = spatial_mean(Y_IND_land, as_float = False).values # land
y_mm_day = [y_mm_day_ind, y_mm_day_ind_land]

m_best = 2

# colors_box2 = ["#4E4E4E","firebrick", "royalblue"]
# obs_color = ["#e41a1c", "#4daf4a", "#984ea3", "#9E7646", "k"]
# obs_color = ["darkorange", "#4daf4a", "#984ea3", "#9E7646", "k"]
# obs_color = [colors["d.orange"][4], colors["green"][4], colors["purple"][4], colors["brown"][4], colors["blue grey"][8]]
# obs_color = [colors["green"][i] for i in range(4, 9)]
# domain_color = ["red", "royalblue"]
domain_color = ["red", "blue"]
# xticks_lab = [f"Constrained by\n{X_obs.dataset[0]}"] + [X_obs.dataset[i] for i in range(1, 5)]
xticks_lab = [X_obs.dataset[i] for i in range(0, 4)] + ["Obs. mean"]

obs_color = [colors["green"][4]]*4 + [colors["green"][8]]
obs_facecolor = [colors["green"][2]]*4 + [colors["green"][6]]
obs_marker = ["v", "s", "d", "o"]
obs_ls = [marker + "-" for marker in obs_marker]
shift = [0.1, -0.1, 0.2, -0.05, 0]

colors_box = ["k", "#F30033", "#62B902"]
eps = 0.1

_, axs = plt.subplots(
    nrows = 1, ncols = 2,
    figsize = (TEXTWIDTH, TEXTWIDTH / (1.2 * GOLDEN_RATIO))
)

# axs[0].set_title("Constraint of future precipitation change\nusing the 2 first modes of the MCA")

y_temp = np.linspace(-2, 4, 1000)

for i, var in enumerate([Y_IND, Y_IND_land]) :

    y = y_mm_day[i]
    mean_values = y
    
    axs[0].hlines(
        y.mean(),
        xmin = -0.1 + 1 * i, xmax = 0.7 + 1 * i,
        # colors = colors[domain_color[i]][2],
        colors = colors["grey"][6],
        # colors = colors[domain_color[i]][6],
        lw = 0.5
    )
    
    axs[0].boxplot(
        mean_values,
        # showmeans = True,
        positions = [i], patch_artist = True,
        boxprops = {"color": colors["grey"][7], "facecolor": colors["grey"][5], "alpha": 1}, whiskerprops = {"color": colors["grey"][7]}, capprops = {"color": colors["grey"][7]}, medianprops = {"color": colors["grey"][7]}, flierprops = {"markeredgecolor": colors["grey"][7], "markersize": 1},
        widths = 0.05,
        zorder = 50,
        tick_labels = ["Raw"]
    )
    # axs[0].plot(i - norm_y_np, y_temp, color = "k", lw = 1)
    # axs[0].fill_betweenx(
    #     y = y_temp, x1 = i - norm_y_np, x2 = [i] * len(norm_y_np),
    #     color = "k", alpha = 0.2
    # )

# for i, var in enumerate([Y_c_E5.isel(nb_of_mode = j) for j in range(5)]) :
for i, var in enumerate([Y_c_obs_IND, Y_c_obs_IND_land]) :
    for j in range(5) :
        mean_values = spatial_mean(var.sel(obs = j, nb_of_mode = m_best), as_float = False).values
        # norm_y_np = norm.pdf(y_temp, loc = np.mean(mean_values), scale = np.std(mean_values))
        # norm_y_np /= 2.2 * norm_y_np.max()
        axs[0].boxplot(
            mean_values,
            positions = [i + (j+2) * eps], patch_artist = True,
            boxprops = {"color": obs_color[j], "facecolor": obs_facecolor[j], "alpha": 1}, whiskerprops = {"color": obs_color[j]}, capprops = {"color": obs_color[j]}, medianprops = {"color": obs_color[j]}, flierprops = {"markeredgecolor": obs_color[j], "markersize": 1},
            # boxprops = {"color": colors["green"][j + 4], "facecolor": colors["green"][j + 1], "alpha": 1}, whiskerprops = {"color": colors["green"][j + 4]}, capprops = {"color": colors["green"][j + 4]}, medianprops = {"color": colors["green"][j + 4]}, flierprops = {"markeredgecolor": colors["green"][j + 4], "markersize": 1},
            widths = 0.05,
            tick_labels = [xticks_lab[j]]
        )
        # axs[0].plot(i + eps - norm_y_np, y_temp, color = colors_box[1], lw = 1)
        # axs[0].plot(i - norm_y_np, y_temp, color = colors_box[1], lw = 1)
        # axs[0].fill_betweenx(
        #     y = y_temp, x1 = i + eps - norm_y_np, x2 = [i + eps] * len(norm_y_np),
        #     color = colors_box[1], alpha = 0.2
        # )

axs[0].fill_betweenx(y = [-10, 10], x1 = -0.10, x2 = 0.70, color = colors[domain_color[0]][3], alpha = 0.1, zorder = -5, lw = 0)
axs[0].fill_betweenx(y = [-10, 10], x1 = 0.90, x2 = 1.70, color = colors[domain_color[1]][3], alpha = 0.1, zorder = -1, lw = 0)
axs[0].tick_params(axis = "x", labelrotation = 90)
# axs[0].set_xticks(
#     ticks = np.arange(0, 1.8, 0.1),
#     labels = ["Raw", "", "Constrained by"] + [X_obs.dataset[m] for m in range(5)] + [""]*2 + ["Raw", "", "Constrained by"] + [X_obs.dataset[m] for m in range(5)]
# )
# for i in [1, 2, 8, 9, 11, 12,]:
#     axs[0].xaxis.get_major_ticks()[i].tick1line.set_visible(False)
#     axs[0].xaxis.get_major_ticks()[i].tick2line.set_visible(False)

axs[0].set_ylabel("Mean precipitation change (mm day$^{-1}$)")
# axs[0].set_xlim(-0.7, 2.5)
axs[0].set_xlim(-0.40, 2)
# axs[0].set_xlim(-0.40, 3.5)
axs[0].set_ylim(-1, 3.5)
# axs[0].set_ylim(-1, 5.5)
axs[0].grid(axis = "both", alpha = 0.2, zorder = -50)

axs[0].hlines(y = 0, xmin = -5, xmax = 5, colors = "grey", alpha = 0.75, lw = 1, zorder = -1)

text = axs[0].text(
    x = 0.3, y = 3.2, s = "EISM",
    va = "center", ha = "center",
    color = "k"
)
# text.set_path_effects([Stroke(linewidth=1.5, foreground="white"), Normal()])
text = axs[0].text(
    x = 1.3, y = 3.2, s = "ISM",
    va = "center", ha = "center",
    color = "k"
)
# text.set_path_effects([Stroke(linewidth=1.5, foreground="white"), Normal()])


#########################################################

xmin, xmax = -0.5, 0.5
axs[1].grid(axis = "both", alpha = 0.3)
axs[1].hlines([0.5], xmin = xmin, xmax = xmax, colors = [colors["grey"][4]], lw = 0.8, alpha = 1)
axs[1].vlines([0], ymin = 0, ymax = 2, colors = [colors["grey"][4]], lw = 0.8, alpha = 1)

i = 0
for y_c, y in zip([Y_c_obs_IND, Y_c_obs_IND_land], [Y_IND, Y_IND_land]) :
    mean_values_y = spatial_mean(y, as_float = False).values
    for j in range(5) :
        mean_values_y_c = spatial_mean(y_c.sel(obs = j, nb_of_mode = m_best), as_float = False).values
        # axs[1].scatter((np.mean(mean_values_y_c) / np.mean(mean_values_y)) - 1, np.var(mean_values_y_c) / np.var(mean_values_y), color = colors_box[i])
        axs[1].scatter((np.mean(mean_values_y_c) - np.mean(mean_values_y)), np.var(mean_values_y_c) / np.var(mean_values_y), marker = (obs_marker + ["P"])[j], color = obs_color[j], s = 15, edgecolor = colors[domain_color[i]][7], lw = 0.5, zorder = 10)
        # axs[1].scatter(np.mean(mean_values_y_c), np.var(mean_values_y_c) / np.var(mean_values_y), marker = (obs_marker + ["P"])[j], color = obs_color[j], s = 15, edgecolor = colors[domain_color[i]][7], lw = 0.5, zorder = 10)
    axs[1].hlines(y = np.var(mean_values_y_c) / np.var(mean_values_y), xmin = xmin, xmax = xmax, color = colors[domain_color[i]][7], lw = 1)
    # axs[1].vlines(x = np.mean(mean_values_y), ymin = 0, ymax = 1, color = colors[domain_color[i]][7], lw = 1)
    # axs[1].vlines(
    #     np.mean(mean_values_y),
    #     ymin = 0,
    #     ymax = 1,
    #     # colors = colors[domain_color[i]][2],
    #     # colors = colors["grey"][6],
    #     colors = colors[domain_color[i]][6],
    #     lw = 0.5
    # )
    i+=1

# i = 0
# for y_c, y in zip([Y_c_GPCP_IND, Y_c_GPCP_IND_land], [Y_IND, Y_IND_land]) :
#     mean_values_y = spatial_mean(y, as_float = False).values
#     mean_values_y_c = spatial_mean(y_c.sel(nb_of_mode = m_best), as_float = False).values
#     # axs[1].scatter((np.mean(mean_values_y_c) / np.mean(mean_values_y)) - 1, np.var(mean_values_y_c) / np.var(mean_values_y), color = colors_box[i])
#     axs[1].scatter((np.mean(mean_values_y_c) - np.mean(mean_values_y)), np.var(mean_values_y_c) / np.var(mean_values_y), color = colors_box2[i], edgecolors = colors_box[2], s = 20, zorder = 10)
#     print("Reduction in uncertainty:", 1 - np.var(mean_values_y_c) / np.var(mean_values_y))
#     i+=1

# # left, right = axs[1].get_xlim()

ds_pr_TS_India_Y_C6 = pr_TS_India_6.resample(time = "1YE").mean()
ds_pr_TS_India_JJAS_C6 = pr_TS_India_6.sel(time = pr_TS_India_6['time.month'].isin([6, 7, 8, 9]))
ds_pr_TS_India_mJJAS_C6 = ds_pr_TS_India_JJAS_C6.resample(time = "1YE").mean()

ds_pr_TS_India_Y_C5 = pr_TS_India_5.resample(time = "1YE").mean()
ds_pr_TS_India_JJAS_C5 = pr_TS_India_5.sel(time = pr_TS_India_5['time.month'].isin([6, 7, 8, 9]))
ds_pr_TS_India_mJJAS_C5 = ds_pr_TS_India_JJAS_C5.resample(time = "1YE").mean()

pr_trend_1979_2024_C6 = temporal_regression(ds_pr_TS_India_mJJAS_C6.sel(time = slice("1979", "2024")).groupby("time.year").mean(dim = "time"))
pr_trend_1979_2024_C5 = temporal_regression(ds_pr_TS_India_mJJAS_C5.sel(time = slice("1979", "2024")).groupby("time.year").mean(dim = "time"))
pr_trend_1979_2024 = xr.concat([pr_trend_1979_2024_C5, pr_trend_1979_2024_C6], dim = "model")["slope"] * 46

for i, y in enumerate(y_mm_day) :
    slope, intercept, pvalue, r2 = linregress_1d(
        y,
        pr_trend_1979_2024.values
    )
    
    axs[1].hlines(y = 1 - r2, xmin = xmin, xmax = xmax, color = colors[domain_color[i]][7], lw = 1, ls = "--")

# x = spatial_mean(X_IND, as_float = False).values # trends 1979-2024
# for i, y in enumerate(y_mm_day) :
#     slope, intercept, pvalue, r2 = linregress_1d(y, x)
    
#     if pvalue < 0.05 :
#         axs[1].hlines(y = 1 - r2, xmin = -1, xmax = 1, color = colors_box2[i], lw = 1, ls = "--")

ax_right = axs[1].twinx()
ax_right.plot([], [], color='r')
ax_right.set_ylim(100, 0)
ax_right.set_ylabel("Reduction in variance - \%")
ax_right.minorticks_on()

for i in range(4) :
    axs[1].scatter([], [], marker = (obs_marker + ["P"])[i], s = 15, color = obs_color[i], label = X_obs.dataset[i], lw  = 0)
axs[1].scatter([], [], marker = "P", s = 15, color = obs_color[-1], label = "Obs. mean", lw  = 0)
axs[1].hist([], color = colors[domain_color[0]][7], label = "EISM domain")
axs[1].hist([], color = colors[domain_color[1]][7], label = "ISM domain")
axs[1].plot([], [], color = "k", alpha = 0.6, ls = "-", label = "EC MCA")
axs[1].plot([], [], color = "k", alpha = 0.6, ls = "--", label = "Traditional EC")
# axs[1].legend(loc = "upper center", bbox_to_anchor = (0.5, -0.17), ncols = 2)
axs[1].legend(ncols = 2, loc = "lower center", fontsize = 8)

# axs[1].set_yticks([0.0, 0.2, 0.4, 0.5, 0.6, 0.8, 1.0], [0.0, 0.2, 0.4, 0.5, 0.6, 0.8, 1.0])
# axs[1].set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
# axs[1].set_yticks(np.arange(0, 1.1, 0.1), np.arange(0, 1.1, 0.1))
# # axs[1].set_xlim(left, right)
axs[1].set_xlim(xmin, xmax)
# axs[1].set_xlabel("Mean precipitation change\nrelative to raw distrubtion (mm day$^{-1}$)")
axs[1].set_xlabel("Change in mean value\nrelative to raw mean change (mm day$^{-1}$)")
# axs[1].set_ylim(0.3, 1)
axs[1].set_ylim(0, 1)
axs[1].set_ylabel("Remaining variance ratio")
# # axs[1].set_ylabel("Remaining variance\n" + fr"$\frac{{var(Y|X_o^{{({m_best})}})}}{{var(Y)}}$")
# # axs[1].set_ylabel("Remaining variance\n" + fr"$var(Y|X_o^{{({m_best})}})/var(Y)$")

axs[1].minorticks_on()
# axs[1].tick_params(axis = "y", which = "minor")

# plt.subplots_adjust(wspace = 0.4)
plt.subplots_adjust(wspace = 0.25)

axs_flat = axs.flatten()
for i in range (len(axs_flat)) :
    axs_flat[i].annotate(
        labels[i], xy = (0.05, 0.95), xycoords = 'axes fraction',
        va = "center", ha = "center",
        bbox = dict(boxstyle = "round", fc = "w", ec = "k", lw = 0.5),
        fontsize = 7
    )

plt.savefig("figures/fig12.pdf")
plt.close()
# plt.show()