from init.const import *
from init.lib import *
from init.func import *

from load_data.obs import *
from load_data.GCMs import pr_trend_JJAS, pr_change_JJAS, pr_trend_JJAS_MIROC6, pr_change_JJAS_MIROC6

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

X_MIROC6 = crop(pr_trend_JJAS_MIROC6 , box = box_X)
Y_MIROC6 = crop(pr_change_JJAS_MIROC6 , box = box_Y)

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

weights = np.sqrt(np.cos(np.deg2rad(X.lat)))

fig, axs = plt.subplots(
    nrows = 2, ncols = 1,
    figsize = (COLUMNWIDTH, COLUMNWIDTH * 2)
)

axs[0].set_axisbelow(True)
axs[0].grid(alpha = 0.5)
axs[1].set_axisbelow(True)
axs[1].grid(alpha = 0.5)

for m, m_lab in enumerate(["1st", "2nd"]) :

    PC_a_std = ((EOF["u"].isel(mode = m).fillna(0) * (X - X.mean(dim = "time")).fillna(0)) * weights).sum(dim = ["lon", "lat"]).std(dim = "time")
    PC_b_std = ((EOF["v"].isel(mode = m).fillna(0) * (Y - Y.mean(dim = "time")).fillna(0)) * weights).sum(dim = ["lon", "lat"]).std(dim = "time")

    PC_a_obs = ((EOF["u"].isel(mode = m).fillna(0) * (X_obs - X.mean(dim = "time")).fillna(0)) * weights).sum(dim = ["lon", "lat"]) / PC_a_std
    PC_a_MIROC6 = ((EOF["u"].isel(mode = m).fillna(0) * (X_MIROC6 - X.mean(dim = "time")).fillna(0)) * weights).sum(dim = ["lon", "lat"]) / PC_a_std
    PC_b_MIROC6 = ((EOF["v"].isel(mode = m).fillna(0) * (Y_MIROC6 - Y.mean(dim = "time")).fillna(0)) * weights).sum(dim = ["lon", "lat"]) / PC_b_std
    
    # MIROC6 LE
    axs[m].scatter(PC_a_MIROC6 * -1, PC_b_MIROC6 * -1, c = "red", s = 2, zorder = 2)
    # Outliers
    axs[m].scatter(PC["a"].isel(mode = m)[out] * -1, PC["b"].isel(mode = m)[out] * -1, c = colors["grey"][5], s = 17, zorder = 2)
    # CMIP5
    axs[m].scatter(PC["a"].isel(mode = m)[~CMIP6_True] * -1, PC["b"].isel(mode = m)[~CMIP6_True] * -1, c = "#FFC20A", s = 2, zorder = 2)
    # CMIP6
    axs[m].scatter(PC["a"].isel(mode = m)[CMIP6_True] * -1, PC["b"].isel(mode = m)[CMIP6_True] * -1, c = "#0C7BDC", s = 2, zorder = 2)
    # MIROC6 member used
    axs[m].scatter(PC["a"].isel(mode = m, time = 35) * -1, PC["b"].isel(mode = m, time = 35) * -1, c = "#0C7BDC", edgecolor = "red", lw = 1, s = 15, zorder = 2)
    
    bottom, top = axs[m].get_ylim()
    ymax = np.max(np.abs([bottom, top]))
    
    # Observations average
    axs[m].vlines(PC_a_obs.isel(obs = -1).values * -1, ymin = -ymax, ymax = ymax, color = colors["green"][8], lw = 0.8, zorder = 1)
    
    axs[m].set_ylim(-ymax, ymax)
    left, right = axs[m].get_xlim()
    xmax = np.max(np.abs([left, right]))
    axs[m].set_xlim(-xmax, xmax)
    axs[m].set_xlabel(fr"$\mathbf{{u}}_{m+1}^T \boldsymbol{{\mathsf{{X}}}}$" + fr"$ \ - \ {expvar["X"].isel(mode = m).values:.2f} \%$" + fr"$ \ ({expvar_pca["X"].isel(mode = 0).values:.2f} \%)$")
    axs[m].set_ylabel(fr"$\mathbf{{v}}_{m+1}^T \boldsymbol{{\mathsf{{Y}}}}$" + fr"$ \ - \ {expvar["Y"].isel(mode = m).values:.2f} \%$" + fr"$ \ ({expvar_pca["Y"].isel(mode = 0).values:.2f} \%)$")
    axs[m].set_title(f"{m_lab} mode of the MCA")
    axs[m].annotate(
        fr"$\mathrm{{SCF}}_{m+1}={PC["scf"].isel(mode = m).values:.1f} \%$" + "\n"
        fr"$\rho_{m+1}={np.corrcoef(PC["a"].isel(mode = m), PC["b"].isel(mode = m))[0, 1]:.2f}$",
        xy = (0.05, 0.84), xycoords = "axes fraction",
        bbox = dict(boxstyle = "round", fc = "w", ec = "#C4C5C7",),
        fontsize = 9
    )
    print("About LE spread")
    print(f"mode {m+1}")
    print("var frac a: ", PC_a_MIROC6.var().values)
    print("var frac b: ", PC_b_MIROC6.var().values)

    # Show obs. spread on x-axis
    axs[m].fill_betweenx(
        y = [-ymax, ymax],
        x1 = PC_a_obs.isel(obs = -1) * -1 - PC_a_obs.isel(obs = slice(0, 4)).std(dim = "obs"),
        x2 = PC_a_obs.isel(obs = -1) * -1 + PC_a_obs.isel(obs = slice(0, 4)).std(dim = "obs"),
        color = colors["green"][6],
        alpha = 0.3,
        lw = 0,
        zorder = -1
    )

    # Show MIROC6 spread on x-axis
    axs[m].fill_betweenx(
        y = [-ymax, ymax],
        x1 = PC_a_MIROC6.mean(dim = "run") * -1 - PC_a_MIROC6.std(dim = "run"),
        x2 = PC_a_MIROC6.mean(dim = "run") * -1 + PC_a_MIROC6.std(dim = "run"),
        color = colors["red"][6],
        alpha = 0.2,
        lw = 0,
        zorder = -1
    )

    # Show MIROC6 spread on y-axis
    axs[m].fill_between(
        x = [-xmax, xmax],
        y1 = PC_b_MIROC6.mean(dim = "run") * -1 - PC_b_MIROC6.std(dim = "run"),
        y2 = PC_b_MIROC6.mean(dim = "run") * -1 + PC_b_MIROC6.std(dim = "run"),
        color = colors["red"][6],
        alpha = 0.2,
        lw = 0,
        zorder = -1
    )

plt.subplots_adjust(hspace = 0.4)

# Legend
axs[0].scatter([], [], c = "#FFC20A", s = 2, label = "CMIP5")
axs[0].scatter([], [], c = "#0C7BDC", s = 2, label = "CMIP6")
axs[0].scatter([], [], c = "red", s = 2, label = "MIROC6")
axs[0].plot([], [], color = colors["green"][8], lw = 0.8, label = "Obs. mean")
axs[0].hist(
    [],
    color = colors["red"][6],
    alpha = 0.2,
    label = "$\pm$ 1 MIROC6 std"
)
axs[0].hist(
    [],
    color = colors["green"][6],
    alpha = 0.3,
    label = "$\pm$ 1 obs. std"
)

plt.figlegend(ncols = 3, loc = "lower center", bbox_to_anchor = (0.5, -0.04))

axs_flat = axs.flatten()
for i in range (len(axs_flat)) :
    axs_flat[i].annotate(
        labels[i], xy = (0.96, 0.05), xycoords = 'axes fraction',
        va = "center", ha = "center",
        bbox = dict(boxstyle = "round", fc = "w", ec = "k", lw = 0.5),
        fontsize = 7
    )

plt.savefig("figures/fig7.pdf")
