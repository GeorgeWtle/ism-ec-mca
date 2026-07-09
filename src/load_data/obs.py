import xarray as xr
import numpy as np

from init.func import *

#* ERA5 - reanalysis
## pr
pr_ERA5 = xr.open_dataset("scratchu/gwhittle/obs/ERA5/ERA5_PR_194001_202412.T127.nc")["tp"]
pr_clim_ERA5_JJAS = xr.open_dataset("data/gwhittle/obs/ERA5/pr_clim_1995_2014_JJAS.nc")["tp"]
pr_trend_ERA5_JJAS = xr.open_dataset("data/gwhittle/obs/ERA5/pr_trend_1979_2024_JJAS.nc")["slope"]

#* GPCP - pr
pr_GPCP = xr.open_dataset("scratchu/gwhittle/obs/GPCP/GPCP_197901_202509.T127.nc")["precip"]
pr_clim_GPCP_JJAS = xr.open_dataset("data/gwhittle/obs/GPCP/pr_clim_1995_2014_JJAS.nc")["precip"]
pr_trend_GPCP_JJAS = xr.open_dataset("data/gwhittle/obs/GPCP/pr_trend_1979_2024_JJAS.nc")["slope"]

#* CMAP - pr
pr_CMAP = xr.open_dataset("scratchu/gwhittle/obs/CMAP/CMAP_197901_202604.T127.nc")["precip"]
pr_clim_CMAP_JJAS = xr.open_dataset("data/gwhittle/obs/CMAP/pr_clim_1995_2014_JJAS.nc")["precip"]
pr_trend_CMAP_JJAS = xr.open_dataset("data/gwhittle/obs/CMAP/pr_trend_1979_2024_JJAS.nc")["slope"]

#* MSEWP - pr
pr_MSWEP = xr.open_dataset("scratchu/gwhittle/obs/MSWEP3.16/MSWEP3.16_197901_202505.T127.nc")["precipitation"]
pr_MSWEP = pr_MSWEP / 30 #! MSWEP is in mm/month
pr_clim_MSWEP_JJAS = xr.open_dataset("data/gwhittle/obs/MSWEP3.16/pr_clim_1995_2014_JJAS.nc")["precipitation"]
pr_trend_MSWEP_JJAS = xr.open_dataset("data/gwhittle/obs/MSWEP3.16/pr_trend_1979_2024_JJAS.nc")["slope"]


