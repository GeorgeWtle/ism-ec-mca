import xarray as xr
import numpy as np

from init.func import *
from init.const import *

### MULTI MODEL ENSEMBLE (MME) - CMIP5 & CMIP6 ###

#* Precipitation (pr)
## Change: 2081-2100 vs 1995-2014
pr_change_JJAS_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/pr/pr_change_1995_2014_2081_2100_JJAS.nc")["pr change"]
pr_change_JJAS_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/pr/pr_change_1995_2014_rcp85_2081_2100_JJAS.nc")["pr change"]
pr_change_JJAS = merge_CMIP(pr_change_JJAS_6, pr_change_JJAS_5)
pr_change_JJAS_SA = crop(pr_change_JJAS, box_SAsia)

pr_change_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/pr/pr_change_1995_2014_2081_2100_Y.nc")["pr change"]
pr_change_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/pr/pr_change_1995_2014_rcp85_2081_2100_Y.nc")["pr change"]
pr_change = merge_CMIP(pr_change_6, pr_change_5)

## Trend: 1979-2024
pr_trend_JJAS_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/pr/pr_trend_1979_2024_JJAS.nc")["pr trend"]
pr_trend_JJAS_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/pr/pr_trend_1979_2024_JJAS.nc")["pr trend"]
pr_trend_JJAS = merge_CMIP(pr_trend_JJAS_6, pr_trend_JJAS_5)
pr_trend_JJAS_SA = crop(pr_trend_JJAS, box = box_SAsia)

## Clim: 1995-2014
pr_clim_JJAS_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/pr/pr_clim_1995_2014_JJAS.nc")["pr clim"]
pr_clim_JJAS_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/pr/pr_clim_1995_2014_JJAS.nc")["pr clim"]
pr_clim_JJAS = merge_CMIP(pr_clim_JJAS_6, pr_clim_JJAS_5)

pr_clim_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/pr/pr_clim_1995_2014_Y.nc")["pr clim"]
pr_clim_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/pr/pr_clim_1995_2014_Y.nc")["pr clim"]
pr_clim = merge_CMIP(pr_clim_6, pr_clim_5)

## Time series
pr_TS_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/pr/pr_mean_time_serie_GLO.nc")["pr"]
pr_TS_6.attrs["scenario"] = "ssp585"
pr_TS_6.attrs["units"] = "mm day-1"
pr_TS_6 = pr_TS_6 * 86400

pr_TS_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/pr/pr_mean_time_serie_GLO.nc")["pr"]
pr_TS_5.attrs["scenario"] = "rcp85"
pr_TS_5.attrs["units"] = "mm day-1"
pr_TS_5 = pr_TS_5 * 86400

# pr_TS = xr.concat(
#     [pr_TS_5, pr_TS_6],
#     dim = "model"
# )

pr_TS_India_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/pr/pr_mean_time_serie_India.nc")["pr"]
pr_TS_India_6.attrs["scenario"] = "ssp585"
pr_TS_India_6.attrs["units"] = "mm day-1"
pr_TS_India_6 = pr_TS_India_6 * 86400

pr_TS_India_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/pr/pr_mean_time_serie_India.nc")["pr"]
pr_TS_India_5.attrs["scenario"] = "rcp85"
pr_TS_India_5.attrs["units"] = "mm day-1"
pr_TS_India_5 = pr_TS_India_5 * 86400

# pr_TS_India = xr.concat(
#     [pr_TS_India_5, pr_TS_India_6],
#     dim = "model"
# )

# Land mask
# land_mask = xr.open_dataset("scratchu/gwhittle/mer0.nc").nmask
# land_mask = align_lat(land_mask, pr_change_JJAS)
# land_mask = shift_lon(land_mask)

#* Temperature (tas)
## Change: 2081-2100 vs 1995-2014
tas_change_JJAS_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/tas/tas_change_1995_2014_2081_2100_JJAS.nc")["tas change"]
tas_change_JJAS_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/tas/tas_change_1995_2014_rcp85_2081_2100_JJAS.nc")["tas change"]
tas_change_JJAS = merge_CMIP(tas_change_JJAS_6, tas_change_JJAS_5)
mean_tas_change_JJAS = spatial_mean(tas_change_JJAS, as_float = False)
tas_change_JJAS_SA = crop(tas_change_JJAS, box_SAsia)

tas_change_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/tas/tas_change_1995_2014_2081_2100_Y.nc")["tas change"]
tas_change_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/tas/tas_change_1995_2014_rcp85_2081_2100_Y.nc")["tas change"]
tas_change = merge_CMIP(tas_change_6, tas_change_5)
mean_tas_change = spatial_mean(tas_change, as_float = False)
tas_change_SA = crop(tas_change, box_SAsia)

## Time series
tas_TS_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/tas/tas_mean_time_serie_GLO.nc")["tas"]
tas_TS_6.attrs["scenario"] = "ssp585"
tas_TS_6.attrs["units"] = "°C"
tas_TS_6 = tas_TS_6 - 273.15

tas_TS_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/tas/tas_mean_time_serie_GLO.nc")["tas"]
tas_TS_5.attrs["scenario"] = "rcp85"
tas_TS_5.attrs["units"] = "°C"
tas_TS_5 = tas_TS_5 - 273.15

tas_TS = xr.concat(
    [tas_TS_5, tas_TS_6],
    dim = "model"
)

tas_NH_TS_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/tas/tas_mean_time_serie_NH.nc")["tas"]
tas_NH_TS_6.attrs["scenario"] = "ssp585"
tas_NH_TS_6.attrs["units"] = "°C"
tas_NH_TS_6 = tas_NH_TS_6 - 273.15

tas_NH_TS_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/tas/tas_mean_time_serie_NH.nc")["tas"]
tas_NH_TS_5.attrs["scenario"] = "rcp85"
tas_NH_TS_5.attrs["units"] = "°C"
tas_NH_TS_5 = tas_NH_TS_5 - 273.15

tas_NH_TS = xr.concat(
    [tas_NH_TS_5, tas_NH_TS_6],
    dim = "model"
)

tas_SH_TS_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/tas/tas_mean_time_serie_SH.nc")["tas"]
tas_SH_TS_6.attrs["scenario"] = "ssp585"
tas_SH_TS_6.attrs["units"] = "°C"
tas_SH_TS_6 = tas_SH_TS_6 - 273.15

tas_SH_TS_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/tas/tas_mean_time_serie_SH.nc")["tas"]
tas_SH_TS_5.attrs["scenario"] = "rcp85"
tas_SH_TS_5.attrs["units"] = "°C"
tas_SH_TS_5 = tas_SH_TS_5 - 273.15

tas_SH_TS = xr.concat(
    [tas_SH_TS_5, tas_SH_TS_6],
    dim = "model"
)

tas_AMTG_N_TS_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/tas/tas_mean_time_serie_AMTG_N.nc")["tas"]
tas_AMTG_N_TS_6.attrs["scenario"] = "ssp585"
tas_AMTG_N_TS_6.attrs["units"] = "°C"
tas_AMTG_N_TS_6 = tas_AMTG_N_TS_6 - 273.15

tas_AMTG_N_TS_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/tas/tas_mean_time_serie_AMTG_N.nc")["tas"]
tas_AMTG_N_TS_5.attrs["scenario"] = "rcp85"
tas_AMTG_N_TS_5.attrs["units"] = "°C"
tas_AMTG_N_TS_5 = tas_AMTG_N_TS_5 - 273.15

tas_AMTG_N_TS = xr.concat(
    [tas_AMTG_N_TS_5, tas_AMTG_N_TS_6],
    dim = "model"
)

tas_AMTG_S_TS_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/tas/tas_mean_time_serie_AMTG_S.nc")["tas"]
tas_AMTG_S_TS_6.attrs["scenario"] = "ssp585"
tas_AMTG_S_TS_6.attrs["units"] = "°C"
tas_AMTG_S_TS_6 = tas_AMTG_S_TS_6 - 273.15

tas_AMTG_S_TS_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/tas/tas_mean_time_serie_AMTG_S.nc")["tas"]
tas_AMTG_S_TS_5.attrs["scenario"] = "rcp85"
tas_AMTG_S_TS_5.attrs["units"] = "°C"
tas_AMTG_S_TS_5 = tas_AMTG_S_TS_5 - 273.15

tas_AMTG_S_TS = xr.concat(
    [tas_AMTG_S_TS_5, tas_AMTG_S_TS_6],
    dim = "model"
)

## Trend: 1979-2024
tas_trend_JJAS_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/tas/tas_trend_1979_2024_JJAS.nc")["tas trend"]
tas_trend_JJAS_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/tas/tas_trend_1979_2024_JJAS.nc")["tas trend"]
tas_trend_JJAS = merge_CMIP(tas_trend_JJAS_6, tas_trend_JJAS_5)
tas_trend_JJAS_SA = crop(tas_trend_JJAS, box = box_SAsia)

## Clim: 1995-2014
tas_clim_JJAS_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/tas/tas_clim_1995_2014_JJAS.nc")["tas clim"]
tas_clim_JJAS_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/tas/tas_clim_1995_2014_JJAS.nc")["tas clim"]
tas_clim_JJAS = merge_CMIP(tas_clim_JJAS_6, tas_clim_JJAS_5)

#* Sea surface temperature (sst)
#! as masked tas
## Change: 2081-2100 vs 1995-2014
sst_change_JJAS = mask(tas_change_JJAS, land_mask, 1)
sst_change_JJAS_SA = crop(sst_change_JJAS, box_SAsia)

sst_change = mask(tas_change, land_mask, 1)
sst_change_SA = crop(sst_change, box_SAsia)

## Trend: 1979-2024
sst_trend_JJAS = mask(tas_trend_JJAS, land_mask, 1)
sst_trend_JJAS_SA = crop(sst_trend_JJAS, box_SAsia)

## Clim: 1995-2014
sst_clim_JJAS = mask(tas_clim_JJAS, land_mask, 1)
sst_clim_JJAS_SA = crop(sst_clim_JJAS, box_SAsia)

#* Pressure at sea level (psl)
## Change: 2081-2100 vs 1995-2014
psl_change_JJAS_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/psl/psl_change_1995_2014_2081_2100_JJAS.nc")["psl change"]
psl_change_JJAS_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/psl/psl_change_1995_2014_rcp85_2081_2100_JJAS.nc")["psl change"]
psl_change_JJAS = merge_CMIP(psl_change_JJAS_6, psl_change_JJAS_5)

## Trend: 1979-2024
psl_trend_JJAS_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/psl/psl_trend_1979_2024_JJAS.nc")["psl trend"]
psl_trend_JJAS_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/psl/psl_trend_1979_2024_JJAS.nc")["psl trend"]
psl_trend_JJAS = merge_CMIP(psl_trend_JJAS_6, psl_trend_JJAS_5)

## Clim: 1995-2014
psl_clim_JJAS_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/psl/psl_clim_1995_2014_JJAS.nc")["psl clim"]
psl_clim_JJAS_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/psl/psl_clim_1995_2014_JJAS.nc")["psl clim"]
psl_clim_JJAS = merge_CMIP(psl_clim_JJAS_6, psl_clim_JJAS_5)

#* Zonal wind at 850hPa (ua850)
# ## Change: 2081-2100 vs 1995-2014
# ua850_change_JJAS_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/ua/ua850_change_1995_2014_2081_2100_JJAS.nc")["ua change"]
# ua850_change_JJAS_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/ua/ua850_change_1995_2014_rcp85_2081_2100_JJAS.nc")["ua change"]
# ua850_change_JJAS = merge_CMIP(ua850_change_JJAS_6, ua850_change_JJAS_5)

# ## Trend: 1979-2024
# ua850_trend_JJAS_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/ua/ua850_trend_1979_2024_JJAS.nc")["ua trend"]
# ua850_trend_JJAS_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/ua/ua850_trend_1979_2024_JJAS.nc")["ua trend"]
# ua850_trend_JJAS = merge_CMIP(ua850_trend_JJAS_6, ua850_trend_JJAS_5)

## Clim: 1995-2014
ua850_clim_JJAS_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/ua/ua850_clim_1995_2014_JJAS.nc")["ua clim"]
ua850_clim_JJAS_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/ua/ua850_clim_1995_2014_JJAS.nc")["ua clim"]
ua850_clim_JJAS = merge_CMIP(ua850_clim_JJAS_6, ua850_clim_JJAS_5)

#* Meridional wind at 850hPa (va850)
# ## Change: 2081-2100 vs 1995-2014
# va850_change_JJAS_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/va/va850_change_1995_2014_2081_2100_JJAS.nc")["va change"]
# va850_change_JJAS_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/va/va850_change_1995_2014_rcp85_2081_2100_JJAS.nc")["va change"]
# va850_change_JJAS = merge_CMIP(va850_change_JJAS_6, va850_change_JJAS_5)

# ## Trend: 1979-2024
# va850_trend_JJAS_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/va/va850_trend_1979_2024_JJAS.nc")["va trend"]
# va850_trend_JJAS_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/va/va850_trend_1979_2024_JJAS.nc")["va trend"]
# va850_trend_JJAS = merge_CMIP(va850_trend_JJAS_6, va850_trend_JJAS_5)

## Clim: 1995-2014
va850_clim_JJAS_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/va/va850_clim_1995_2014_JJAS.nc")["va clim"]
va850_clim_JJAS_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/va/va850_clim_1995_2014_JJAS.nc")["va clim"]
va850_clim_JJAS = merge_CMIP(va850_clim_JJAS_6, va850_clim_JJAS_5)

#* Velocity potential at 200hPa (vp200)
## Change: 2081-2100 vs 1995-2014
vp200_change_JJAS_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/vp200/vp200_change_1995_2014_2081_2100_JJAS.nc")["vp200 change"]
vp200_change_JJAS_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/vp200/vp200_change_1995_2014_rcp85_2081_2100_JJAS.nc")["vp200 change"]
vp200_change_JJAS = merge_CMIP(vp200_change_JJAS_6, vp200_change_JJAS_5)

## Trend: 1979-2024
vp200_trend_JJAS_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/vp200/vp200_trend_1979_2024_JJAS.nc")["vp200 trend"]
vp200_trend_JJAS_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/vp200/vp200_trend_1979_2024_JJAS.nc")["vp200 trend"]
vp200_trend_JJAS = merge_CMIP(vp200_trend_JJAS_6, vp200_trend_JJAS_5)

## Clim: 1995-2014
vp200_clim_JJAS_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/vp200/vp200_clim_1995_2014_JJAS.nc")["vp200 clim"]
vp200_clim_JJAS_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/vp200/vp200_clim_1995_2014_JJAS.nc")["vp200 clim"]
vp200_clim_JJAS = merge_CMIP(vp200_clim_JJAS_6, vp200_clim_JJAS_5)

#* Velocity potential at 200hPa (vp200) - JJAS Monsoon component (Tanaka et al., 2006)
## Change: 2081-2100 vs 1995-2014
# vpM200_change_JJAS_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/vpM200/vpM200_change_1995_2014_2081_2100_JJAS.nc")["vpM200 change"]
# vpM200_change_JJAS_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/vpM200/vpM200_change_1995_2014_rcp85_2081_2100_JJAS.nc")["vpM200 change"]
# vpM200_change_JJAS = merge_CMIP(vpM200_change_JJAS_6, vpM200_change_JJAS_5)

# ## Trend: 1979-2024
# vpM200_trend_JJAS_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/vpM200/vpM200_trend_1979_2024_JJAS.nc")["vpM200 trend"]
# vpM200_trend_JJAS_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/vpM200/vpM200_trend_1979_2024_JJAS.nc")["vpM200 trend"]
# vpM200_trend_JJAS = merge_CMIP(vpM200_trend_JJAS_6, vpM200_trend_JJAS_5)

# ## Clim: 1995-2014
# vpM200_clim_JJAS_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/vpM200/vpM200_clim_1995_2014_JJAS.nc")["vpM200 clim"]
# vpM200_clim_JJAS_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/vpM200/vpM200_clim_1995_2014_JJAS.nc")["vpM200 clim"]
# vpM200_clim_JJAS = merge_CMIP(vpM200_clim_JJAS_6, vpM200_clim_JJAS_5)

### LARGE ENSEMBLE (LE) - MIROC6 ###

## Change: 2081-2100 vs 1995-2014
pr_change_JJAS_MIROC6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/pr/MIROC6/pr_change_1995_2014_2081_2100_JJAS.nc")["pr change"]
pr_change_JJAS_MIROC6 = xr.concat([pr_change_JJAS_6.isel(time = 4), pr_change_JJAS_MIROC6], dim = "run")
pr_change_JJAS_MIROC6_SA = crop(pr_change_JJAS_MIROC6, box = box_SAsia)

## Trend: 1979-2024
pr_trend_JJAS_MIROC6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/pr/MIROC6/pr_trend_1979_2024_JJAS.nc")["pr trend"]
pr_trend_JJAS_MIROC6 = xr.concat([pr_trend_JJAS_6.isel(time = 4), pr_trend_JJAS_MIROC6], dim = "run")
pr_trend_JJAS_MIROC6_SA = crop(pr_trend_JJAS_MIROC6, box = box_SAsia)

## Clim: 1995-2014
pr_clim_JJAS_MIROC6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/pr/MIROC6/pr_clim_1995_2014_JJAS.nc")["pr clim"]
pr_clim_JJAS_MIROC6 = xr.concat([pr_clim_JJAS_6.isel(time = 4), pr_clim_JJAS_MIROC6], dim = "run")
pr_clim_JJAS_MIROC6_SA = crop(pr_clim_JJAS_MIROC6, box = box_SAsia)