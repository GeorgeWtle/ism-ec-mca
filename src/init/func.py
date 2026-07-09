from init.lib import *
from init.const import *

## Functions

def setup_figure(fig = None, where = "ext"):

    if fig is None:
        fig = plt.gcf()

    if where == "ext":  
        manager = plt.get_current_fig_manager()
        manager.window.wm_geometry("1920x1080+100+100")

_original_subplots = plt.subplots

def subplots(*args, **kwargs):
    fig, ax = _original_subplots(*args, **kwargs)
    setup_figure(fig)
    return fig, ax

plt.subplots = subplots

_original_savefig = plt.savefig
def savefig(path, show = True):
    _original_savefig(path)
    if show:
        subprocess.Popen(["evince", path])
    
plt.savefig = savefig
    
## Plot
def plot_cartopy_contourf(data, ax, min, max, step = None, num = None, tickstep = 2, cmap = "BrBG", title = None, cbar_label = None, cbar_loc = "right", cbar_ticks = None, grid = True, grid_labels = True, colorbar = True, undercolor = None, regional = False, box = None, lw_grid = 0.5, lw_coastlines = 0.5):
    """Plot xarray data using cartopy.

    Args:
        data (xarray): 2D xarray, dims: lon, lat.
        ax (ax): Previously created ax used for ploting.
        min (float): Min value for colormap.
        max (float): Max value for colormap.
        step (float): step for discrete colormap.
        cmap (str, optional): Colormap for plot. Defaults to "BrBG".
        title (str, optional): Title. Defaults to None.
        cbar_label (str, optional): Label of the colormap. Defaults to None.
        cbar_loc (str, optional): Position of the colorbar. Defaults to "right".
        cbar_ticks (array, optional): Colorbar range. Defaults to None.
        grid (bool, optional): Show the lat,lon grid. Defaults to True.
        grid_labels (bool, optional): Show the lat,lon values. Defaults to True.
        colorbar (bool, optional): Show the colorbar. Defaults to True.
        regional (bool, optional): Use meshgrid rather than countourf for plot. Defaults to False.
        box (array, optional): Zooming box for plot. Defaults to None.

    Returns:
        _type_: The created map.
    """
    col_map = plt.get_cmap(cmap)
    if undercolor is not None :
        col_map.set_under(undercolor)
    ax.coastlines(lw = lw_coastlines)
    if box is not None:
        ax.set_extent(box, crs = ccrs.PlateCarree())
    if grid:
        gl = ax.gridlines(draw_labels = grid_labels, lw = lw_grid)
        gl.xlabel_style = {'size': 5}
        gl.ylabel_style = {'size': 5}
    if num is None :
        cbar_level = np.arange(min, max + step, step)
    elif step is None :
        cbar_level = np.linspace(min, max, num)
    else:
        raise ValueError("Provide either step or num")
    if cbar_ticks is None:
        cbar_ticks = cbar_level[::tickstep]
    if regional == False:
        if colorbar:
            map = data.plot.contourf(
                ax = ax,
                levels = cbar_level,
                transform = ccrs.PlateCarree(),
                cbar_kwargs = {"label": cbar_label, "ticks": cbar_ticks, "location": cbar_loc},
                extend = "both", # show values higher than (vmax, vmin),
                cmap = col_map
            )
        else:
            map = data.plot.contourf(
                ax = ax,
                levels = cbar_level,
                transform = ccrs.PlateCarree(),
                extend = "both", # show values higher than (vmax, vmin),
                cmap = col_map,
                add_colorbar = colorbar
            )
    if regional == True:
        map = data.plot(
            ax = ax,
            norm = mpl.colors.BoundaryNorm(cbar_level, ncolors=col_map.N, extend = "both"),
            transform = ccrs.PlateCarree(),
            cbar_kwargs = {"label": cbar_label, "ticks": cbar_ticks, "location": cbar_loc},
            extend = "both", # show values higher than (vmax, vmin),
            cmap = col_map
        )
  
    ax.set_title(title)
    
    return map

def plot_pval(xarray, ax, fdr = False, lower = True, level = 0.01, zorder = 1000, pattern = "..."):

    lon = xarray.lon
    lat = xarray.lat
    if fdr:
        values = np.nan_to_num(xarray.values, nan = 1)
        data = false_discovery_control(values)
    else:
        data = xarray.values

    # data, lon = add_cyclic_point(data, coord = lon)

    if lower:
        levels = [0, level] # stipplings where pval < level
        hatches = [pattern, ""]
    else :
        levels = [level, 1] # stipplings where pval > level
        # hatches = ["", pattern]
        hatches = [pattern, ""]
    ax.contourf(
        lon,
        lat,
        data,
        transform = ccrs.PlateCarree(),
        levels = levels,
        hatches = hatches,
        alpha = 0,
        zorder = zorder
    )

def plot_wind (xarray_U, xarray_V, ax, width = 0.005, scale = 60, regrid_shape = 30, keyx = 0.5, keyy = -0.03, ref = 10, key_label = "m s$^{-1}$", C = None):

    if C is not None :
        bins = [0, 0.05, 0.1, 0.15, 0.2, 0.25]
        # cmap = plt.get_cmap("Greys_r", len(bins) - 1)  # discrete colormap
        cmap = mcolors.ListedColormap(["#252525FF", "#252525BF", "#25252580", "#25252581", "#2525251A"])  # discrete colormap
        norm = mcolors.BoundaryNorm(bins, cmap.N)
        
        Q = ax.quiver(
            xarray_U.lon, xarray_U.lat,
            xarray_U,
            xarray_V,
            C,
            transform = ccrs.PlateCarree(),
            scale = scale,
            regrid_shape = regrid_shape,
            cmap = cmap,
            norm = norm,
            width = width
        )
    else :
        Q = ax.quiver(
            xarray_U.lon, xarray_U.lat,
            xarray_U,
            xarray_V,
            color = "k",
            transform = ccrs.PlateCarree(),
            scale = scale,
            regrid_shape = regrid_shape,
            width = width
        )

    qk = ax.quiverkey(Q, keyx, keyy, ref, label = f"{ref} " + key_label, labelpos = "E")
    
    return Q, qk

def rect (box, mask = None, mval = None):
    
    bbox = shp.Polygon([
    (box[0], box[2]), (box[1], box[2]),
    (box[1], box[3]), (box[0], box[3]),
    (box[0], box[2])
    ])
    
    rect = bbox
    
    if mask is not None :
        lat = mask['lat'].values
        lon = mask['lon'].values
        mask_values = mask.values
        
        binary_mask = (mask_values >= mval).astype(float)

        contours = measure.find_contours(binary_mask)

        polygons = []
        for contour in contours:
            contour_lat = np.interp(contour[:, 0], np.arange(len(lat)), lat)
            contour_lon = np.interp(contour[:, 1], np.arange(len(lon)), lon)
            coords = list(zip(contour_lon, contour_lat))
            poly = shp.Polygon(coords)
            if poly.is_valid and poly.area > 0.01:
                polygons.append(poly)

        mask_polygon = unary_union(polygons)
        
        rect = mask_polygon.intersection(bbox)
    
    return (rect)

def latex(unit_str):
    # Handle ** exponent notation (e.g., m**2, s**-1)
    s = re.sub(r"\*\*(-?\d+)", r"$^{\1}$", unit_str)
    
    # Handle trailing exponent without ** (e.g., yr-1)
    s = re.sub(r"([a-zA-Z])(-\d+)", r"\1$^{\2}$", s)
    
    return s

## Pre-process xarrays

def shift_lon(xarray):
    new_xarray = xarray.copy()
    new_xarray.coords["lon"] = (new_xarray.coords['lon'] + 180) % 360 -180 # shift longitude so that it is between -180 and 180
    new_xarray = new_xarray.sortby(new_xarray.lon) # sort the longitude after shift
    return new_xarray
    
def align_lat(xarray1, xarray2):
    new_xarray1 = xarray1.copy()
    new_xarray1['lat'] = xarray2.lat
    return new_xarray1

def align_lon(xarray1, xarray2):
    new_xarray1 = xarray1.copy()
    new_xarray1['lon'] = xarray2.lon
    return new_xarray1

def align_time(xarray1, xarray2):
    new_xarray1 = xarray1.copy()
    new_xarray1['time'] = xarray2.time
    return new_xarray1

def merge_CMIP(xarray_C6, xarray_C5) :
    xarray_C5C6 = xr.concat([xarray_C5, xarray_C6], dim = "time", combine_attrs = "drop_conflicts")
    xarray_C5C6 = xarray_C5C6.assign_attrs(
        scenario = xarray_C5.scenario + " and " + xarray_C6.scenario,
        model = "CMIP5-6",
        models_name = xarray_C5.models_name + xarray_C6.models_name,
        models_CMIP6 = [0] * len(xarray_C5.models_name) + [1] * len(xarray_C6.models_name)
    )
    
    xarray_C5C6["time"] = np.arange(len(xarray_C5C6.time))
    
    return xarray_C5C6

## Operations

def crop(xarray, box):
    """Crop an xarray over a box.

    Args:
        xarray (dataarray): Data to be cropped. 0 longitude is Greenwich.
        box (list): List of longitude and latitude defining the box.

    Returns:
        dataarray: Cropped xarray over the set box.
    """
    
    if not box :
        return xarray
    
    xarray = xarray.sortby("lat", ascending = True)
    
    lon_min, lon_max, lat_min, lat_max = box
    
    lat_slice = slice(lat_min, lat_max)
    lon_slice = slice(lon_min, lon_max)
    
    if np.max(np.abs([lon_min, lon_max])) <= 180 :
        xarray_copy = xarray.copy(deep = True)
    elif np.max(np.abs([lon_min, lon_max])) > 180 :
        xarray_copy = xarray.copy(deep = True)
        xarray_copy = xarray_copy.assign_coords(lon=((xarray_copy.lon + 360) % 360)).sortby("lon")
        
    cropped = (xarray_copy
        .sel(
            lon = lon_slice,
            lat = lat_slice   
        )
    )
        
    return cropped

def mask(xarray, mask, mval):
    dims_order = xarray.dims
    attributes = xarray.attrs
    mask = align_lon(mask, xarray)
    mask = align_lat(mask, xarray)
    masked = xr.where(mask == mval, xarray, np.nan).transpose(*dims_order)
    masked.attrs = attributes
    return masked

def spatial_mean(xarray, as_float = True):
    weights = np.cos(np.deg2rad(xarray.lat))
    weights.name = "weights"
    s_mean = xarray.weighted(weights).mean(dim = ["lon", "lat"])
    if as_float:
        return float(s_mean.values)
    else:
        return s_mean

def zonal_mean(xarray, as_float = True):
    weights = np.cos(np.deg2rad(xarray.lat))
    weights.name = "weights"
    s_mean = xarray.weighted(weights).mean(dim = ["lon"])
    if as_float:
        return float(s_mean.values)
    else:
        return s_mean

def spatial_std(xarray, as_float = True):
    weights = np.cos(np.deg2rad(xarray.lat))
    weights.name = "weights"
    s_std = xarray.weighted(weights).std(dim = ["lon", "lat"])
    if as_float:
        return float(s_std.values)
    else:
        return s_std

def clim(xarray, start, end, months = None):
    xarray_sliced = xarray.sel(time = slice(start, end))
    
    if months is not None:
        if months == [12, 1, 2, 3]:
            xarray_sliced = xarray_sliced.isel(time = slice(0, -1)) # ! so that the last december month is not computed for seasonal climatology
        xarray_sliced = xarray_sliced.sel(time = xarray_sliced['time.month'].isin(months)) # * seasonal slicing
        xarray_clim = (xarray_sliced
            .mean(dim = "time")
        )
    else:
        xarray_clim = (xarray_sliced
            .mean(dim = "time")
        )
    
    return xarray_clim, xarray_sliced

def temporal_regression(Y) :
    slope, intercept, pval, r2 = xr.apply_ufunc(
        linregress_1d,
        Y,              # spatial field
        Y["year"],      # x-serie
        input_core_dims = [["year"], ["year"]],
        output_core_dims = [[], [], [], []],
        vectorize = True,
        dask = "parallelized",  # if using dask-backed xarrays
        output_dtypes = [float, float, float, float]
    )

    ds_regression = xr.Dataset({
        "slope": slope,
        "intercept": intercept,
        "pval": pval,
        "r2": r2
    })
    
    return ds_regression

## Statistics

def linregress_1d(y, x, err = False):
    result = linregress(x, y)
    if err :
        return result.slope, result.intercept, result.pvalue, result.rvalue**2, result.stderr, result.intercept_stderr
    else :
        return result.slope, result.intercept, result.pvalue, result.rvalue**2

def regression(Y, x):
    slope, intercept, pval, r2 = xr.apply_ufunc(
        linregress_1d,
        Y,      # spatial field
        x,      # x-serie
        input_core_dims = [["time"], ["time"]],
        output_core_dims = [[], [], [], []],
        vectorize = True,
        dask = "parallelized",  # if using dask-backed xarrays
        output_dtypes = [float, float, float, float]
    )

    ds_regression = xr.Dataset({
        "slope": slope,
        "intercept": intercept,
        "pval": pval,
        "r2": r2
    })
    
    return ds_regression

def qr_multiple_reg_old (Y_da, X_df) :
    X_columns = X_df.columns
    Y_da_values = Y_da.values
    # Y_da_values = Y_da_values[~np.isnan(Y_da_values)]
    beta_da_list = []
    for m in range(len(X_columns)) :
        X = np.column_stack((np.ones(len(X_df)), X_df[X_columns[:m+1]].values))  # add intercept
        Q, R = np.linalg.qr(X) # get the QR decomposition for linear regression
        QTy = np.tensordot(Q.T, Y_da_values, axes=(1, 0))  # shape (p, lat, lon) # product $Q^T @ y$
        Rinv = np.linalg.inv(R) # inverse matrice $R^{-1}$
        beta = np.tensordot(Rinv, QTy, axes=(1, 0))  # shape (p, lat, lon) product $R^{-1} @ Q^T @ y$ which is the definition of parameter matrix $\beta$
        coef_names = ['intercept'] + list(X_df[X_columns[:m+1]].columns)
        beta_da = xr.DataArray(
            beta,
            dims=('coef', 'lat', 'lon'),
            coords={'coef': coef_names, 'lat': Y_da.lat, 'lon': Y_da.lon},
            name='beta'
        )
        beta_da_list.append(beta_da)
        
    beta_ds = xr.concat(beta_da_list, dim="nb_of_mode")
    
    return beta_ds

def qr_multiple_reg (Y_da, X_df):
    X_columns = X_df.columns
    
    slope_da_list = [] # store the slope regression coefficient
    r2_da_list = [] # store the R-squared coefficient of determination
    pval_da_list = [] # store the p-value associated to the regression

    Y_mean = Y_da.mean(dim="time") if "time" in Y_da.dims else Y_da.mean()
    SST = ((Y_da - Y_mean) ** 2).sum(dim="time") if "time" in Y_da.dims else ((Y_da - Y_mean) ** 2).sum()

    for m in range(len(X_columns)):
        X = np.column_stack((np.ones(len(X_df)), X_df[X_columns[:m+1]].values))  # add intercept
        Q, R = np.linalg.qr(X)
        QTy = np.tensordot(Q.T, Y_da.values, axes=(1, 0))
        Rinv = np.linalg.inv(R)
        slope = np.tensordot(Rinv, QTy, axes=(1, 0))  # shape (p, lat, lon)

        # Predictions and residuals
        y_hat = np.tensordot(X, slope, axes=(1, 0))  # (n, lat, lon)
        residuals = Y_da.values - y_hat
        SSR = np.sum(residuals**2, axis=0)
        n, p = X.shape
        sigma2 = SSR / (n - p)

        # Covariance, standard errors, t-stats, p-values
        RinvRT = Rinv @ Rinv.T
        se = np.sqrt(np.tensordot(np.diag(RinvRT), sigma2, axes=0))  # (p, lat, lon)
        tstat = slope / se
        pvals = 2 * (1 - t.cdf(np.abs(tstat), df=n - p))

        # R²
        SSE = SST.values - SSR
        R2 = SSE / SST.values

        coef_names = ['intercept'] + list(X_df[X_columns[:m+1]].columns)
        slope_da = xr.DataArray(
            slope,
            dims=('coef', 'lat', 'lon'),
            coords={'coef': coef_names, 'lat': Y_da.lat, 'lon': Y_da.lon},
            name='slope'
        )
        pval_da = xr.DataArray(
            pvals,
            dims=('coef', 'lat', 'lon'),
            coords={'coef': coef_names, 'lat': Y_da.lat, 'lon': Y_da.lon},
            name='pval'
        )
        r2_da = xr.DataArray(
            R2,
            dims=('lat', 'lon'),
            coords={'lat': Y_da.lat, 'lon': Y_da.lon},
            name='R2'
        )

        slope_da_list.append(slope_da)
        pval_da_list.append(pval_da)
        r2_da_list.append(r2_da)

    slope_ds = xr.concat(slope_da_list, dim="nb_of_mode")
    pval_ds = xr.concat(pval_da_list, dim="nb_of_mode")
    r2_ds = xr.concat(r2_da_list, dim="nb_of_mode")

    return xr.Dataset({"slope": slope_ds, "pval": pval_ds, "R2": r2_ds})

def constraint_1d(x, y, x_obs):
    slope, intercept, pvalue, r2 = linregress_1d(y, x)
    y_c = y + slope * (x_obs - x)

    _, axs = plt.subplots(
        nrows = 1, ncols = 2,
        width_ratios = [0.3, 1]
    )

    plt.subplots_adjust(left=0.05, right=0.95, wspace = 0.05)

    axs[1].plot(x, y, "o", label = "unconstrained")
    axs[1].plot(x, y_c, "o", label = "constrained")

    left, right = axs[1].get_xlim()
    bottom, top = axs[1].get_ylim()
    shift = (top - bottom) / 5

    x_temp = np.linspace(left, right, 1000)

    norm_X_np = norm.pdf(x_temp, loc = np.mean(x), scale = np.std(x))
    norm_X_np /= (1 + shift) * norm_X_np.max()
    # kde_X = gaussian_kde(x)
    # kde_X_np = kde_X(x)
    # kde_X_np /= 1.3 * kde_X_np.max()
    # ind_X = list((x >= np.mean(x))).index(True)

    axs[1].set_title("Emergent constraint between " + r"$X$" + " and " + r"$Y$" + "\nVariance reduction: " + fr"$1-\frac{{Var(Y|X_o)_n}}{{Var(Y)_n}}=\frac{{Var(\hat{{Y}})_n}}{{Var(Y)_n}}=\rho_{{X, Y}}^2={r2:.1f}$")
    axs[1].hlines([np.mean(y)], xmin = left, xmax = right, color = "C0")
    # axs[1].vlines([np.mean(X)], ymin = 0, ymax = 8, color = "k", ls = "--", alpha = 0.5)
    axs[1].plot(np.linspace(left, right, 100), slope * np.linspace(left, right, 100) + intercept, color = "k", alpha = 0.5)
    # axs[1].plot(np.linspace(0, 1, 100), slope_2 * np.linspace(0, 1, 100) + intercept_2)
    axs[1].scatter(x_obs, + bottom - shift, color = "red", label = r"$X_o$")
    axs[1].vlines([x_obs], ymin = + bottom - shift, ymax = np.mean(y_c), color = "red", ls = "--", alpha = 0.3)
    axs[1].hlines([np.mean(y_c)], xmin = left, xmax = x_obs, color = "red", ls = "--", alpha = 0.3)
    axs[1].plot(x_temp, norm_X_np + bottom - shift, color = "C0")
    axs[1].fill_between(
        x = x_temp, y1 = norm_X_np + bottom - shift, y2 = [bottom - shift] * len(norm_X_np),
        color = "C0", alpha = 0.1
    )
    axs[1].set_xlabel(r"$X$")
    axs[1].set_ylabel(r"$Y$")
    axs[1].set_xlim(left, right)
    axs[1].set_ylim(+ bottom - shift, top)

    axs[1].legend()

    axs[0].spines['top'].set_visible(False)
    axs[0].spines['bottom'].set_visible(False)
    axs[0].spines['left'].set_visible(False)

    y_temp  = np.linspace(+ bottom - shift, top, 1000)

    norm_y_np = norm.pdf(y_temp, loc = np.mean(y), scale = np.std(y))
    # kde_Y = gaussian_kde(y)
    # kde_Y_np = kde_Y(y)
    # # kde_Y_np /= 1.3 * kde_Y_np.max()
    ind_y = list((y_temp >= np.mean(y))).index(True)

    norm_y_c_np = norm.pdf(y_temp, loc = np.mean(y_c), scale = np.std(y_c))
    # kde_Y_c = gaussian_kde(y_c)
    # kde_Y_c_np = kde_Y_c(y_temp)
    # # kde_Y_c_np /= 1.3 * kde_Y_c_np.max()
    ind_y_c = list((y_temp >= np.mean(y_c))).index(True)

    axs[0].hlines([np.mean(y)], xmin = -norm_y_np[ind_y], xmax = 1, color = "C0", label = r"$E[Y]$")
    axs[0].hlines([np.mean(y_c)], xmin = -norm_y_c_np[ind_y_c], xmax = 1, color = "C1", label = r"$E[Y|X_o]$")
    axs[0].plot(-norm_y_np, y_temp , color = "C0")
    axs[0].fill_betweenx(
        y = y_temp, x1 = -norm_y_np, x2 = [0] * len(norm_y_np),
        color = "C0", alpha = 0.1
    )
    axs[0].boxplot(
        y, positions = [-0.1], tick_labels = [r"$y$"], patch_artist = True,
        boxprops = {"color": "C0", "facecolor": "C0", "alpha": 0.2}, whiskerprops = {"color": "C0"}, capprops = {"color": "C0"}, medianprops = {"color": "C0"}, flierprops = {"markeredgecolor": "C0", "markerfacecolor": "C0", "marker" : "o", "markersize": 3},
        widths = 0.05
    )
    axs[0].plot(-norm_y_c_np, y_temp, color = "C1")
    axs[0].fill_betweenx(
        y = y_temp, x1 = -norm_y_c_np, x2 = [0] * len(norm_y_c_np),
        color = "C1", alpha = 0.1
    )
    axs[0].boxplot(
        y_c, positions = [-0.2], tick_labels = [r"$y|x_o$"], patch_artist = True,
        boxprops = {"color": "C1", "facecolor": "C1", "alpha": 0.5}, whiskerprops = {"color": "C1"}, capprops = {"color": "C1"}, medianprops = {"color": "C1"}, flierprops = {"markeredgecolor": "C1", "markerfacecolor": "C1", "marker" : "o", "markersize": 3},
        widths = 0.05
    )

    left0 = max([norm_y_c_np.max(), norm_y_np.max()])
    axs[0].set_xlim(-left0*1.1, 0)
    axs[0].set_ylim(+ bottom - shift, top)
    axs[0].set_xticks([], [])
    axs[0].set_yticks([], [])
    # axs[0].legend()

    plt.tight_layout()
    
    return y_c, slope, intercept, pvalue, r2



def MCA(X, Y, M = 4):
    
    mca = xMCA(X, Y)
    mca.apply_coslat()
    mca.solve()
    
    pca_X = xMCA(X)
    pca_X.apply_coslat()
    pca_X.solve()

    pca_Y = xMCA(Y)
    pca_Y.apply_coslat()
    pca_Y.solve()

    # PCs (or singular decomposition) i.e projected data on eigenvector
    pcs = mca.pcs(n = M, scaling = "eigen") # ? not of great use when using MCA ? scaling should be rather "std" or "None"
    a, b = pcs["left"], pcs["right"]

    a_norm = (a - a.mean(dim = "time")) / a.std(dim = "time") # no dimension
    b_norm = (b - b.mean(dim = "time")) / b.std(dim = "time") # no dimension
    
    # EOFs (or singular values) i.e eigenvector
    eofs = mca.eofs(n = M)
    u, v = eofs["left"], eofs["right"]
    
    # Homogeneous & heterogeneous patterns
    HM = mca.homogeneous_patterns(n = M)[0] # as correlation
    HM_X, HM_Y = HM["left"]*X.std(dim = "time"), HM["right"]*Y.std(dim = "time") # as covariance
    
    HT = mca.heterogeneous_patterns(n = M)[0] # as correlation
    HT_X, HT_Y = HT["left"]*X.std(dim = "time"), HT["right"]*Y.std(dim = "time") # as covariance
    
    # Squared covariance fraction i.e a metric on the importance of modes
    scf = mca.scf(n = M)
    
    # Explained variance of the field from MCA
    expvar_X = (a.var(dim = "time", ddof = 1) / pca_X.variance().sum()) * 100 # how much of initial variance of X is a's variance representing ?
    expvar_Y = (b.var(dim = "time", ddof = 1) / pca_Y.variance().sum()) * 100 # how much of initial variance of Y is b's variance representing ?
    
    # Explained variance of the field from PCA
    expvar_pca_X = (pca_X.variance() / pca_X.variance().sum()) * 100
    expvar_pca_Y = (pca_Y.variance() / pca_Y.variance().sum()) * 100
    
    PC = xr.merge([a_norm.rename("a"), b_norm.rename("b"), scf.rename("scf")])
    EOF = xr.merge([u.rename("u"), v.rename("v")])
    HM = xr.merge([HM_X.rename("X"), HM_Y.rename("Y")])
    HT = xr.merge([HT_X.rename("X"), HT_Y.rename("Y")])
    expvar = xr.merge([expvar_X.rename("X"), expvar_Y.rename("Y")])
    expvar_pca = xr.merge([expvar_pca_X.rename("X"), expvar_pca_Y.rename("Y")])
    
    return PC, EOF, HM_X, HM_Y, HT_X, HT_Y, expvar, expvar_pca

def comp_HM_HT (
    X, Y,
    box_X = None, mask_X = None, mval_X = None,
    box_Y = None, mask_Y = None, mval_Y = None,
    M = 4,
    MCA_only = False,
    box_SAsia = [50, 110, -15, 40]
) :
    
    X_init = X.copy(deep = True)
    
    if box_X is not None:
        X_box = crop(X, box = box_X) # croped field
        X = X_box.copy(deep = True)
    if mask_X is not None:
        # X_box_masked = X_box.where(crop(mask_X, box = box_X) == mval_X) # croped and masked field
        X_box_masked = mask(X_box, crop(mask_X, box = box_X), mval_X) # croped and masked field
        X = X_box_masked.copy(deep = True)

    Y_init = Y.copy(deep = True)
    
    if box_Y is not None:
        Y_box = crop(Y, box = box_Y) # croped field
        Y = Y_box.copy(deep = True)
    if mask_Y is not None:
        # Y_box_masked = Y_box.where(crop(mask_Y, box = box_Y) == mval_Y) # croped and masked field
        Y_box_masked = mask(Y_box, crop(mask_Y, box = box_Y), mval_Y) # croped and masked field
        Y = Y_box_masked.copy(deep = True)
    
    PC, EOF, HM_X, HM_Y, HT_X, HT_Y, expvar, expvar_pca = MCA(X, Y, M = M)
    
    if MCA_only:
        return X, Y, PC, EOF, HM_X, HM_Y, HT_X, HT_Y, expvar, expvar_pca
    
    EC_a_label = [f"a{i}" for i in range (M)]
    EC_a_df = pd.DataFrame(
        [PC["a"].isel(mode = i).values for i in range (M)],
        index = EC_a_label
    ).T
    
    HM_X_init_list = []
    HT_Y_init_list = []

    X_SA = crop(X_init, box = box_SAsia)
    Y_SA = crop(Y_init, box = box_SAsia)
    
    HM_X_SA_list = []
    HT_Y_SA_list = []
                 
    for m in range(M) :
    
        HM_X_init_m = qr_multiple_reg(X_init, EC_a_df[[f"a{m}"]]).isel(nb_of_mode = 0).sel(coef = f"a{m}")
        HT_Y_init_m = qr_multiple_reg(Y_init, EC_a_df[[f"a{m}"]]).isel(nb_of_mode = 0).sel(coef = f"a{m}")
        
        HM_X_SA_m = qr_multiple_reg(X_SA, EC_a_df[[f"a{m}"]]).isel(nb_of_mode = 0).sel(coef = f"a{m}")
        HT_Y_SA_m = qr_multiple_reg(Y_SA, EC_a_df[[f"a{m}"]]).isel(nb_of_mode = 0).sel(coef = f"a{m}")
        
        HM_X_init_m = HM_X_init_m.expand_dims("mode")
        HM_X_init_m = HM_X_init_m.assign_coords(mode=[m])
        HM_X_init_list.append(HM_X_init_m)
        
        HT_Y_init_m = HT_Y_init_m.expand_dims("mode")
        HT_Y_init_m = HT_Y_init_m.assign_coords(mode=[m])
        HT_Y_init_list.append(HT_Y_init_m)

        HM_X_SA_m = HM_X_SA_m.expand_dims("mode")
        HM_X_SA_m = HM_X_SA_m.assign_coords(mode=[m])
        HM_X_SA_list.append(HM_X_SA_m)
        
        HT_Y_SA_m = HT_Y_SA_m.expand_dims("mode")
        HT_Y_SA_m = HT_Y_SA_m.assign_coords(mode=[m])
        HT_Y_SA_list.append(HT_Y_SA_m)
    
    HM_X_init = xr.concat(HM_X_init_list, dim = "mode")
    HT_Y_init = xr.concat(HT_Y_init_list, dim = "mode")
    
    HM_X_init = HM_X_init.assign_attrs(
        units = X_init.units
    )

    HT_Y_init = HT_Y_init.assign_attrs(
        units = Y_init.units
    )

    HM_X_SA = xr.concat(HM_X_SA_list, dim = "mode")
    HT_Y_SA = xr.concat(HT_Y_SA_list, dim = "mode")

    HM_X_SA = HM_X_SA.assign_attrs(
        units = X_init.units
    )

    HT_Y_SA = HT_Y_SA.assign_attrs(
        units = Y_init.units
    )

    return X, Y, HM_X_SA, HM_X_init, HT_Y_SA, HT_Y_init, PC, EOF, HM_X, HM_Y, HT_X, HT_Y, expvar, expvar_pca
    