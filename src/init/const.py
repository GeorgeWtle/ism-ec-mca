from init.lib import *
from init.func import merge_CMIP, align_lat, shift_lon, rect

## Constants

COLUMNWIDTH = 228 / 72.27 # pts to inch
TEXTWIDTH =  468 / 72.27 # pts to inch
TEXTHEIGHT = 634.43 / 72.27 # pts to inch
GOLDEN_RATIO = ((1 + 5**0.5) / 2)

## Definition of LaTeX font and size
plt.style.use("ametsoc.mplstyle")

## Definition for figsize
plt.rcParams["figure.figsize"] = (TEXTWIDTH, TEXTWIDTH * GOLDEN_RATIO)
plt.rcParams["figure.figsize"] = (TEXTWIDTH, TEXTWIDTH / GOLDEN_RATIO)

labels = string.ascii_lowercase
LABELS = string.ascii_uppercase

# Land mask
pr_change_6 = xr.open_dataset("data/gwhittle/CMIP6/T127/ssp585/pr/pr_change_1995_2014_2081_2100_Y.nc")["pr change"]
pr_change_5 = xr.open_dataset("data/gwhittle/CMIP5/T127/rcp85/pr/pr_change_1995_2014_rcp85_2081_2100_Y.nc")["pr change"]
pr_change = merge_CMIP(pr_change_6, pr_change_5)
land_mask = xr.open_dataset("scratchu/gwhittle/mer0.nc").nmask
land_mask = align_lat(land_mask, pr_change)
land_mask = shift_lon(land_mask)

# spatial box
box_WEurope = [-20, 40, 33, 63]
box_SAsia = [50, 110, -15, 40]
box_India = [70, 90, 0, 30]
box_Equatorial = [-180, 180, -20, 20]
box_WPacific = [120, 200, -20, 30]
box_India_2 = [65, 95, 0, 30]
rect_India = rect(box_India_2)
rect_India_land = rect(box_India_2, mask = land_mask, mval = 1)
box_GLO = [-180, 180, -90, 90]
box_Equatorial_India = [50, 160, -15, 25] # for pacific effect on PR
box_Equatorial_India2 = [50, 160, -20, 40]
box_Trop = [-180, 180, -20, 40]

lon_min, lon_max = box_SAsia[0], box_SAsia[1]
lat_min, lat_max = box_SAsia[2], box_SAsia[3]
resolution = 1

bottom = [(lon, lat_min) for lon in np.arange(lon_min, lon_max, resolution)]
right = [(lon_max, lat) for lat in np.arange(lat_min, lat_max, resolution)]
top = [(lon, lat_max) for lon in np.arange(lon_max, lon_min, -resolution)]
left = [(lon_min, lat) for lat in np.arange(lat_max, lat_min, -resolution)]

coords_SAsia = bottom + right + top + left + [bottom[0]]

CMIP6_True = np.array(pr_change.models_CMIP6).astype(bool)
CMIP6_True_no_46 = np.delete(CMIP6_True, 46)

# some models names
CNRM_models = ['CNRM-CM6-1', 'CNRM-CM6-1-HR', 'CNRM-ESM2-1']
# print("CNRM models:", CNRM_models)
IPSL_models = ['IPSL-CM6A-LR']
# print("IPSL models:", IPSL_models)

# model to color
model_to_color = {
    'CNRM-CM6-1': '#74a9cf',
    'CNRM-CM6-1-HR': '#023858',
    'CNRM-ESM2-1': '#0570b0',
    'IPSL-CM6A-LR': '#feb24c',
    'NorESM2-MM': '#de2d26',
    'CAS-ESM2-0': '#31a354',
    'MME': 'C7'
}

var_to_color = {
    'Precipitation': '#1b9e77',
    'Temperature': '#d95f02',
    'Sea level pressure': "#7570b3"
}

# Color list was taken from Nicolas P. Rougier work,
# "Scientific Visualization: Python + Matplotlib",
# freely available here: https://inria.hal.science/hal-03427242/document
colors = {
    "red": {
        0: "#ffebee",
        1: "#ffcdd2",
        2: "#ef9a9a",
        3: "#e57373",
        4: "#ef5350",
        5: "#f44336",
        6: "#e53935",
        7: "#d32f2f",
        8: "#c62828",
        9: "#b71c1c",
    },
    "pink": {
        0: "#fce4ec",
        1: "#f8bbd0",
        2: "#f48fb1",
        3: "#f06292",
        4: "#ec407a",
        5: "#e91e63",
        6: "#d81b60",
        7: "#c2185b",
        8: "#ad1457",
        9: "#880e4f",
    },
    "purple": {
        0: "#f3e5f5",
        1: "#e1bee7",
        2: "#ce93d8",
        3: "#ba68c8",
        4: "#ab47bc",
        5: "#9c27b0",
        6: "#8e24aa",
        7: "#7b1fa2",
        8: "#6a1b9a",
        9: "#4a148c",
    },
    "d.purple": {
        0: "#ede7f6",
        1: "#d1c4e9",
        2: "#b39ddb",
        3: "#9575cd",
        4: "#7e57c2",
        5: "#673ab7",
        6: "#5e35b1",
        7: "#512da8",
        8: "#4527a0",
        9: "#311b92",
    },
    "indigo": {
        0: "#e8eaf6",
        1: "#c5cae9",
        2: "#9fa8da",
        3: "#7986cb",
        4: "#5c6bc0",
        5: "#3f51b5",
        6: "#3949ab",
        7: "#303f9f",
        8: "#283593",
        9: "#1a237e",
    },
    "blue": {
        0: "#e3f2fd",
        1: "#bbdefb",
        2: "#90caf9",
        3: "#64b5f6",
        4: "#42a5f5",
        5: "#2196f3",
        6: "#1e88e5",
        7: "#1976d2",
        8: "#1565c0",
        9: "#0d47a1",
    },
    "l.blue": {
        0: "#e1f5fe",
        1: "#b3e5fc",
        2: "#81d4fa",
        3: "#4fc3f7",
        4: "#29b6f6",
        5: "#03a9f4",
        6: "#039be5",
        7: "#0288d1",
        8: "#0277bd",
        9: "#01579b",
    },
    "cyan": {
        0: "#e0f7fa",
        1: "#b2ebf2",
        2: "#80deea",
        3: "#4dd0e1",
        4: "#26c6da",
        5: "#00bcd4",
        6: "#00acc1",
        7: "#0097a7",
        8: "#00838f",
        9: "#006064",
    },
    "teal": {
        0: "#e0f2f1",
        1: "#b2dfdb",
        2: "#80cbc4",
        3: "#4db6ac",
        4: "#26a69a",
        5: "#009688",
        6: "#00897b",
        7: "#00796b",
        8: "#00695c",
        9: "#004d40",
    },
    "green": {
        0: "#e8f5e9",
        1: "#c8e6c9",
        2: "#a5d6a7",
        3: "#81c784",
        4: "#66bb6a",
        5: "#4caf50",
        6: "#43a047",
        7: "#388e3c",
        8: "#2e7d32",
        9: "#1b5e20",
    },
    "l.green": {
        0: "#f1f8e9",
        1: "#dcedc8",
        2: "#c5e1a5",
        3: "#aed581",
        4: "#9ccc65",
        5: "#8bc34a",
        6: "#7cb342",
        7: "#689f38",
        8: "#558b2f",
        9: "#33691e",
    },
    "lime": {
        0: "#f9fbe7",
        1: "#f0f4c3",
        2: "#e6ee9c",
        3: "#dce775",
        4: "#d4e157",
        5: "#cddc39",
        6: "#c0ca33",
        7: "#afb42b",
        8: "#9e9d24",
        9: "#827717",
    },
    "yellow": {
        0: "#fffde7",
        1: "#fff9c4",
        2: "#fff59d",
        3: "#fff176",
        4: "#ffee58",
        5: "#ffeb3b",
        6: "#fdd835",
        7: "#fbc02d",
        8: "#f9a825",
        9: "#f57f17",
    },
    "amber": {
        0: "#fff8e1",
        1: "#ffecb3",
        2: "#ffe082",
        3: "#ffd54f",
        4: "#ffca28",
        5: "#ffc107",
        6: "#ffb300",
        7: "#ffa000",
        8: "#ff8f00",
        9: "#ff6f00",
    },
    "orange": {
        0: "#fff3e0",
        1: "#ffe0b2",
        2: "#ffcc80",
        3: "#ffb74d",
        4: "#ffa726",
        5: "#ff9800",
        6: "#fb8c00",
        7: "#f57c00",
        8: "#ef6c00",
        9: "#e65100",
    },
    "d.orange": {
        0: "#fbe9e7",
        1: "#ffccbc",
        2: "#ffab91",
        3: "#ff8a65",
        4: "#ff7043",
        5: "#ff5722",
        6: "#f4511e",
        7: "#e64a19",
        8: "#d84315",
        9: "#bf360c",
    },
    "brown": {
        0: "#efebe9",
        1: "#d7ccc8",
        2: "#bcaaa4",
        3: "#a1887f",
        4: "#8d6e63",
        5: "#795548",
        6: "#6d4c41",
        7: "#5d4037",
        8: "#4e342e",
        9: "#3e2723",
    },
    "grey": {
        0: "#fafafa",
        1: "#f5f5f5",
        2: "#eeeeee",
        3: "#e0e0e0",
        4: "#bdbdbd",
        5: "#9e9e9e",
        6: "#757575",
        7: "#616161",
        8: "#424242",
        9: "#212121",
    },
    "blue grey": {
        0: "#eceff1",
        1: "#cfd8dc",
        2: "#b0bec5",
        3: "#90a4ae",
        4: "#78909c",
        5: "#607d8b",
        6: "#546e7a",
        7: "#455a64",
        8: "#37474f",
        9: "#263238",
    },
}