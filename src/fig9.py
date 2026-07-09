from init.const import *
from init.lib import *
from init.func import *

from process.LOOCV import M, mask_Y, box_Y, mval_Y, Y_hat, MSE
from load_data.GCMs import pr_trend_JJAS_SA, pr_change_JJAS_SA

fig, axs = plt.subplots(
    subplot_kw = {'projection': ccrs.PlateCarree()},
    nrows = M, ncols = 3,
    figsize = (TEXTWIDTH, TEXTHEIGHT)
)

if mask_Y is None :
    rect_Y = rect(box_Y)
else :
    rect_Y = rect(box_Y, mask = mask_Y, mval = mval_Y)

for m in range (M) :

    plot_cartopy_contourf(
        ((pr_change_JJAS_SA - Y_hat.isel(nb_of_mode = m)).var(dim = "time") / pr_change_JJAS_SA.var(dim = "time")) * 100,
        ax = axs[m, 0],
        min = 10, max = 100, step = 10,
        cmap = "RdYlBu",
        grid_labels = {"bottom": "x", "left": "y"},
        cbar_label = "\%",
        tickstep = 1
    )

    plot_cartopy_contourf(
        (MSE.isel(nb_of_mode = m) / pr_change_JJAS_SA.var(dim = "time")) * 100,
        ax = axs[m, 1],
        min = 10, max = 100, step = 10,
        cmap = "RdYlBu",
        grid_labels = {"bottom": "x"},
        cbar_label = "\%",
        tickstep = 1
    )

    plot_cartopy_contourf(
        (MSE.isel(nb_of_mode = m) / ((pr_change_JJAS_SA - Y_hat.isel(nb_of_mode = m)).var(dim = "time"))),
        ax = axs[m, 2],
        min = 1.05, max = 1.5, step = 0.05,
        cmap = "Reds",
        grid_labels = {"bottom": "x"},
        tickstep = 1,
        undercolor = "white"
    )
    
    axs[m, 0].annotate(f"$m={m+1}$", xy = (-0.3, 0.5), xycoords = 'axes fraction', rotation = "vertical", va = "center")

    for i in range (3):
        axs[m, i].add_geometries([rect_Y], crs = ccrs.PlateCarree(), edgecolor = "red", facecolor = 'none', zorder = 10)
    

axs[0, 0].set_title(r"$Var(\boldsymbol{\mathsf{E}}^{(m)}) \big / Var(\boldsymbol{\mathsf{Y}})$")
axs[0, 1].set_title(r"$\boldsymbol{\mathrm{MSE}}^{(m)} \big / Var(\boldsymbol{\mathsf{Y}})$")
axs[0, 2].set_title(r"$\boldsymbol{\mathrm{MSE}}^{(m)} \big/ Var(\boldsymbol{\mathsf{E}}^{(m)})$")

axs_flat = axs.flatten()
for i in range (len(axs_flat)) :
    axs_flat[i].annotate(
        labels[i], xy = (0.075, 0.90), xycoords = 'axes fraction',
        va = "center", ha = "center",
        bbox = dict(boxstyle = "round", fc = "w", ec = "k", lw = 0.5),
        fontsize = 7
    )
    
plt.savefig("figures/fig9.pdf")